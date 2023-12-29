#Author: Patrick Hammer
from collections import deque
from copy import deepcopy
import sys
import time
import random
from environment import World, Action, WorldNode
from learner import Learner
from learner.Rule import prettyPrintRule

print("Welcome to NACE!")
if "debug" in sys.argv:
    print('Debugger: enter to let agent move, w/a/s/d for manual movement in simulated world, v for switching to imagined world, l to list hypotheses, q to exit imagined world')
else:
    print('Pass "debug" parameter for interactive debugging')
print('Food collecting (1), cup on table challenge (2), doors and keys (3), food collecting with moving object (4), pong (5), input "1", "2", "3", "4", or "5":')
challenge = input()
print('Slippery ground y/n (n default)? Causes the chosen action to have the consequence of another action in 10% of cases.')
slippery = "y" in input()

# THE WORLD
loc = (2,4)
world: WorldNode  = World(challenge, loc).world

agent = Learner(world)



# LET'S SIMULATE FOR 100 STEPS


rules = set([])
negrules = set([])
for t in range(300):
    start_time = time.time()
    rules, negrules, world, debuginput = agent.airis_step(rules, negrules, deepcopy(world))
    end_time = time.time()
    print("VALUES", world.values)
    elapsed_time = end_time - start_time
    if elapsed_time < 1.0:
        time.sleep(1.0 - elapsed_time)
    if "debug" in sys.argv and debuginput != "" and debuginput != "w" and debuginput != "a" and debuginput != "s" and debuginput != "d" and debuginput != "l":
        saveworld: WorldNode = deepcopy(world)
        predworld: WorldNode = deepcopy(world)
        score = 0.0
        while True:
            print("\033[1;1H\033[2J")
            print(predworld)
            print("score:", score)
            d = input()
            score = 0.0
            if d == 'q':
                break
            if d == 'r':
                predworld = deepcopy(world)
            if d == 'a':
                predworld, score, age = agent.world_predict(deepcopy(predworld), Action.L, rules)
            if d == 'd':
                predworld, score, age = agent.world_predict(deepcopy(predworld), Action.R, rules)
            if d == 'w':
                predworld, score, age = agent.world_predict(deepcopy(predworld), Action.U, rules)
            if d == 's':
                predworld, score, age = agent.world_predict(deepcopy(predworld), Action.D, rules)
            if d == 'l':
                for x in rules:
                    prettyPrintRule(x)
                input()
            if d == 'n':
                for x in negrules:
                    prettyPrintRule(x)
                input()
