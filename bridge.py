"""
 * The MIT License
 *
 * Copyright (c) 2024 Peter Isaev
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 * """

#BRIDGE HANDLES NACE-NARS connection with MeTTa (for the world=9 demo)
import sys
import os

useONA = True #whether to use ONA for MeTTa-NARS acceleration instead of MeTTa-NARS with MeTTa-Morph for world=9
useNarsese=False
if "ona" in sys.argv:
    useONA = True
if "narsese" in sys.argv:
    useONA = True
    useNarsese = True
if useONA:
    mettanars = os.path.abspath('../OpenNARS-for-Applications/misc/Python')
    sys.path.append(mettanars)
    cwd = os.getcwd()
    os.chdir(mettanars)
    from MeTTa import *
    os.chdir(cwd)
else:
    mettanars = os.path.abspath('../metta-morph/metta-nars/')
    sys.path.append(mettanars)
    cwd = os.getcwd()
    os.chdir(mettanars)
    from NAR import *
    os.chdir(cwd)
useSpaces = False
if "spaces" in sys.argv and not useNarsese:
    from spaces import space_input, space_init, space_tick
    useSpaces = True
    space_init()

def BRIDGE_INIT(widthval, heightval, BOARDval, SetNACEPlanningObjectiveVal):
    global width, height, BOARD, SetNACEPlanningObjective
    width = widthval
    height = heightval
    BOARD = BOARDval
    SetNACEPlanningObjective = SetNACEPlanningObjectiveVal
    with open("knowledge.metta") as f:
        backgroundknowledge = f.read()
    for belief in backgroundknowledge.split("\n"):
        if belief != "" and not belief.startswith(";"):
            NAR_AddInput(belief)
            if useSpaces:
                space_input(belief)
            NAR_Cycle(30)

def ParseGroundedRelation(METTA):
    R = METTA.split("--> ")[1].split(")")[0]
    S = METTA.split(": (((")[1].split(" x")[0]
    P = METTA.split(" x ")[1].split(")")[0]
    F_C = METTA.split(") (")[1].split(")")[0].split(" ")
    F_C = (float(F_C[0]), float(F_C[1]))
    #print("DEBUG", S, P, R, F_C, METTA, float(F_C[1]) < 0.1, R not in ["left", "right", "up", "down"], len(S), len(P)); input()
    if R not in ["left", "right", "up", "down", "near", "far"] or len(S) > 1 or len(P) > 1:
        exceptionThrown = 1/0 #TODO return flag
    return S, P, R, F_C

def groundedGoal(METTA):
    #s,p,yoff,xoff = groundedFunction(METTA)
    #((S x P) --> left)
    S, P, R, F_C = ParseGroundedRelation(METTA)
    if F_C[1] < 0.5:
        return
    yoffset = "y+1"
    xoffset = "x"
    if R == "up":
        yoffset = "y-1"
        xoffset = "x"
    if R == "down":
        yoffset = "y+1"
        xoffset = "x"
    if R == "left":
        yoffset = "y"
        xoffset = "x-1"
    if R == "right":
        yoffset = "y"
        xoffset = "x+1"
    #print("GROUNDING DEBUG:", S, P, R, yoffset, xoffset)
    STR = f"lambda world: any( world[0][{yoffset}][{xoffset}] == '{S}' and world[0][y][x] == '{P}' for x in range(1, width-1) for y in range(1, height-1))"
    if R == "near":
        STR = f"lambda world: any( (world[0][y-1][x] == '{S}' and world[0][y][x] == '{P}') or (world[0][y+1][x] == '{S}' and world[0][y][x] == '{P}') or (world[0][y][x-1] == '{S}' and world[0][y][x] == '{P}') or (world[0][y][x+1] == '{S}' and world[0][y][x] == '{P}') for x in range(1, width-1) for y in range(1, height-1))"
    if R == "far":
        STR = f"lambda world: not any( (world[0][y-1][x] == '{S}' and world[0][y][x] == '{P}') or (world[0][y+1][x] == '{S}' and world[0][y][x] == '{P}') or (world[0][y][x-1] == '{S}' and world[0][y][x] == '{P}') or (world[0][y][x+1] == '{S}' and world[0][y][x] == '{P}') for x in range(1, width-1) for y in range(1, height-1))"
    #print("FUNC:", STR); input()
    FUNC = eval(STR)
    return FUNC

