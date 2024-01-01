from copy import deepcopy
from collections import deque
from hypothesis import *
from world import *
import sys

if "NoMovementOpAssumptions" not in sys.argv: #if we want the system to exploit assumptions about space (the default)
    Hypothesis_UseMovementOpAssumptions(left, right, up, down)

rules = set([])
negrules = set([])
worldchange = set([])
RuleEvidence = dict([])
observed_world = [[[" " for x in world[BOARD][i]] for i in range(len(world[BOARD]))], world[VALUES], world[TIMES]]

def NACE_Cycle(Time, RuleEvidence, worldchange, loc, observed_world, rulesin, negrules, oldworld):
    rulesExcluded = set([])
    rules = deepcopy(rulesin)
    for i, rule1 in enumerate(rulesin):
        if Hypothesis_TruthExpectation(Hypothesis_TruthValue(RuleEvidence[rule1])) <= 0.5: #exclude rules which are not better than exp (only 0.5+ makes sense here)
            if rule1 in rules:
                rulesExcluded.add(rule1)
                rules.reWorld_Move(rule1)
        for j, rule2 in enumerate(rulesin): #exclude rules which are worse by truth value
            if i != j:
                if rule1[0] == rule2[0]:
                    rulex = Hypothesis_Choice(rule1, rule2)
                    if rulex == rule1:
                        if rule2 in rules:
                            rulesExcluded.add(rule2)
                            rules.reWorld_Move(rule2)
                            #print("excluded ", end=''); Prettyprint_rule(rule2)
                    else:
                        if rule1 in rules:
                            rulesExcluded.add(rule1)
                            rules.reWorld_Move(rule1)
                            #print("excluded", end=''); Prettyprint_rule(rule1)
    observed_world = World_FieldOfView(Time, loc, observed_world, oldworld)
    favoured_actions, airis_score, favoured_actions_for_revisit, oldest_age = _plan(Time, observed_world, rules, actions, customGoal = World_CupIsOnTable)
    debuginput = ""
    if "debug" in sys.argv:
        debuginput = input()
    print("\033[1;1H\033[2J")
    babble = random.random() > 1.0
    plan = []
    if airis_score >= 1.0 or babble or len(favoured_actions) == 0:
        if not babble and oldest_age > 0.0 and airis_score == 1.0 and len(favoured_actions_for_revisit) != 0:
            print("EXPLORE", Prettyprint_plan(favoured_actions_for_revisit), oldest_age)
            action = favoured_actions_for_revisit[0]
            plan = favoured_actions_for_revisit
        else:
            print("BABBLE", airis_score)
            action = random.choice(actions) #motorbabbling
    else:
        print("ACHIEVE" if airis_score == float("-inf") else "CURIOUS", Prettyprint_plan(favoured_actions), airis_score)#, rules)
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
            Prettyprint_rule(RuleEvidence, Hypothesis_TruthValue, x)
        input()
    loc, newworld = World_Move(loc, deepcopy(oldworld), action)
    observed_world_old = deepcopy(observed_world)
    observed_world = World_FieldOfView(Time, loc, observed_world, newworld)
    predicted_world, _, __ = _predict(Time, deepcopy(observed_world_old), action, rules)
    print(f"\033[0mWorld t={Time} beliefs={len(rules)}:\033[97;40m")
    World_Print(newworld)
    print("\033[0mMental map:\033[97;44m")
    World_Print(observed_world)
    print("\033[0mPredicted end:\033[97;41m")
    planworld = deepcopy(predicted_world)
    for i in range(1, len(plan)):
        planworld, _, __ = _predict(Time, deepcopy(planworld), plan[i], rules)
    World_Print(planworld)
    print("\033[0m")
    RuleEvidence, worldchange, newrules, newnegrules = _observe(RuleEvidence, worldchange, observed_world_old, action, observed_world, rules, negrules, predicted_world)
    for rule in rulesExcluded: #add again so we won't loose them
        newrules.add(rule)
    return RuleEvidence, worldchange, loc, observed_world, newrules, newnegrules, newworld, debuginput

# PLAN FORWARD SEARCHING FOR SITUATIONS OF HIGHEST UNCERTAINTY (max depth & max queue size obeying breadth first search)
def _plan(Time, world, rules, actions, max_depth=100, max_queue_len=1000, customGoal = None):
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
        world_BOARD_VALUES = World_AsTuple([current_world[BOARD]]) #, current_world[VALUES][1:]]) #-- 1!!!
        if world_BOARD_VALUES in encountered and depth >= encountered[world_BOARD_VALUES]:
            continue
        if world_BOARD_VALUES not in encountered or depth < encountered[world_BOARD_VALUES]:
            encountered[world_BOARD_VALUES] = depth
        for action in actions:
            new_world, new_score, new_age = _predict(Time, deepcopy(current_world), action, rules, customGoal)
            new_planned_actions = planned_actions + [action]
            if new_score < best_score or (new_score == best_score and len(new_planned_actions) < len(best_actions)):
                best_actions = new_planned_actions
                best_score = new_score
            if new_age > oldest_age or (new_age == oldest_age and len(new_planned_actions) < len(best_action_combination_for_revisit)):
                best_action_combination_for_revisit = new_planned_actions
                oldest_age = new_age
            if new_score == 1.0:
                _, robot_cnt = World_GetRobotPosition(new_world)
                if robot_cnt == 1:
                    queue.append((new_world, new_planned_actions, depth + 1))  # Enqueue children at the end
    return best_actions, best_score, best_action_combination_for_revisit, oldest_age

