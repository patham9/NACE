"""
 * The MIT License
 *
 * Copyright (c) 2024 Patrick Hammer
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

import os
import sys
import time
print("Welcome to NACE!")
if "debug" in sys.argv:
    print('Debugger: enter to let agent World_Move, w/a/s/d for manual World_Movement in simulated world, v for switching to imagined world, l to list hypotheses, p to look through the predicted plan step-wise, q to exit imagined world')
else:
    print("""COMMAND-LINE PARAMETERS:
Pass "debug" parameter for interactive debugging, 
"silent" for hiding hypothesis formation output, 
"manual" for trying the environment as a human, 
"nosleep" to remove simulation visualization delay, 
"nopredictions" to hide prediction rectangles,
"nogui" to hide GUI,
"notextures" to not render textures in GUI, 
"colors" to render colors.
"interactive" for MeTTa-NARS bridge with shell,
"adversary" to add shell-controllable player character,
"frames=b" to create a gif file including frames until frame b.
"startframe=a" optional to let the gif start later.
"world=k" to start world k without asking for the world input.
"ona" to use ONA with MeTTa interface in world=9 instead of MeTTa-NARS,
""")
from nace import *

useONA = False #whether to use OpenNARS-for-Applications instead of MeTTa-NARS for world=9
useNarsese=False
if "ona" in sys.argv:
    useONA = True
if "narsese" in sys.argv:
    useONA = True
    useNarsese = True
adversaryWorld = "adversary" in sys.argv or getIsWorld0()
interactiveWorld = "manual" not in sys.argv and ("interactive" in sys.argv or getIsWorld9())
if interactiveWorld:
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

def groundedGoal(METTA):
    #s,p,yoff,xoff = groundedFunction(METTA)
    #((S x P) --> left)
    pred = METTA.split("--> ")[1].split(")")[0]
    if pred not in ["left", "right", "up", "down"]:
        exceptionThrown = 1/0 #TODO return flag
    S = METTA.split("(!: (((")[1].split(" x")[0]
    P = METTA.split(" x ")[1].split(")")[0]
    yoffset = "y+1"
    xoffset = "x"
    if pred == "up":
        yoffset = "y-1"
        xoffset = "x"
    if pred == "down":
        yoffset = "y+1"
        xoffset = "x"
    if pred == "left":
        yoffset = "y"
        xoffset = "x-1"
    if pred == "right":
        yoffset = "y"
        xoffset = "x+1"
    print("GROUNDING DEBUG:", S, P, yoffset, xoffset)
    STR = f"lambda world: any( world[BOARD][{yoffset}][{xoffset}] == '{S}' and world[BOARD][y][x] == '{P}' for x in range(1, width-1) for y in range(1, height-1))"
    print("FUNC:", STR)
    FUNC = eval(STR)
    return FUNC

def groundedBelief(METTA):
    pred = METTA.split("--> ")[1].split(")")[0]
    S = METTA.split("(.: (((")[1].split(" x")[0]
    P = METTA.split(" x ")[1].split(")")[0]
    #print("DEBUG", S, P); input()
    yoffset = 1
    xoffset = 0
    if pred == "up":
        yoffset = +1
        xoffset = 0
    if pred == "down":
        yoffset = -1
        xoffset = 0
    if pred == "left":
        yoffset = 0
        xoffset = -1
    if pred == "right":
        yoffset = 0
        xoffset = +1
    for x in range(1,width-1):
        for y in range(1,height-1):
            if observed_world[BOARD][y][x] == S:
                 observed_world[BOARD][y+yoffset][x+xoffset] = P
            if observed_world[BOARD][y][x] == P:
                observed_world[BOARD][y-yoffset][x-xoffset] = S

#Configure hypotheses to use euclidean space properties if desired
Hypothesis_UseMovementOpAssumptions(left, right, up, down, drop, "DisableOpSymmetryAssumption" in sys.argv or World_Num5())
#Run the simulation in a loop for up to k steps:
Time = -1
behavior = "BABBLE"
plan = []
def Step(inject_key=""):
    global usedRules, FocusSet, RuleEvidence, loc, observed_world, rules, negrules, world, debuginput, values, lastplanworld, planworld, behavior, plan, Time
    Time+=1
    if adversaryWorld:
        print("Adversary movement (w/a/s/d):")
        direction = input()
        BREAK = False
        if direction == "s":
            for i in range(1,width-1):
                for j in range(1,height-1):
                    if world[BOARD][j][i] == HUMAN and world[BOARD][j+1][i] == ' ':
                        world[BOARD][j][i] = ' '
                        world[BOARD][j+1][i] = HUMAN
                        BREAK = True; break
                if BREAK: break
        if direction == "w":
            for i in range(1,width-1):
                for j in range(1,height-1):
                    if world[BOARD][j][i] == HUMAN and world[BOARD][j-1][i] == ' ':
                        world[BOARD][j][i] = ' '
                        world[BOARD][j-1][i] = HUMAN
                        BREAK = True; break
                if BREAK: break
        if direction == "d":
            for i in range(1,width-1):
                for j in range(1,height-1):
                    if world[BOARD][j][i] == HUMAN and world[BOARD][j][i+1] == ' ':
                        world[BOARD][j][i] = ' '
                        world[BOARD][j][i+1] = HUMAN
                        BREAK = True; break
                if BREAK: break
        if direction == "a":
            for i in range(1,width-1):
                for j in range(1,height-1):
                    if world[BOARD][j][i] == HUMAN and world[BOARD][j][i-1] == ' ':
                        world[BOARD][j][i] = ' '
                        world[BOARD][j][i-1] = HUMAN
                        BREAK = True; break
                if BREAK: break
    if interactiveWorld: #(:! ((0 x _) --> left))
        print("MeTTa input:")
        METTA = input() #f"(:! ((4 x 0) --> left))"
        if METTA.startswith("!") or METTA.endswith("! :|:") or METTA.endswith(". :|:") or METTA.endswith("?") or METTA.endswith("? :|:"):
            GOAL = "AddGoalEvent" in METTA or METTA.endswith("! :|:")
            METTA = METTA.replace("AddGoalEvent", "AddBeliefEvent").replace("! :|:", ". :|:")
            if useNarsese:
                METTA2 = NAR_NarseseToMeTTa(METTA)
            else:
                METTA2 = METTA
            atomic_terms = METTA2.replace(" x ", " ").replace("(", " ").replace(")", " ").replace("!", "").split(" ")
            connectors = ["-->", "IntSet", "<->", "<=>"]
            with open("knowledge.metta") as f:
                backgroundknowledge = f.read()
            for belief in backgroundknowledge.split("\n"):
                if belief != "" and not belief.startswith(";"):
                    for atomic_term in atomic_terms:
                        if atomic_term != "AddBeliefEvent" and atomic_term != "" and atomic_term not in connectors and atomic_term in belief and not atomic_term.replace(".","").isnumeric():
                            NAR_AddInput(belief)
                            break
            if useNarsese:
                NAR_SetUseNarsese(True) #bypass metta translation in this case
                ret = NAR_AddInput(METTA)
                NAR_SetUseNarsese(False)
            else:
                ret = NAR_AddInput(METTA)
            tasks = ret["input"] + ret["derivations"]
            ret = NAR_Cycle(2)
            tasks += (ret["input"] + ret["derivations"])
            processGoals = True
            for taskdict in tasks:
                if 'metta' not in taskdict:
                    #print("NOT INCLUDED", taskdict); input() TODO FIX
                    continue
                task = taskdict['metta'].replace(" * ", " x ")  #transformation only needed for Narsese version
                if "$1" in task or "#1" in task or "<=>" in task or "==>" in task or "=/>" in task: #check only needed for Narsese version
                    continue
                if GOAL: #"(!:" in task:
                    task = task.replace("(.:", "(!:")
                    print("!!!!!TASK", task)
                    try:
                        if processGoals:
                            World_SetObjective(groundedGoal(task))
                            processGoals = False
                            print("TASK ACCEPTED")
                    except:
                        print("TASK REJECTED")
                        None
                elif "(.:" in task:
                    print("!!!!!TASK", task)
                    try:
                        groundedBelief(task)
                        print("TASK ACCEPTED")
                    except:
                        print("TASK REJECTED")
                        None
    start_time = time.time()
    usedRules, FocusSet, RuleEvidence, loc, observed_world, rules, negrules, world, debuginput, values, lastplanworld, planworld, behavior, plan = NACE_Cycle(Time, FocusSet, RuleEvidence, loc, observed_world, rules, negrules, deepcopy(world), inject_key)
    end_time = time.time()
    print("score=" + str(world[VALUES][0]) + ", vars="+str(list(world[VALUES][1:])), end="")
    if "manual" in sys.argv:
        print()
    else:
        print(",", "focus="+str(FocusSet))
    elapsed_time = end_time - start_time
    if elapsed_time < 1.0 and "nosleep" not in sys.argv and "debug" not in sys.argv and "manual" not in sys.argv:
        time.sleep(1.0 - elapsed_time)
    if "debug" in sys.argv and debuginput != "" and debuginput not in ["w", "a", "s", "d", "l", "p", "enter", "b", "n", "t"]:
        predworld = deepcopy(observed_world)
        score = 0.0
        while True:
            print("\033[1;1H\033[2J")
            print("\033[0mImagined map:\033[97;43m")
            World_Print(predworld)
            print("\033[0m")
            NACE_PrintScore(score)
            print("values:", values)
            d = input()
            score = 0.0
            if d == 'q' or d == 'i':
                break
            if d == 'r':
                predworld = deepcopy(observed_world)
            if d == 'a':
                predworld, score, age, values = NACE_Predict(Time, FocusSet, deepcopy(predworld), left, usedRules)
            if d == 'd':
                predworld, score, age, values = NACE_Predict(Time, FocusSet, deepcopy(predworld), right, usedRules)
            if d == 'w':
                predworld, score, age, values = NACE_Predict(Time, FocusSet, deepcopy(predworld), up, usedRules)
            if d == 's':
                predworld, score, age, values = NACE_Predict(Time, FocusSet, deepcopy(predworld), down, usedRules)
            if d == 'b':
                predworld, score, age, values = NACE_Predict(Time, FocusSet, deepcopy(predworld), pick, usedRules)
            if d == 'n':
                predworld, score, age, values = NACE_Predict(Time, FocusSet, deepcopy(predworld), drop, usedRules)
            if d == 't':
                predworld, score, age, values = NACE_Predict(Time, FocusSet, deepcopy(predworld), toggle, usedRules)
            if d == 'l':
                for x in rules:
                    Prettyprint_rule(RuleEvidence, Hypothesis_TruthValue, x)
                input()
            if d == 'n':
                for x in negrules:
                    Prettyprint_rule(x)
                input()

if adversaryWorld:
    for i in range(1,width-1):
        BREAK = False
        for j in range(1,height-1):
            if world[BOARD][j][i] == ' ':
                world[BOARD][j][i] = HUMAN
                BREAK = True; break
        if BREAK: break

if "nogui" in sys.argv:
    for Time in range(300):
        Step()

if "nogui" in sys.argv:
    exit()
else:
    from matplotlib.animation import FuncAnimation
    from matplotlib.patches import FancyArrow
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle, Circle
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch
    import matplotlib.colors as mc
    from nace import _IsPresentlyObserved
    import colorsys
    import os

    def lighten_color(color, amount=0.5):
        try:
            c = mc.cnames[color]
        except:
            c = color
        c = colorsys.rgb_to_hls(*mc.to_rgb(c))
        return colorsys.hls_to_rgb(c[0], 1 - amount * (1 - c[1]), c[2])

    predicted_certainty = None
    def plot_pattern(pattern, values, DrawPredictions=True):
        global loc, predicted_certainty
        if DrawPredictions and "nopredictions" in sys.argv:
            DrawPredictions = False
        rows = len(pattern)
        cols = len(pattern[0])
        ax.clear()
        for i in range(rows):
            for j in range(cols):
                color = colors.get(pattern[i][j], 'white')
                lastaction = None
                if len([x for x in plan if x == left or x == right]) > 0:
                    lastaction = [x for x in plan if x == left or x == right][-1]
                if "colors" not in sys.argv:
                    if pattern[i][j] == ".":
                        color = "gray"
                        color = lighten_color(color, 0.6)
                    elif _IsPresentlyObserved(Time, observed_world, i, j):
                        color = "white"
                    else:
                        color = "lightgray"
                else:
                    if not _IsPresentlyObserved(Time, observed_world, i, j) and color != "gray":
                        if color == "white":
                            color = "lightgray"
                        else:
                            color = lighten_color(color, 1.2)
                ax.add_patch(Rectangle((j, -i), 1, 1, facecolor=color, edgecolor='none'))
                if "manual" not in sys.argv and DrawPredictions and observed_world[BOARD][i][j] != planworld[BOARD][i][j]:
                    color = colors.get(planworld[BOARD][i][j], 'white')
                    if "colors" not in sys.argv:
                        if pattern[i][j] == ".":
                            color = "gray"
                        elif _IsPresentlyObserved(Time, observed_world, i, j):
                            color = "lightgray"
                        else:
                            color = "gray"
                    elif not _IsPresentlyObserved(Time, observed_world, i, j) and color != "gray":
                        if color == "white":
                            color = "lightgray"
                        else:
                            color = lighten_color(color, 1.2)
                    color = lighten_color(color, 1.1)
                    patt = planworld[BOARD][i][j]
                    if behavior == "CURIOUS" and planworld[BOARD][i][j] != lastplanworld[BOARD][i][j]:
                        patt = "what"
                    if patt == ".":
                        patt = "unknown"
                    ax.add_patch(Circle((j+0.5, -i+0.5), 0.25, facecolor=color, edgecolor='none', zorder=50, alpha=0.8))
                    if patt != "what" and (((lastaction is None and direction == "right") or lastaction == right) and patt == ROBOT) or patt.isupper():
                        patt += "2"
                    if "notextures" not in sys.argv and patt != " ":
                        # Display the texture inside the rectangle using imshow
                        ax.imshow(M[patt], extent=(j+0.3, j + 0.7, -i+0.3, -i + 0.7), zorder=100)
                patt = pattern[i][j]
                if (direction == "right" and patt == 'x') or patt.isupper():
                    patt += "2"
                if patt == ".":
                    patt = "unknown"
                if "notextures" not in sys.argv and patt in M:
                    # Display the texture inside the rectangle using imshow
                    ax.imshow(M[patt], extent=(j, j + 1, -i, -i + 1), zorder=10)
        # Map of actions to changes in x and y
        action_dict = {left: (-1, 0), right: (1, 0), up: (0, 1), down: (0, -1), pick: (0, 0), drop: (0, 0), toggle: (0, 0)}
        # Plot path
        if len(plan) > 0 and DrawPredictions:
            (x,y) = (loc[0]+0.5,-loc[1]+0.5)
            vizloc = loc
            #nextstepworld, _, __, ___ = NACE_Predict(Time, FocusSet, deepcopy(observed_world), plan[0], usedRules)
            nextstepworld = observed_world
            for i, action in enumerate(plan[1:]):
                dx, dy = action_dict[action]
                if i == len(plan[1:])-1:
                    ax.add_patch(FancyArrow(x, y, dx, dy, color='black', width=0.01, head_width=0.1, head_length=0.2))
                else:
                    ax.add_line(Line2D([x, x + dx], [y, y + dy], color='black'))
                nextstepworld, predscore, __, ___ = NACE_Predict(Time, FocusSet, deepcopy(nextstepworld), action, usedRules)
                #now check if there is indeed a robot predicted to be there
                #(to take into account that the agent indeed knows how location is affected, which matters for visualization, as in egg world)
                tx = x + dx
                ty = y + dy
                tvizloc = action(vizloc)
                if tvizloc[1] >= 0 and tvizloc[1] < height and tvizloc[0] >= 0 and tvizloc[0] < width and nextstepworld[BOARD][tvizloc[1]][tvizloc[0]] == ROBOT:
                    (x, y, vizloc) = (tx, ty, tvizloc)
        ax.set_xlim(0, width)  # Set the desired x-axis limits
        ax.set_ylim(-rows+1, 1)  # Set the desired y-axis limits
        ax.set_aspect('equal', adjustable='box')
        ax.set_xticks(range(cols+1))
        ax.set_yticks(range(-rows+1, 1))
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.grid(False)
        plt.title(behavior + " score=" + str(values[0]) + " vars="+str(list(values[1:])) + ("" if predicted_certainty is None else " certainty="+str(predicted_certainty)))
        plt.draw()

    def updateloc(key=""):
        global lastloc, direction
        if loc[0] > lastloc[0] or key == "d":
            direction = "right"
        if loc[0] < lastloc[0] or key == "a":
            direction = "left"
        lastloc = loc

    predworldi = None
    def on_key(event):
        global predworldi, predicted_certainty
        predicted_certainty = None
        if event.key in ["w", "s", "a", "d", "p", "enter", "r", "b", "n", "t"]:
            if predworldi is None and event.key != 'r':
                Step(inject_key = event.key)
                updateloc(event.key)
                plot_pattern(observed_world[BOARD], observed_world[VALUES], event.key not in ["w", "s", "a", "d", "b", "n", "t"])
            else:
                if event.key == 'r':
                    predworldi = deepcopy(observed_world)
                    predicted_certainty = 1.0
                else:
                    score = 1.0
                    if event.key == 'a':
                        predworldi, score, age, values = NACE_Predict(Time, FocusSet, deepcopy(predworldi), left, usedRules)
                    if event.key == 'd':
                        predworldi, score, age, values = NACE_Predict(Time, FocusSet, deepcopy(predworldi), right, usedRules)
                    if event.key == 'w':
                        predworldi, score, age, values = NACE_Predict(Time, FocusSet, deepcopy(predworldi), up, usedRules)
                    if event.key == 's':
                        predworldi, score, age, values = NACE_Predict(Time, FocusSet, deepcopy(predworldi), down, usedRules)
                    if event.key == 'b':
                        predworldi, score, age, values = NACE_Predict(Time, FocusSet, deepcopy(predworldi), pick, usedRules)
                    if event.key == 'n':
                        predworldi, score, age, values = NACE_Predict(Time, FocusSet, deepcopy(predworldi), drop, usedRules)
                    if event.key == 't':
                        predworldi, score, age, values = NACE_Predict(Time, FocusSet, deepcopy(predworldi), toggle, usedRules)
                    if score >= 0.0 and score <= 1.0:
                        predicted_certainty = score
                plot_pattern(predworldi[BOARD], predworldi[VALUES], DrawPredictions=False)
        if event.key == "i":
            if predworldi is None:
                predworldi = deepcopy(observed_world)
            else:
                predworldi = None
        if event.key == "l":
            for x in rules:
                Prettyprint_rule(RuleEvidence, Hypothesis_TruthValue, x)
        if event.key == "u":
            for x in usedRules:
                Prettyprint_rule(RuleEvidence, Hypothesis_TruthValue, x)
        if event.key == "x":
            for x in rules - usedRules:
                Prettyprint_rule(RuleEvidence, Hypothesis_TruthValue, x)
    frame = 1
    def update(wat):
        global lastloc, direction, frame
        start = 1
        for arg in sys.argv:
            if arg.startswith("startframe="):
                start = int(arg.split("startframe=")[1])
        if frame >= start:
            Step()
            updateloc()
        plot_pattern(observed_world[BOARD], observed_world[VALUES])
        frame += 1

    lastloc = loc
    direction = "right"
    M = {}
    if "notextures" not in sys.argv:
        # Iterate through files in the folder
        for filename in os.listdir("textures"):
            # Check if the file has a ".png" extension
            if filename.endswith(".png"):
                # Remove the ".png" extension to get the key
                key = os.path.splitext(filename)[0]
                # Add to dictionary M
                M[key] = plt.imread('textures/' + filename)
    planworld = [[["." for x in world[BOARD][i]] for i in range(len(world[BOARD]))], world[VALUES], world[TIMES]]
    lastplanworld = planworld
    pattern = [
        "............",
        "............",
        "............",
        "............",
        "............",
        "............",
        "............"
    ]
    colors = {
        COFFEEMACHINE: "black",
        ' ': 'white',
        ROBOT: 'red',
        '.': 'gray',
        #food level:
        WALL: 'blue',
        FOOD: 'green',
        ARROW_DOWN: 'purple',
        ARROW_UP: 'darkblue',
        #cup table level:
        CUP: 'cyan', #purple
        TABLE: 'orange',
        #door key battery level:
        DOOR: 'cyan', 
        KEY: 'magenta',
        BATTERY: 'green',
        #pong
        BALL: 'green',
        #egg level:
        EGG: 'orange',
        EGGPLACE: 'cyan',
        CHICKEN: 'green',
        #soccer:
        GOAL: 'green',
        SBALL: 'orange',
        #eletric shock level
        SHOCK: "yellow",
        TRASH: "magenta"
    }
    fig, ax = plt.subplots()
    plt.rcParams['keymap.save'].remove('s')
    plt.rcParams['keymap.quit'].remove('q')
    plot_pattern(pattern, [0, 0])
    fig.canvas.mpl_connect('key_press_event', on_key)
    if "manual" not in sys.argv and "debug" not in sys.argv:
        frames = 0
        worldname = ""
        for arg in sys.argv:
            if arg.startswith("frames="):
                frames = int(arg.split("frames=")[1])
            if arg.startswith("world="):
                worldname = arg.split("world=")[1]
        if frames > 0:
            ani = FuncAnimation(fig, update, interval=100, repeat=False, frames=frames)  # Update every 100 milliseconds
            ani.save(f'world{worldname}.gif', writer='imagemagick', fps=1)
        else:
            ani = FuncAnimation(fig, update, interval=100)  # Update every 100 milliseconds
    plt.show()

