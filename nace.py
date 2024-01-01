#Author: Patrick Hammer
from collections import deque
from copy import deepcopy
import sys
import time
import random

# THE WORLD
world = """
oooooooooooo
o   o   f  o
o          o
o   oooooooo
o x        o
o       u  o
oooooooooooo
"""
world2 = """
oooooooooooo
o          o
o   u      o
o     ooooTo
o x        o
o          o
oooooooooooo
"""
world3 = """
oooooooooooo
o  k  o   ko
o     D b  o
o     oooooo
o x   D b  o
o     o   ko
oooooooooooo
"""
world4 = """
oooooooooooo
o   o   f  o
o          o
o   oooooooo
o x v      o
o       u  o
oooooooooooo
"""
world5 = """
oooooooooooo
oo          
oo          
oo         c
oox         
oo          
oooooooooooo
"""

print("Welcome to NACE!")
if "debug" in sys.argv:
    print('Debugger: enter to let agent move, w/a/s/d for manual movement in simulated world, v for switching to imagined world, l to list hypotheses, q to exit imagined world')
else:
    print('Pass "debug" parameter for interactive debugging')
print('Food collecting (1), cup on table challenge (2), doors and keys (3), food collecting with moving object (4), pong (5), input "1", "2", "3", "4", or "5":')
challenge = input()
print('Slippery ground y/n (n default)? Causes the chosen action to have the consequence of another action in 10% of cases.')
slippery = "y" in input()
isWorld5 = False
if "2" in challenge:
    world = world2
if "3" in challenge:
    world = world3
if "4" in challenge:
    world = world4
if "5" in challenge:
    world = world5
    isWorld5 = True

VIEWDISTX, VIEWDISTY = (3, 2)
WALL, ROBOT, CUP, FOOD, BATTERY, FREE, TABLE, KEY, DOOR, ARROW_DOWN, ARROW_UP, BALL = ('o', 'x', 'u', 'f', 'b', ' ', 'T', 'k', 'D', 'v', '^', 'c')
world=[[[*x] for x in world[1:-1].split("\n")], tuple([0, 0])]
BOARD, VALUES, TIMES = (0, 1, 2)
def printworld(world):
    for line in world[BOARD]:
        print("".join(line))
height, width = (len(world[BOARD]), len(world[BOARD][0]))
world.append([[float("-inf") for i in range(width)] for j in range(height)])

# MOVE FUNCTIONS TAKING WALLS INTO ACCOUNT
def left(loc):
    return (loc[0]-1, loc[1])
def right(loc):
    return (loc[0]+1, loc[1])
def up(loc):
    return (loc[0],   loc[1]-1)
def down(loc):
    return (loc[0],   loc[1]+1)