def truth_expectation(F_C):
    frequency, confidence = F_C
    return confidence * (frequency - 0.5) + 0.5

def groundedBelief(METTA, observed_world, placeTruths):
    S, P, R, F_C = ParseGroundedRelation(METTA)
    if F_C[1] < 0.5:
        return
    yoffset = 1
    xoffset = 0
    if R == "up":
        yoffset = +1
        xoffset = 0
    if R == "down":
        yoffset = -1
        xoffset = 0
    if R == "left":
        yoffset = 0
        xoffset = -1
    if R == "right":
        yoffset = 0
        xoffset = +1
    for x in range(1, width-1):
        for y in range(1, height-1):
            #do not override more confident assignments!
            if observed_world[BOARD][y][x] == S:
                key = (BOARD, y+yoffset, x+xoffset)
                if key not in placeTruths:
                    placeTruths[key] = F_C
                    observed_world[BOARD][y+yoffset][x+xoffset] = P
                else:
                    if truth_expectation(F_C) > truth_expectation(placeTruths[key]):
                        placeTruths[key] = F_C
                        observed_world[BOARD][y+yoffset][x+xoffset] = P
                    else:
                        print("Less truth expectation than prior option"); #input()
            if observed_world[BOARD][y][x] == P:
                key = (BOARD, y-yoffset, x-xoffset)
                if key not in placeTruths:
                    placeTruths[key] = F_C
                    observed_world[BOARD][y-yoffset][x-xoffset] = S
                else:
                    if truth_expectation(F_C[1]) > truth_expectation(placeTruths[key]):
                        placeTruths[key] = F_C
                        observed_world[BOARD][y-yoffset][x-xoffset] = S
                    else:
                        print("Less truth expectation than prior option"); #input()

goal = None
goalTask = ""
def BRIDGE_Tick(observed_world):
    if goal is not None:
        if goal(observed_world): #goal achieved
            beliefEventFromAchievedGoal = "!(AddBeliefEvent " + goalTask.split("(!: ")[1].split(") (")[0] + ")" + " (1.0 0.9)))"
            BRIDGE_Input(beliefEventFromAchievedGoal, observed_world, NACEToNARS=False, ForceMeTTa=True, FromSpace=False)
            if useONA:
                NAR_Cycle(20)
            SetNACEPlanningObjective(eval("lambda world: False"))
    if useSpaces:
        space_tick()