# APPLY MOVE TO THE WORLD MODEL WHEREBY WE USE THE EXISTING RULES TO DECIDE HOW A GRID ELEMENT CHANGES
def _predict(Time, oldworld, action, rules, customGoal = None):
    newworld = deepcopy(oldworld)
    used_rules_sumscore = 0.0
    used_rules_amount = 0
    (positionscores, highesthighscore) = _matchHypotheses(oldworld, action, rules)
    for y in range(height):
        for x in range(width):
            if (y,x) not in positionscores:
                continue
            scores, highscore = positionscores[(y,x)]
            for rule in rules:
                if _ruleApplicable(scores, highscore, highesthighscore, rule):
                    if highscore == 1.0:
                        newworld[VALUES] = rule[1][3]
                    newworld[BOARD][y][x] = rule[1][2]
                    used_rules_sumscore += scores.get(rule, 0.0)
                    used_rules_amount += 1
    score = used_rules_sumscore/used_rules_amount if used_rules_amount > 0 else 1.0 #AIRIS confidence
    robot_position, _ = World_GetRobotPosition(newworld)
    age = 0
    if robot_position:
        age = (Time - newworld[TIMES][robot_position[0]][robot_position[1]])
    #but if the predicted world has higher value, then set prediction score to the best it can be
    if (newworld[VALUES][0] == 1 and score == 1.0)  or (customGoal and customGoal(newworld)):
        score = float('-inf')
    return newworld, score, age 

# EXTRACT NEW RULES FROM THE OBSERVATIONS
def _observe(RuleEvidence, worldchange, oldworld, action, newworld, oldrules, oldnegrules, predictedworld=None):
    newrules = deepcopy(oldrules)
    newnegrules = deepcopy(oldnegrules)
    robot_position, _ = World_GetRobotPosition(newworld)
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
                if Hypothesis_ValidCondition(condition):
                    preconditions.append(condition)
            preconditions = sorted(preconditions)
            for pr in preconditions:
                action_values_precondition.append(pr)
            rule = (tuple(action_values_precondition), (0, 0, newworld[BOARD][y1_abs][x1_abs], tuple([newworld[VALUES][0]-oldworld[VALUES][0]] + list(newworld[VALUES][1:]))))
            if len(preconditions) == 2:
                RuleEvidence, newrules = Hypothesis_Confirmed(RuleEvidence, newrules, newnegrules, rule)
        break #speedup
    #build a more specialized rule which has the precondition and conclusion corrected!
    (positionscores, highesthighscore) = _matchHypotheses(oldworld, action, newrules)
    for y in range(height):
        for x in range(width):
            if y < robot_position[0] - (VIEWDISTY - 1) or y > robot_position[0] + (VIEWDISTY - 1) or \
               x < robot_position[1] - (VIEWDISTX - 1) or x > robot_position[1] + (VIEWDISTX - 1):
                continue
            if (y,x) not in positionscores:
                continue
            scores, highscore = positionscores[(y,x)]
            for rule in oldrules:
                if _ruleApplicable(scores, highscore, highesthighscore, rule):
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
                            #print("RULE CORRECTION ", y, x, loc, worldchange); Prettyprint_rule(rule); Prettyprint_rule(rule_new)
                            RuleEvidence, newrules = Hypothesis_Confirmed(RuleEvidence, newrules, newnegrules, rule_new)
                        break
    #CRISP MATCH: REMOVE CONTRADICTING RULES FROM RULE SET
    for y in range(height):
        for x in range(width):
            if y < robot_position[0] - (VIEWDISTY - 1) or y > robot_position[0] + (VIEWDISTY - 1) or \
               x < robot_position[1] - (VIEWDISTX - 1) or x > robot_position[1] + (VIEWDISTX - 1):
                continue
            for rule in oldrules: #find rules which don't work, and reWorld_Move them adding them to newnegrules
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
                    RuleEvidence, newrules, newnegrules = Hypothesis_Contradicted(RuleEvidence, newrules, newnegrules, rule) #score increase did not happen
                    continue
                for k in range(1, len(rule[1][3])): #wrong value prediction
                    if rule[1][3][k] != newworld[VALUES][k]:
                        RuleEvidence, newrules, newnegrules = Hypothesis_Contradicted(RuleEvidence, newrules, newnegrules, rule)
                        CONTINUE = True
                        break
                if CONTINUE:
                    continue
                if rule[1][2] != newworld[BOARD][y][x]:
                    RuleEvidence, newrules, newnegrules = Hypothesis_Contradicted(RuleEvidence, newrules, newnegrules, rule)
    worldchange = deepcopy(changesets[0])
    return RuleEvidence, worldchange, newrules, newnegrules

def _matchHypotheses(oldworld, action, rules):
    positionscores = dict([])
    highesthighscore = 0.0
    robot_position, robotcnt = World_GetRobotPosition(oldworld)
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

def _ruleApplicable(scores, highscore, highesthighscore, rule):
    if highscore > 0.0 and scores.get(rule, 0.0) == highesthighscore:
        return True
    return False