def move(loc, world, action):
    if slippery and random.random() > 0.9: #agent still believes it did the proper action
        action = random.choice(actions)    #but the world is slippery!
    newloc = action(loc)
    oldworld = deepcopy(world)
    #ROBOT MOVEMENT ON FREE SPACE
    if oldworld[BOARD][newloc[1]][newloc[0]] == FREE:
        world[BOARD][loc[1]][loc[0]] = FREE
        loc = newloc
        world[BOARD][loc[1]][loc[0]] = ROBOT
    oldworld = deepcopy(world)
    for y in range(height):
        for x in range(width):
            if oldworld[BOARD][y][x] == BALL and oldworld[BOARD][y][x-1] == FREE:
                world[BOARD][y][x-1] = BALL
                world[BOARD][y][x] = FREE
            if oldworld[BOARD][y][x] == BALL and oldworld[BOARD][y][x-1] == WALL:
                world[BOARD][y][x] = FREE
                world[BOARD][random.choice(range(1, height-1))][width-1] = BALL
            if oldworld[BOARD][y][x] == ARROW_DOWN and oldworld[BOARD][y+1][x] == FREE:
                world[BOARD][y+1][x] = ARROW_DOWN
                world[BOARD][y][x] = FREE
            if oldworld[BOARD][y][x] == ARROW_UP and oldworld[BOARD][y-1][x] == FREE:
                world[BOARD][y-1][x] = ARROW_UP
                world[BOARD][y][x] = FREE
            if oldworld[BOARD][y][x] == ARROW_DOWN and oldworld[BOARD][y+1][x] == WALL:
                world[BOARD][y][x] = ARROW_UP
            if oldworld[BOARD][y][x] == ARROW_UP and oldworld[BOARD][y-1][x] == WALL:
                world[BOARD][y][x] = ARROW_DOWN
            if oldworld[BOARD][y][x] == CUP and oldworld[BOARD][y+1][x] == TABLE:
                world[BOARD][y][x] = FREE
                while True:
                    xr, yr = (random.randint(0, width-1), random.randint(0, height-1))
                    if oldworld[BOARD][yr][xr] == FREE:
                        world[BOARD][yr][xr] = CUP
                        break
    #CUP
    if world[BOARD][newloc[1]][newloc[0]] == CUP: #an object the system could shift around
        world[BOARD][loc[1]][loc[0]] = CUP
        loc = newloc
        world[BOARD][loc[1]][loc[0]] = ROBOT
    #KEY
    if world[BOARD][newloc[1]][newloc[0]] == KEY:
        world[BOARD][loc[1]][loc[0]] = FREE
        loc = newloc
        world[BOARD][loc[1]][loc[0]] = ROBOT
        world[VALUES] = tuple([world[VALUES][0]] + [world[VALUES][1] + 1] + list(world[VALUES][2:])) #the second value +1 and the rest stays
    #DOOR
    if world[BOARD][newloc[1]][newloc[0]] == DOOR and world[VALUES][1] > 0:
        world[BOARD][loc[1]][loc[0]] = FREE
        loc = newloc
        world[BOARD][loc[1]][loc[0]] = ROBOT
        world[VALUES] = tuple([world[VALUES][0]] + [world[VALUES][1] - 1] + list(world[VALUES][2:])) #the second value +1 and the rest stays
    #BALL
    if oldworld[BOARD][newloc[1]][newloc[0]] == BALL:
        world[BOARD][loc[1]][loc[0]] = FREE
        loc = newloc
        world[BOARD][loc[1]][loc[0]] = ROBOT
        world[VALUES] = tuple([world[VALUES][0] + 1] + list(world[VALUES][1:])) #the first value +1 and the rest stays
    #BATTERY
    if world[BOARD][newloc[1]][newloc[0]] == BATTERY:
        world[BOARD][loc[1]][loc[0]] = FREE
        loc = newloc
        world[BOARD][loc[1]][loc[0]] = ROBOT
        world[VALUES] = tuple([world[VALUES][0] + 1] + list(world[VALUES][1:])) #the first value +1 and the rest stays
    #FOOD
    if world[BOARD][newloc[1]][newloc[0]] == FOOD:
        world[BOARD][loc[1]][loc[0]] = FREE
        loc = newloc
        world[BOARD][loc[1]][loc[0]] = ROBOT
        world[VALUES] = tuple([world[VALUES][0] + 1] + list(world[VALUES][1:])) #the first value +1 and the rest stays
        while True:
            x, y = (random.randint(0, width-1), random.randint(0, height-1))
            if world[BOARD][y][x] == FREE:
                world[BOARD][y][x] = FOOD
                break
    #FREE SPACE
    if world[BOARD][newloc[1]][newloc[0]] == FREE or world[BOARD][newloc[1]][newloc[0]] == BALL:
        world[BOARD][loc[1]][loc[0]] = FREE
        loc = newloc
        world[BOARD][loc[1]][loc[0]] = ROBOT
    return loc, [world[BOARD], world[VALUES], world[TIMES]]

actions = [left, right, up, down]
if isWorld5:
    actions = [up, down, left]

def motorbabbling():
    return random.choice(actions)

def prettyValue(value):
    if value == FREE:
        return "free"
    if value == FOOD:
        return "food"
    if value == TABLE:
        return "table"
    if value == CUP:
        return "cup"
    if value == ROBOT:
        return "robot"
    if value == WALL:
        return "wall"
    if value == KEY:
        return "key"
    if value == DOOR:
        return "door"
    if value == BATTERY:
        return "battery"
    if value == ARROW_UP:
        return "arrowup"
    if value == ARROW_DOWN:
        return "arrowdown"
    if value == BALL:
        return "ball"
    return value

