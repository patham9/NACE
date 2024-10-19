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
from base_utils import Logger as log

log.init_message("debug" in sys.argv)

from nace import *

adversaryWorld = "adversary" in sys.argv or getIsWorld0()
interactiveWorld = "manual" not in sys.argv and ("interactive" in sys.argv or getIsWorld9())
if interactiveWorld:
    from bridge import *
    BRIDGE_INIT(width, height, BOARD, World_SetObjective)

#Configure hypotheses to use euclidean space properties if desired
Hypothesis_UseMovementOpAssumptions(left, right, up, down, drop, "DisableOpSymmetryAssumption" in sys.argv or World_Num5())
#Run the simulation in a loop for up to k steps:
Time = -1
behavior = "BABBLE"
plan = []

def safe_check(item):
    """Return True if item is True, catch exceptions and return False."""
    try:
        return bool(item)
    except Exception:
        return False

def safe_any(condition):
    """Return True if any condition holds; catch exceptions and return False for the iteration with an exception."""
    return any(
        (safe_check(item) for item in condition)
    )

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
        asked = True
        while asked:
            print("MeTTa input:")
            METTA = input()
            #example: the cup should be above the coffee machine
            #example: the cup should be above the table
            #example: the cup should be above the table and the agent should be below the table
            if METTA.strip() == "":
                break
            COND = METTA
            PROMPT = f"Imagine you have a 2D array named 'grid' of ASCII characters, first y coordinate then x in indexing order. up means y-1, down means y+1, right means x+1, left means x-1. Now knowing the grid has width 'width' and height 'height' now define a condition which reflects {COND} in Python, only return the Python condition which when evaluated at a particular x,y position would return True or False."
            PROMPT += "Please consider the mapping u=cup, G=coffee machine, T=table, x=agent, o=wall, H=cabinet"
           
            
            from openai import OpenAI

            client = OpenAI(
              api_key=''
            )

            completion = client.chat.completions.create(
              model="o1-preview", #gpt-4o, o1-preview
              messages=[
                {"role": "user", "content": PROMPT}
              ]
            )

            #import os
            response = completion.choices[0].message.content.replace("grid","world[0]")
            response = "lambda world: safe_any(" + response.split("python")[1].split('```')[0].strip() + " for y in range(height) for x in range(width))"
            #os.system('say "' + response + '"')
            print("!!!!", response); input()
            
            World_SetObjective(eval(response))
            break
            #BRIDGE_Input(METTA, observed_world, NACEToNARS = False)
            #if not METTA.endswith("?") and not METTA.endswith("? :|:") and not METTA.startswith("!(EternalQuestion ") and not METTA.startswith("!(EventQuestion "):
            #    asked = False
    start_time = time.time()
    usedRules, FocusSet, RuleEvidence, loc, observed_world, rules, negrules, world, debuginput, values, lastplanworld, planworld, behavior, plan = NACE_Cycle(Time, FocusSet, RuleEvidence, loc, observed_world, rules, negrules, deepcopy(world), inject_key)
    if interactiveWorld:
        BRIDGE_observationToNARS(observed_world)
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
    return usedRules, FocusSet, RuleEvidence, loc, observed_world, rules, negrules, world, debuginput, values, lastplanworld, planworld, behavior, plan, Time

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
    exit()

else:
    from gui import *
    GUI_INIT(Step, NACE_Predict, world, loc, left, right, up, down, pick, drop, toggle, width, height, behavior, plan, observed_world)
