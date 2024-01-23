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

import sys
import time
print("Welcome to NACE!")
if "debug" in sys.argv:
    print('Debugger: enter to let agent World_Move, w/a/s/d for manual World_Movement in simulated world, v for switching to imagined world, l to list hypotheses, p to look through the predicted plan step-wise, q to exit imagined world')
else:
    print('Pass "debug" parameter for interactive debugging, "silent" for hiding hypothesis formation output, "manual" for trying the environment as a human, "nosleep" to renove simulation visualization delay.')
from nace import *

#Configure hypotheses to use euclidean space properties if desired
Hypothesis_UseMovementOpAssumptions(left, right, up, down, "DisableOpSymmetryAssumption" in sys.argv)
#Run the simulation in a loop for up to k steps:
if __name__ == "__main__":
    for Time in range(300):
        start_time = time.time()
        usedRules, FocusSet, RuleEvidence, loc, observed_world, rules, negrules, world, debuginput, values = NACE_Cycle(Time, FocusSet, RuleEvidence, loc, observed_world, rules, negrules, deepcopy(world))
        end_time = time.time()
        print("score=" + str(world[VALUES][0]) + ", vars="+str(list(world[VALUES][1:]))+",", "focus="+str(FocusSet))
        elapsed_time = end_time - start_time
        if elapsed_time < 1.0 and "nosleep" not in sys.argv:
            time.sleep(1.0 - elapsed_time)
        if "debug" in sys.argv and debuginput != "" and debuginput not in ["w", "a", "s", "d", "l", "p"]:
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
                if d == 'q':
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
                if d == 'l':
                    for x in rules:
                        Prettyprint_rule(RuleEvidence, Hypothesis_TruthValue, x)
                    input()
                if d == 'n':
                    for x in negrules:
                        Prettyprint_rule(x)
                    input()