def prettyVarValue(name, value):
    return f"<k_{value} --> {name}>"

def prettyTriplet(triplet):
    (y, x, value) = triplet[:3]
    value = prettyValue(value)
    if x == 0 and y == 0:
        return f"<(mid * {value}) --> shape>"
    if x == 1 and y == 0:
        return f"<(right * {value}) --> shape>"
    if x == -1 and y == 0:
        return f"<(left * {value}) --> shape>"
    if x == 0 and y == 1:
        return f"<(down * {value}) --> shape>"
    if x == 0 and y == -1:
        return f"<(up * {value}) --> shape>"
    return triplet

def prettyPrintRule(rule):
    actions_values_preconditions = rule[0]
    action = prettyaction(actions_values_preconditions[0])
    precons = actions_values_preconditions[2:]
    print("<(", end="")
    for i, x in enumerate(actions_values_preconditions[1]):
        name = "keys"
        print(f"{prettyVarValue(name, x)}", end="")
        print(f" &| ", end="")
    for i, x in enumerate(precons):
        print(f"{prettyTriplet(x)}", end="")
        if i != len(precons)-1:
            print(f" &| ", end="")
    scoreInc = f"<s_{rule[1][3][0]} --> scorePlus>"
    keys = f"<k_{rule[1][3][1]} --> keys>"
    print(") &/", action, "=/> (" + prettyTriplet(rule[1]) + " &| " + scoreInc + " &| " + keys + ")>.", TruthValue(RuleEvidence[rule]))

def OpRotate(op):
    if op == right:
        return down
    if op == down:
        return left
    if op == left:
        return up
    if op == up:
        return right

def ConditionRotate(cond):
    (y, x, v) = cond
    if y == 0 and x == -1: #left
        return (-1, 0, v)  #up
    if y == -1 and x == 0: #up
        return (0, 1, v)   #right
    if y == 0 and x == 1:  #right
        return (1, 0, v)   #down
    if y == 1 and x == 0:  #down
        return (0, -1, v)  #left
    if x == 0 and y == 0:
        return (0, 0, v)

def validCondition(cond):  #restrict to neighbours (CA assumption)
    (y, x, v) = cond
    if y == 0 and x == 0: #self
        return True
    if y == 0 and x == -1: #left
        return True
    if y == -1 and x == 0: #up
        return True
    if y == 0 and x == 1:  #right
        return True
    if y == 1 and x == 0:  #down
        return True
    if x == 0 and y == 0: #mid stays same
        return True
    return False

def ruleVariants(rule): #location symmetry (knowledge about movement operations for faster learning)
    action_values_precons = rule[0]
    conditions = action_values_precons[2:]
    action = action_values_precons[0]
    for (y,x,v) in conditions: #unnecessary
        if (action == left or action == right) and y != 0:
            return []
        if (action == up or action == down) and x != 0:
            return []
    rules = [rule]
    if action != left and action != right and action != down and action != up: #not such an op where symmetry would apply
        return rules
    conditionlist2 = sorted([ConditionRotate(x) for x in conditions])
    conditionlist3 = sorted([ConditionRotate(x) for x in conditionlist2])
    conditionlist4 = sorted([ConditionRotate(x) for x in conditionlist3])
    action2 = OpRotate(action)
    action3 = OpRotate(action2)
    action4 = OpRotate(action3)
    rules.append((tuple([action2, action_values_precons[1]] + conditionlist2), rule[1]))
    rules.append((tuple([action3, action_values_precons[1]] + conditionlist3), rule[1]))
    rules.append((tuple([action4, action_values_precons[1]] + conditionlist4), rule[1]))
    return rules

def AddRuleEvidence(RuleEvidence, rule, positive, w_max = 20):
    if rule not in RuleEvidence:
        RuleEvidence[rule] = (0, 0)
    (wp, wn) = RuleEvidence[rule]
    if positive:
        if wp + wn <= w_max:
            RuleEvidence[rule] = (wp+1, wn)
        else:
            RuleEvidence[rule] = (wp, max(0, wn-1))
    else:
        if wp + wn <= w_max:
            RuleEvidence[rule] = (wp, wn+1)
        else:
            RuleEvidence[rule] = (max(0, wp-1), wn)
    return RuleEvidence