last_observed_world = None
def BRIDGE_Input(METTA, observed_world, NACEToNARS=False, ForceMeTTa=False, FromSpace=False): #can now also be Narsese
    global goal, goalTask, last_observed_world
    if observed_world is not None:
        last_observed_world = observed_world
    else:
        observed_world = last_observed_world
    if useSpaces and not FromSpace:
        space_input(METTA)
    if METTA.startswith("!") or METTA.endswith("! :|:") or METTA.endswith(". :|:") or METTA.endswith(".") or METTA.endswith("?") or METTA.endswith("? :|:"):
        GOAL = "AddGoalEvent" in METTA or METTA.endswith("! :|:")
        #METTA = METTA.replace("AddGoalEvent", "AddBeliefEvent").replace("! :|:", ". :|:")
        useNarseseNow = useNarsese and not ForceMeTTa
        if useNarseseNow:
            METTA2 = NAR_NarseseToMeTTa(METTA)
        else:
            METTA2 = METTA
        atomic_terms = [x for x in METTA2.replace("AddBeliefEvent", "").replace(" x ", " ").replace("(", " ").replace(")", " ").replace("!", "").replace("-->","").split(" ") if x != ""]
        connectors = ["-->", "IntSet", "<->", "<=>"]
        if useNarseseNow:
            NAR_SetUseNarsese(True) #bypass metta translation in this case
            ret = NAR_AddInput(METTA)
            NAR_SetUseNarsese(False)
        else:
            ret = NAR_AddInput(METTA)
        if NACEToNARS:
            return
        tasks = ret["input"] + ret["derivations"]
        ret = NAR_Cycle(20)
        tasks += (ret["input"] + ret["derivations"])
        processGoals = True
        placeTruths = dict([])
        for taskdict in tasks:
            if 'metta' not in taskdict:
                #print("NOT INCLUDED", taskdict); input() TODO FIX
                continue
            task = taskdict['metta'].replace(" * ", " x ")  #transformation only needed for Narsese version
            if useSpaces:
                space_input(taskdict['metta'])
            if "$1" in task or "#1" in task or "<=>" in task or "==>" in task or "=/>" in task or "&&" in task or "||" in task or "/1" in task or "/2" in task: #check only needed for Narsese version
                continue
            if GOAL:
                #print("!!!!!TASK", task)
                try:
                    if processGoals:
                        goalTask = task
                        goal = groundedGoal(task)
                        SetNACEPlanningObjective(goal)
                        processGoals = False
                        print("TASK ACCEPTED", task); #input()
                except:
                    print("TASK REJECTED")
                    None
            elif "(.:" in task:
                #print("!!!!!TASK", task)
                try:
                    groundedBelief(task, observed_world, placeTruths)
                    print("TASK ACCEPTED", task); #input()
                except Exception as ex:
                    print("TASK REJECTED")#,ex)
                    None

def observeSpatialRelation(y,x, observed_world, horizontal=True, vertical=True):
    board = observed_world[BOARD]
    if horizontal:
        valueMid = board[y][x]
        valueLeft = board[y][x-1]
        valueRight = board[y][x+1]
        MeTTaL = f"!(AddBeliefEvent ((({valueRight} x {valueMid}) --> right) (1.0 0.90)))"
        MeTTaR = f"!(AddBeliefEvent ((({valueLeft} x {valueMid}) --> left) (1.0 0.90)))"
        if valueRight != " " and valueMid != " ":
            BRIDGE_Input(MeTTaL, observed_world, NACEToNARS = True, ForceMeTTa = True)
        if valueRight != " " and valueMid != " " and valueLeft != " ":
            if useONA:
                NAR_Cycle(20)
                #NAR_SetUseNarsese(True)
                #NAR_AddInput("*concurrent")
                #NAR_SetUseNarsese(False)
        if valueMid != " " and valueLeft != " ":
            BRIDGE_Input(MeTTaR, observed_world, NACEToNARS = True, ForceMeTTa = True)
    if vertical:
        valueMid = board[y][x]
        valueUp = board[y-1][x]
        valueDown = board[y+1][x]
        MeTTaD = f"!(AddBeliefEvent ((({valueDown} x {valueMid}) --> down) (1.0 0.90)))"
        MeTTaU = f"!(AddBeliefEvent ((({valueUp} x {valueMid}) --> up) (1.0 0.90)))"
        if valueUp != " " and valueMid != " ":
            BRIDGE_Input(MeTTaU, observed_world, NACEToNARS = True, ForceMeTTa = True)
        if valueUp != " " and valueMid != " " and valueDown != " ":
            if useONA:
                NAR_Cycle(20)
                #NAR_SetUseNarsese(True)
                #NAR_AddInput("*concurrent")
                #NAR_SetUseNarsese(False)
        if valueMid != " " and valueDown != " ":
            BRIDGE_Input(MeTTaD, observed_world, NACEToNARS = True, ForceMeTTa = True)

def BRIDGE_observationToNARS(observed_world):
    agent = False
    for x in range(1,width-1):
        for y in range(1,height-1):
            if observed_world[BOARD][y][x] == 'x': #AGENT
                agent_x, agent_y = (x,y)
                agent = True
                observeSpatialRelation(y, x, observed_world)
                NAR_Cycle(20)
                break
        if agent:
            break
