#Author: Patrick Hammer
from collections import deque
from copy import deepcopy
import sys
import time
import random
from constants import * 
import world as W
import prettyprint as P
import knowledge as K
import learner as L

print("Welcome to NACE!")
if "debug" in sys.argv:
    print('Debugger: enter to let agent move, w/a/s/d for manual movement in simulated world, v for switching to imagined world, l to list hypotheses, q to exit imagined world')
else:
    print('Pass "debug" parameter for interactive debugging')
print('Food collecting (1), cup on table challenge (2), doors and keys (3), food collecting with moving object (4), pong (5), input "1", "2", "3", "4", or "5":')
challenge = "2" # input()
print('Slippery ground y/n (n default)? Causes the chosen action to have the consequence of another action in 10% of cases.')
W.slippery = False # "y" in input()

W.choose_world(challenge)



for t in range(300):
    W.t = t
    start_time = time.time()
    L.rules, L.negrules, W.world, debuginput = L.airis_step(L.rules, L.negrules, deepcopy(W.world))
    end_time = time.time()
    print("VALUES", W.world[VALUES])
    print(f"-- {end_time-start_time:.2f} s/it --")
    elapsed_time = end_time - start_time
    if elapsed_time < 1.0: pass
        # time.sleep(1.0 - elapsed_time)
    if "debug" in sys.argv and debuginput != "" and debuginput != "w" and debuginput != "a" and debuginput != "s" and debuginput != "d" and debuginput != "l":
        saveworld = deepcopy(W.world)
        predworld = deepcopy(W.world)
        score = 0.0
        while True:
            print("\033[1;1H\033[2J")
            P.printworld(predworld)
            print("score:", score)
            d = input()
            score = 0.0
            if d == 'q':
                break
            if d == 'r':
                predworld = deepcopy(W.world)
            if d == 'a':
                predworld, score, age = L.world_predict(deepcopy(predworld), W.left, L.rules)
            if d == 'd':
                predworld, score, age = L.world_predict(deepcopy(predworld), W.right, L.rules)
            if d == 'w':
                predworld, score, age = L.world_predict(deepcopy(predworld), W.up, L.rules)
            if d == 's':
                predworld, score, age = L.world_predict(deepcopy(predworld), W.down, L.rules)
            if d == 'l':
                for x in L.rules:
                    P.prettyPrintRule(x)
                input()
            if d == 'n':
                for x in L.negrules:
                    P.prettyPrintRule(x)
                input()
    
    