def RemoveRule(RuleEvidence, ruleset, negruleset, rule):
    for r in ruleVariants(rule):
        RuleEvidence = AddRuleEvidence(RuleEvidence, rule, False)
        if "silent" not in sys.argv:
            print("Neg. revised: ", end="");  prettyPrintRule(rule)
        #in a deterministic setting this would have sufficed however
        #simply excluding rules does not work in non-deterministic ones
        #if rule in ruleset:
        #    print("RULE REMOVAL: ", end=""); prettyPrintRule(rule)
        #    ruleset.remove(rule)
        #negruleset.add(rule)
    return RuleEvidence, ruleset, negruleset

def TruthValue(wpn):
    (wp, wn) = wpn
    frequency = wp / (wp + wn)
    confidende = (wp + wn) / (wp + wn + 1)
    return (frequency, confidende)

def Truth_Expectation(tv):
    (f, c) = tv
    return (c * (f - 0.5) + 0.5)

def ChoiceRule(rule1, rule2):
    T1 = TruthValue(RuleEvidence[rule1])
    T2 = TruthValue(RuleEvidence[rule2])
    if Truth_Expectation(T1) > Truth_Expectation(T2):
        return rule1
    return rule2

def AddRule(RuleEvidence, ruleset, negruleset, rule): #try location symmetry
    variants = ruleVariants(rule)
    for rule in variants:
        RuleEvidence = AddRuleEvidence(RuleEvidence, rule, True)
        if "silent" not in sys.argv:
            print("Pos. revised: ", end="");  prettyPrintRule(rule)
        if rule not in negruleset:
            if rule not in ruleset:
                #print("RULE ADDITION: ", end=""); prettyPrintRule(rule)
                ruleset.add(rule)
    return RuleEvidence, ruleset

