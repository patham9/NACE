#Author: Patrick Hammer
import sys
import time
print("Welcome to NACE!")
if "debug" in sys.argv:
    print('Debugger: enter to let agent World_Move, w/a/s/d for manual World_Movement in simulated world, v for switching to imagined world, l to list hypotheses, q to exit imagined world')
else:
    print('Pass "debug" parameter for interactive debugging')
from nace import *

if __name__ == "__main__":
    for Time in range(300):
        start_time = time.time()
        RuleEvidence, worldchange, loc, observed_world, rules, negrules, world, debuginput = NACE_Cycle(Time, RuleEvidence, worldchange, loc, observed_world, rules, negrules, deepcopy(world))
        end_time = time.time()
        print("VALUES", world[VALUES])
        elapsed_time = end_time - start_time
        if elapsed_time < 1.0:
            time.sleep(1.0 - elapsed_time)
        if "debug" in sys.argv and debuginput != "" and debuginput != "w" and debuginput != "a" and debuginput != "s" and debuginput != "d" and debuginput != "l":
            saveworld = deepcopy(world)
            predworld = deepcopy(world)
            score = 0.0
            while True:
                print("\033[1;1H\033[2J")
                World_Print(predworld)
                print("score:", score)
                d = input()
                score = 0.0
                if d == 'q':
                    break
                if d == 'r':
                    predworld = deepcopy(world)
                if d == 'a':
                    predworld, score, age = world_predict(Time, deepcopy(predworld), left, rules)
                if d == 'd':
                    predworld, score, age = world_predict(Time, deepcopy(predworld), right, rules)
                if d == 'w':
                    predworld, score, age = world_predict(Time, deepcopy(predworld), up, rules)
                if d == 's':
                    predworld, score, age = world_predict(Time, deepcopy(predworld), down, rules)
                if d == 'l':
                    for x in rules:
                        Prettyprint_rule(RuleEvidence, Hypothesis_TruthValue, x)
                    input()
                if d == 'n':
                    for x in negrules:
                        Prettyprint_rule(x)
                    input()