# APPLY MOVE TO THE REAL WORLD AND EXTRACT NEW RULES FROM THE OBSERVATIONS
def world_observe(RuleEvidence, worldchange, oldworld, action, newworld, oldrules, oldnegrules, predictedworld=None):
    newrules = deepcopy(oldrules)
    newnegrules = deepcopy(oldnegrules)
    robot_position, _ = get_robot_position(newworld)
    changesets = [set([]), set([])]
    for y, line in enumerate(newworld[BOARD]):
        for x, char in enumerate(line):
            if y < robot_position[0] - (VIEWDISTY - 1) or y > robot_position[0] + (VIEWDISTY - 1) or \
               x < robot_position[1] - (VIEWDISTX - 1) or x > robot_position[1] + (VIEWDISTX - 1):
                   continue
            if oldworld[BOARD][y][x] != newworld[BOARD][y][x]:
                changesets[0].add((y, x))
            if predictedworld and predictedworld[BOARD][y][x] != newworld[BOARD][y][x]:
                changesets[1].add((y, x))
    for changeset in changesets:
        for (y1_abs,x1_abs) in changeset:
            action_values_precondition = [action, oldworld[VALUES][1:]]
            preconditions = []
            for (y2_abs, x2_abs) in changeset:
                (y2_rel, x2_rel) = (y2_abs-y1_abs, x2_abs-x1_abs)
                condition = (y2_rel, x2_rel, oldworld[BOARD][y2_abs][x2_abs])
                if validCondition(condition):
                    preconditions.append(condition)
            preconditions = sorted(preconditions)
            for pr in preconditions:
                action_values_precondition.append(pr)
            rule = (tuple(action_values_precondition), (0, 0, newworld[BOARD][y1_abs][x1_abs], tuple([newworld[VALUES][0]-oldworld[VALUES][0]] + list(newworld[VALUES][1:]))))
            if len(preconditions) == 2:
                RuleEvidence, newrules = AddRule(RuleEvidence, newrules, newnegrules, rule)
        break #speedup
    #build a more specialized rule which has the precondition and conclusion corrected!
    (positionscores, highesthighscore) = rule_positionscores(oldworld, action, rules)
    for y in range(height):
        for x in range(width):
            if y < robot_position[0] - (VIEWDISTY - 1) or y > robot_position[0] + (VIEWDISTY - 1) or \
               x < robot_position[1] - (VIEWDISTX - 1) or x > robot_position[1] + (VIEWDISTX - 1):
                continue
            if (y,x) not in positionscores:
                continue
            scores, highscore = positionscores[(y,x)]
            for rule in oldrules:
                if ruleApplicable(scores, highscore, highesthighscore, rule):
                    if rule[1][2] != newworld[BOARD][y][x] and oldworld[BOARD][y][x] == newworld[BOARD][y][x] and rule in scores and scores[rule] == highesthighscore:
                        (precondition, consequence) = rule
                        action_score_and_preconditions = list(precondition)
                        values = action_score_and_preconditions[1]
                        corrected_preconditions = []
                        CONTINUE = False
                        has_condition_in_worldchange = False
                        has_robot_condition = False #TODO!!!
                        for (y_rel, x_rel, requiredstate) in action_score_and_preconditions[2:]:
                            if y+y_rel >= height or y+y_rel < 0 or x+x_rel >= width or x+x_rel < 0:
                                CONTINUE = True
                                break
                            if (y+y_rel, x+x_rel) in worldchange:
                                has_condition_in_worldchange = True
                            if oldworld[BOARD][y+y_rel][x+x_rel] == ROBOT:
                                has_robot_condition = True
                            corrected_preconditions.append((y_rel, x_rel, oldworld[BOARD][y+y_rel][x+x_rel]))
                        corrected_preconditions = sorted(corrected_preconditions)
                        if CONTINUE or not has_condition_in_worldchange or not has_robot_condition:
                            continue
                        rule_new = (tuple([action_score_and_preconditions[0], action_score_and_preconditions[1]]
                                   + corrected_preconditions), tuple([rule[1][0], rule[1][1], newworld[BOARD][y][x], tuple([newworld[VALUES][0]-oldworld[VALUES][0]] + list(newworld[VALUES][1:]))]))
                        if has_robot_condition:
                            #print("RULE CORRECTION ", y, x, loc, worldchange); prettyPrintRule(rule); prettyPrintRule(rule_new)
                            RuleEvidence, newrules = AddRule(RuleEvidence, newrules, newnegrules, rule_new)
                        break
    #CRISP MATCH: REMOVE CONTRADICTING RULES FROM RULE SET
    for y in range(height):
        for x in range(width):
            if y < robot_position[0] - (VIEWDISTY - 1) or y > robot_position[0] + (VIEWDISTY - 1) or \
               x < robot_position[1] - (VIEWDISTX - 1) or x > robot_position[1] + (VIEWDISTX - 1):
                continue
            for rule in oldrules: #find rules which don't work, and remove them adding them to newnegrules
                (precondition, consequence) = rule
                action_score_and_preconditions = list(precondition)
                values = action_score_and_preconditions[1]
                CONTINUE = False
                if action_score_and_preconditions[0] != action: #rule did not apply
                    continue
                for i in range(len(values)):
                    if values[i] != oldworld[VALUES][i+1]: #value didn't match, rule did not apply
                        CONTINUE = True
                        break
                for (y_rel, x_rel, requiredstate) in action_score_and_preconditions[2:]:
                    if y+y_rel >= height or y+y_rel < 0 or x+x_rel >= width or x+x_rel < 0:
                        CONTINUE = True
                        break
                    if oldworld[BOARD][y+y_rel][x+x_rel] != requiredstate: 
                        CONTINUE = True
                        break
                if CONTINUE:
                    continue
                if rule[1][3][0] != newworld[VALUES][0] - oldworld[VALUES][0]:
                    RuleEvidence, newrules, newnegrules = RemoveRule(RuleEvidence, newrules, newnegrules, rule) #score increase did not happen
                    continue
                for k in range(1, len(rule[1][3])): #wrong value prediction
                    if rule[1][3][k] != newworld[VALUES][k]:
                        RuleEvidence, newrules, newnegrules = RemoveRule(RuleEvidence, newrules, newnegrules, rule)
                        CONTINUE = True
                        break
                if CONTINUE:
                    continue
                if rule[1][2] != newworld[BOARD][y][x]:
                    RuleEvidence, newrules, newnegrules = RemoveRule(RuleEvidence, newrules, newnegrules, rule)
    worldchange = deepcopy(changesets[0])
    return RuleEvidence, worldchange, newrules, newnegrules

def rule_positionscores(oldworld, action, rules):
    positionscores = dict([])
    highesthighscore = 0.0
    robot_position, robotcnt = get_robot_position(oldworld)
    if not robot_position or robotcnt != 1: #OPTIONAL SPEEDUP HACK!
        return (positionscores, 0.0)
    for y in range(height):
        for x in range(width):
            if y < robot_position[0] - (VIEWDISTY - 1) or y > robot_position[0] + (VIEWDISTY - 1) or \
               x < robot_position[1] - (VIEWDISTX - 1) or x > robot_position[1] + (VIEWDISTX - 1):
                continue #DISABLES PREDICTION OUTSIDE OF VIEW RELATED TO PREDICTED POSITION OF ROBOT
            if robot_position and (abs(robot_position[0]-y) > 1 or abs(robot_position[1]-x) > 1): #OPTIONAL SPEEDUP HACK!
                continue
            scores = dict([])
            positionscores[(y,x)] = scores
            highscore = 0.0
            for rule in rules:
                (precondition, consequence) = rule
                action_score_and_preconditions = list(precondition)
                values = action_score_and_preconditions[1]
                if action_score_and_preconditions[0] == action:
                    scores[rule] = 0.0
                else:
                    continue
                CONTINUE = False
                for i in range(len(values)):
                    if values[i] != oldworld[VALUES][i+1]:
                        CONTINUE = True
                if CONTINUE:
                    continue
                for (y_rel, x_rel, requiredstate) in action_score_and_preconditions[2:]:
                    if y+y_rel >= height or y+y_rel < 0 or x+x_rel >= width or x+x_rel < 0:
                        CONTINUE = True
                        break
                    if oldworld[BOARD][y+y_rel][x+x_rel] == requiredstate:
                        scores[rule] += 1.0
                if CONTINUE:
                    continue
                scores[rule] /= (len(precondition)-2)
                if scores[rule] > 0.0 and scores[rule] > highscore:
                    highscore = scores.get(rule, 0.0)
            positionscores[(y,x)] = (scores, highscore)
            if highscore > highesthighscore:
                highesthighscore = highscore
    return (positionscores, highesthighscore)

def get_robot_position(world):
    robotcnt = 0
    robot_position = None
    for y in range(height):
        for x in range(width):
            if world[BOARD][y][x] == ROBOT:
                robot_position = (y, x)
                robotcnt += 1
    return robot_position, robotcnt

def ruleApplicable(scores, highscore, highesthighscore, rule):
    if highscore > 0.0 and scores.get(rule, 0.0) == highesthighscore:
        return True
    return False

# APPLY MOVE TO THE WORLD MODEL WHEREBY WE USE THE EXISTING RULES TO DECIDE HOW A GRID ELEMENT CHANGES
def world_predict(oldworld, action, rules, customGoal = None):
    newworld = deepcopy(oldworld)
    used_rules_sumscore = 0.0
    used_rules_amount = 0
    (positionscores, highesthighscore) = rule_positionscores(oldworld, action, rules)
    for y in range(height):
        for x in range(width):
            if (y,x) not in positionscores:
                continue
            scores, highscore = positionscores[(y,x)]
            for rule in rules:
                if ruleApplicable(scores, highscore, highesthighscore, rule):
                    if highscore == 1.0:
                        newworld[VALUES] = rule[1][3]
                    newworld[BOARD][y][x] = rule[1][2]
                    used_rules_sumscore += scores.get(rule, 0.0)
                    used_rules_amount += 1
    score = used_rules_sumscore/used_rules_amount if used_rules_amount > 0 else 1.0 #AIRIS confidence
    robot_position, _ = get_robot_position(newworld)
    age = 0
    if robot_position:
        age = (t - newworld[TIMES][robot_position[0]][robot_position[1]])
    #but if the predicted world has higher value, then set prediction score to the best it can be
    if (newworld[VALUES][0] == 1 and score == 1.0)  or (customGoal and customGoal(newworld)):
        score = float('-inf')
    return newworld, score, age 

def to_tuple(lst):
    return tuple(to_tuple(i) if isinstance(i, list) else i for i in lst)

# PLAN FORWARD SEARCHING FOR SITUATIONS OF HIGHEST UNCERTAINTY (TODO ALSO CONSIDER VALUE)
def max_depth__breadth_first_search(world, rules, actions, max_depth=100, max_queue_len=1000, customGoal = None):
    queue = deque([(world, [], 0)])  # Initialize queue with world state, empty action list, and depth 0
    encountered = dict([])
    best_score = float("inf")
    best_actions = []
    best_action_combination_for_revisit = []
    oldest_age = 0.0
    while queue:
        if len(queue) > max_queue_len:
            print("Planning queue bound enforced!")
            break
        current_world, planned_actions, depth = queue.popleft()  # Dequeue from the front
        if depth > max_depth:  # If maximum depth is reached, stop searching
            continue
        world_BOARD_VALUES = to_tuple([current_world[BOARD]]) #, current_world[VALUES][1:]]) #-- 1!!!
        if world_BOARD_VALUES in encountered and depth >= encountered[world_BOARD_VALUES]:
            continue
        if world_BOARD_VALUES not in encountered or depth < encountered[world_BOARD_VALUES]:
            encountered[world_BOARD_VALUES] = depth
        for action in actions:
            new_world, new_score, new_age = world_predict(deepcopy(current_world), action, rules, customGoal)
            new_planned_actions = planned_actions + [action]
            if new_score < best_score or (new_score == best_score and len(new_planned_actions) < len(best_actions)):
                best_actions = new_planned_actions
                best_score = new_score
            if new_age > oldest_age or (new_age == oldest_age and len(new_planned_actions) < len(best_action_combination_for_revisit)):
                best_action_combination_for_revisit = new_planned_actions
                oldest_age = new_age
            if new_score == 1.0:
                _, robot_cnt = get_robot_position(new_world)
                if robot_cnt == 1:
                    queue.append((new_world, new_planned_actions, depth + 1))  # Enqueue children at the end
    return best_actions, best_score, best_action_combination_for_revisit, oldest_age

# LET'S SIMULATE FOR 100 STEPS
def localObserve(observed_world, world):
    for y in range(VIEWDISTY*2+1):
        for x in range(VIEWDISTX*2+1):
            Y = loc[1]+y-VIEWDISTY
            X = loc[0]+x-VIEWDISTX
            if Y >= 0 and Y < height and \
               X >= 0 and X < width:
                observed_world[BOARD][Y][X] = world[BOARD][Y][X]
                observed_world[TIMES][Y][X] = t
    observed_world[VALUES] = deepcopy(world[VALUES])
    return observed_world

def prettyaction(action):
    M = {left: "^left", right: "^right", up: "^up", down: "^down"}
    return M[action]

def plan_prettystring(actionlist):
    return [prettyaction(x) for x in actionlist[1:]]

def cupIsOnTable(world):
    for x in range(width):
        for y in range(height-1):
            if world[BOARD][y+1][x] == 'T' and world[BOARD][y][x] == 'u':
                return True
    return False

def nace_step(RuleEvidence, worldchange, loc, observed_world, rulesin, negrules, oldworld):
    rulesExcluded = set([])
    rules = deepcopy(rulesin)
    for i, rule1 in enumerate(rulesin):
        if Truth_Expectation(TruthValue(RuleEvidence[rule1])) <= 0.5: #exclude rules which are not better than exp (only 0.5+ makes sense here)
            if rule1 in rules:
                rulesExcluded.add(rule1)
                rules.remove(rule1)
        for j, rule2 in enumerate(rulesin): #exclude rules which are worse by truth value
            if i != j:
                if rule1[0] == rule2[0]:
                    rulex = ChoiceRule(rule1, rule2)
                    if rulex == rule1:
                        if rule2 in rules:
                            rulesExcluded.add(rule2)
                            rules.remove(rule2)
                            #print("excluded ", end=''); prettyPrintRule(rule2)
                    else:
                        if rule1 in rules:
                            rulesExcluded.add(rule1)
                            rules.remove(rule1)
                            #print("excluded", end=''); prettyPrintRule(rule1)
    observed_world = localObserve(observed_world, oldworld)
    favoured_actions, airis_score, favoured_actions_for_revisit, oldest_age = max_depth__breadth_first_search(observed_world, rules, actions, customGoal = cupIsOnTable)
    debuginput = ""
    if "debug" in sys.argv:
        debuginput = input()
    print("\033[1;1H\033[2J")
    babble = random.random() > 1.0
    plan = []
    if airis_score >= 1.0 or babble or len(favoured_actions) == 0:
        if not babble and oldest_age > 0.0 and airis_score == 1.0 and len(favoured_actions_for_revisit) != 0:
            print("EXPLORE", plan_prettystring(favoured_actions_for_revisit), oldest_age)
            action = favoured_actions_for_revisit[0]
            plan = favoured_actions_for_revisit
        else:
            print("BABBLE", airis_score)
            action = motorbabbling()
    else:
        print("ACHIEVE" if airis_score == float("-inf") else "CURIOUS", plan_prettystring(favoured_actions), airis_score)#, rules)
        action = favoured_actions[0]
        plan = favoured_actions
    if debuginput == "w":
        action = up
    if debuginput == "s":
        action = down
    if debuginput == "a":
        action = left
    if debuginput == "d":
        action = right
    if debuginput == 'l':
        for x in rules:
            prettyPrintRule(x)
        input()
    loc, newworld = move(loc, deepcopy(oldworld), action)
    observed_world_old = deepcopy(observed_world)
    observed_world = localObserve(observed_world, newworld)
    predicted_world, _, __ = world_predict(deepcopy(observed_world_old), action, rules)
    print(f"\033[0mWorld t={t} beliefs={len(rules)}:\033[97;40m")
    printworld(newworld)
    print("\033[0mMental map:\033[97;44m")
    printworld(observed_world)
    print("\033[0mPredicted end:\033[97;41m")
    planworld = deepcopy(predicted_world)
    for i in range(1, len(plan)):
        planworld, _, __ = world_predict(deepcopy(planworld), plan[i], rules)
    printworld(planworld)
    print("\033[0m")
    RuleEvidence, worldchange, newrules, newnegrules = world_observe(RuleEvidence, worldchange, observed_world_old, action, observed_world, rules, negrules, predicted_world)
    for rule in rulesExcluded: #add again so we won't loose them
        newrules.add(rule)
    return RuleEvidence, worldchange, loc, observed_world, newrules, newnegrules, newworld, debuginput

loc = (2,4)
rules = set([])
negrules = set([])
worldchange = set([])
RuleEvidence = dict([])
observed_world = [[[" " for x in world[BOARD][i]] for i in range(len(world[BOARD]))], world[VALUES], world[TIMES]]
for t in range(300):
    start_time = time.time()
    RuleEvidence, worldchange, loc, observed_world, rules, negrules, world, debuginput = nace_step(RuleEvidence, worldchange, loc, observed_world, rules, negrules, deepcopy(world))
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
            printworld(predworld)
            print("score:", score)
            d = input()
            score = 0.0
            if d == 'q':
                break
            if d == 'r':
                predworld = deepcopy(world)
            if d == 'a':
                predworld, score, age = world_predict(deepcopy(predworld), left, rules)
            if d == 'd':
                predworld, score, age = world_predict(deepcopy(predworld), right, rules)
            if d == 'w':
                predworld, score, age = world_predict(deepcopy(predworld), up, rules)
            if d == 's':
                predworld, score, age = world_predict(deepcopy(predworld), down, rules)
            if d == 'l':
                for x in rules:
                    prettyPrintRule(x)
                input()
            if d == 'n':
                for x in negrules:
                    prettyPrintRule(x)
                input()
