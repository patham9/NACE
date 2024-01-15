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

from copy import deepcopy
from collections import deque
from hypothesis import *
from world import *
import sys

#Initializing the memory of the AI
FocusSet = dict([])
rules = set([])
negrules = set([])
worldchange = set([])
RuleEvidence = dict([])
observed_world = [[["." for x in world[BOARD][i]] for i in range(len(world[BOARD]))], world[VALUES], world[TIMES]]

#One observe-learn-plan-action cycle of the AI system
def NACE_Cycle(Time, FocusSet, RuleEvidence, loc, observed_world, rulesin, negrules, oldworld):
    rulesExcluded = set([])
    rules = deepcopy(rulesin)
    Hypothesis_BestSelection(rules, rulesExcluded, RuleEvidence, rulesin)
    observed_world = World_FieldOfView(Time, loc, observed_world, oldworld)
    if "manual" not in sys.argv:
        favoured_actions, airis_score, favoured_actions_for_revisit, oldest_age = _Plan(Time, observed_world, rules, actions, customGoal = World_CupIsOnTable)
    else:
        observed_world = [[["." for x in world[BOARD][i]] for i in range(len(world[BOARD]))], world[VALUES], world[TIMES]]
    debuginput = ""
    if "debug" in sys.argv or "manual" in sys.argv:
        debuginput = input()
    print("\033[1;1H\033[2J")
    if "manual" not in sys.argv:
        exploit_babble = random.random() > 1.0 #babbling when wanting to achieve something or curious about something, and babbling when exploring:
        explore_babble = random.random() > (0.9 if "DisableOpSymmetryAssumption" in sys.argv else 1.0) #since it might not know yet about all ops, exploring then can be limited
        plan = []
        if airis_score >= 1.0 or exploit_babble or len(favoured_actions) == 0:
            if not exploit_babble and not explore_babble and oldest_age > 0.0 and airis_score == 1.0 and len(favoured_actions_for_revisit) != 0:
                print("EXPLORE", Prettyprint_Plan(favoured_actions_for_revisit), "age:", oldest_age)
                action = favoured_actions_for_revisit[0]
                plan = favoured_actions_for_revisit
            else:
                print("BABBLE")
                action = random.choice(actions) #motorbabbling
        else:
            print("ACHIEVE" if airis_score == float("-inf") else "CURIOUS", Prettyprint_Plan(favoured_actions), end=" "); NACE_PrintScore(airis_score)
            action = favoured_actions[0]
            plan = favoured_actions
    else:
        action = up
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
    show_plansteps = debuginput == 'p'
    loc, newworld = World_Move(loc, deepcopy(oldworld), action)
    observed_world_old = deepcopy(observed_world)
    observed_world = World_FieldOfView(Time, loc, observed_world, newworld)
    predicted_world, _, __, values = NACE_Predict(Time, FocusSet, deepcopy(observed_world_old), action, rules)
    if "manual" not in sys.argv:
        print(f"\033[0mWorld t={Time} beliefs={len(rules)}:\033[97;40m")
        World_Print(newworld)
        print("\033[0mMental map:\033[97;44m")
    else:
        print("\033[0mObserved map:\033[97;45m")
    World_Print(observed_world)
    if "manual" not in sys.argv:
        print("\033[0mPredicted end:\033[97;41m")
        planworld = deepcopy(predicted_world)
        for i in range(1, len(plan)):
            planworld, _, __, ___ = NACE_Predict(Time, FocusSet, deepcopy(planworld), plan[i], rules)
            if show_plansteps:
                World_Print(planworld)
        if not show_plansteps:
            World_Print(planworld)
    print("\033[0m")
    if "manual" not in sys.argv:
        FocusSet, RuleEvidence, newrules, newnegrules = _Observe(Time, FocusSet, RuleEvidence, observed_world_old, action, observed_world, rules, negrules, predicted_world)
        usedRules = deepcopy(newrules)
        for rule in rulesExcluded: #add again so we won't loose them
            newrules.add(rule)
    else:
        usedRules = newrules = newnegrules = rules
    return usedRules, FocusSet, RuleEvidence, loc, observed_world, newrules, newnegrules, newworld, debuginput, values

# Apply move to the predicted world model whereby we use the learned tules to decide how grid elements might change most likely
def NACE_Predict(Time, FocusSet, oldworld, action, rules, customGoal = None):
    newworld = deepcopy(oldworld)
    used_rules_sumscore = 0.0
    used_rules_amount = 0
    (positionscores, highesthighscore) = _MatchHypotheses(FocusSet, oldworld, action, rules)
    max_focus = None
    if len(FocusSet) > 0:
        max_focus = max(FocusSet, key=lambda k: FocusSet[k])
    age = 0
    for y in range(height):
        for x in range(width):
            if (y,x) not in positionscores:
                continue
            if max_focus and oldworld[BOARD][y][x] in FocusSet and oldworld[BOARD][y][x] == max_focus:
                age = max(age, (Time - newworld[TIMES][y][x]))
            scores, highscore, rule = positionscores[(y,x)]
            #for rule in rules:
            if _RuleApplicable(scores, highscore, highesthighscore, rule):
                if highscore == 1.0:
                    newworld[VALUES] = rule[1][3]
                newworld[BOARD][y][x] = rule[1][2]
                used_rules_sumscore += scores.get(rule, 0.0)
                used_rules_amount += 1
    score = used_rules_sumscore/used_rules_amount if used_rules_amount > 0 else 1.0 #AIRIS confidence
    #but if the predicted world has higher value, then set prediction score to the best it can be
    if (newworld[VALUES][0] == 1 and score == 1.0)  or (customGoal and customGoal(newworld)):
        score = float('-inf')
    return newworld, score, age, newworld[VALUES]

# Plan forward searching for situations of highest reward and if there is no such, then for biggest AIRIS uncertainty (max depth & max queue size obeying breadth first search)
def _Plan(Time, world, rules, actions, max_depth=100, max_queue_len=1000, customGoal = None):
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
        world_BOARD_VALUES = World_AsTuple([current_world[BOARD], current_world[VALUES][1:]])
        if world_BOARD_VALUES in encountered and depth >= encountered[world_BOARD_VALUES]:
            continue
        if world_BOARD_VALUES not in encountered or depth < encountered[world_BOARD_VALUES]:
            encountered[world_BOARD_VALUES] = depth
        for action in actions:
            new_world, new_score, new_age, _ = NACE_Predict(Time, FocusSet, deepcopy(current_world), action, rules, customGoal)
            new_Planned_actions = planned_actions + [action]
            if new_score < best_score or (new_score == best_score and len(new_Planned_actions) < len(best_actions)):
                best_actions = new_Planned_actions
                best_score = new_score
            if new_age > oldest_age or (new_age == oldest_age and len(new_Planned_actions) < len(best_action_combination_for_revisit)):
                best_action_combination_for_revisit = new_Planned_actions
                oldest_age = new_age
            if new_score == 1.0:
                queue.append((new_world, new_Planned_actions, depth + 1))  # Enqueue children at the end
    return best_actions, best_score, best_action_combination_for_revisit, oldest_age

#Whether the grid cell has been observed now (not all have been, due to partial observability)
def _IsPresentlyObserved(Time, world, y, x):
    return Time - world[TIMES][y][x] == 0

#Extract new rules from the observations by looking only for observed changes and prediction-observation mismatches
def _Observe(Time, FocusSet, RuleEvidence, oldworld, action, newworld, oldrules, oldnegrules, predictedworld=None):
    newrules = deepcopy(oldrules)
    newnegrules = deepcopy(oldnegrules)
    changesets = [set([]), set([])]
    valuecount = dict([])
    for y in range(height):
        for x in range(width):
            val = oldworld[BOARD][y][x]
            if val not in valuecount:
                valuecount[val] = 1
            else:
                valuecount[val] += 1
    for y in range(height):
        for x in range(width):
            if not _IsPresentlyObserved(Time, newworld, y, x):
                continue
            if oldworld[BOARD][y][x] != newworld[BOARD][y][x]:
                changesets[0].add((y, x))
                val = oldworld[BOARD][y][x]
                if valuecount[val] == 1: #unique
                    if val not in FocusSet:
                        FocusSet[val] = 1
                    else:
                        FocusSet[val] += 1
            if predictedworld and predictedworld[BOARD][y][x] != newworld[BOARD][y][x]:
                changesets[1].add((y, x))
    if len(changesets[0]) == 1 and newworld[VALUES] != oldworld[VALUES]: #if we moved to an element and a value changed (TODO, egg example)
        (y,x) = list(changesets[0])[0]
        if action == right and x>0 and newworld[BOARD][y][x-1] in FocusSet and newworld[BOARD][y][x-1] == oldworld[BOARD][y][x-1]:
            changesets[0].add((y,x-1))
        if action == left and x<width-1 and newworld[BOARD][y][x+1] in FocusSet and newworld[BOARD][y][x+1] == oldworld[BOARD][y][x+1]:
            changesets[0].add((y,x+1))
        if action == down and y>0 and newworld[BOARD][y-1][x] in FocusSet and newworld[BOARD][y-1][x] == oldworld[BOARD][y-1][x]:
            changesets[0].add((y-1,x))
        if action == up and y<height-1 and newworld[BOARD][y+1][x] in FocusSet and newworld[BOARD][y+1][x] == oldworld[BOARD][y+1][x]:
            changesets[0].add((y+1,x))
    #Build rules based on changes and prediction-observation mismatches
    for changeset in changesets:
        for (y1_abs,x1_abs) in changeset:
            action_values_precondition = [action, oldworld[VALUES][1:]]
            preconditions = []
            midstate = None
            CONTINUE = False
            for (y2_abs, x2_abs) in changeset:
                (y2_rel, x2_rel) = (y2_abs-y1_abs, x2_abs-x1_abs)
                condition = (y2_rel, x2_rel, oldworld[BOARD][y2_abs][x2_abs])
                if Hypothesis_ValidCondition(condition):
                    preconditions.append(condition)
                    if y2_rel == 0 and x2_rel == 0:
                        if oldworld[BOARD][y2_abs][x2_abs] == newworld[BOARD][y1_abs][x1_abs]:
                            CONTINUE = True
                            break
            if CONTINUE:
                continue
            preconditions = sorted(preconditions)
            for pr in preconditions:
                action_values_precondition.append(pr)
            rule = (tuple(action_values_precondition), (0, 0, newworld[BOARD][y1_abs][x1_abs], tuple([newworld[VALUES][0]-oldworld[VALUES][0]] + list(newworld[VALUES][1:]))))
            if len(preconditions) >= 2:
                RuleEvidence, newrules = Hypothesis_Confirmed(FocusSet, RuleEvidence, newrules, newnegrules, rule)
        break #speedup
    #if rule conditions are only partly met or the predicted outcome is different than observed, build a specialized rule which has the precondition and conclusion corrected!
    (positionscores, highesthighscore) = _MatchHypotheses(FocusSet, oldworld, action, newrules)
    for y in range(height):
        for x in range(width):
            if (y,x) not in positionscores:
                continue
            if not _IsPresentlyObserved(Time, newworld, y, x):
                continue
            scores, highscore, rule = positionscores[(y,x)]
            #for rule in oldrules:
            if _RuleApplicable(scores, highscore, highesthighscore, rule):
                if rule[1][2] != newworld[BOARD][y][x] and rule in scores and scores[rule] == highesthighscore:
                    (precondition, consequence) = rule
                    action_score_and_preconditions = list(precondition)
                    values = action_score_and_preconditions[1]
                    corrected_preconditions = []
                    CONTINUE = False
                    has_focus_set_condition = False #TODO!!!
                    for (y_rel, x_rel, requiredstate) in action_score_and_preconditions[2:]:
                        if y+y_rel >= height or y+y_rel < 0 or x+x_rel >= width or x+x_rel < 0:
                            CONTINUE = True
                            break
                        if oldworld[BOARD][y+y_rel][x+x_rel] in FocusSet:
                            has_focus_set_condition = True
                        corrected_preconditions.append((y_rel, x_rel, oldworld[BOARD][y+y_rel][x+x_rel]))
                    corrected_preconditions = sorted(corrected_preconditions)
                    if CONTINUE or not has_focus_set_condition:
                        continue
                    rule_new = (tuple([action_score_and_preconditions[0], action_score_and_preconditions[1]]
                               + corrected_preconditions), tuple([rule[1][0], rule[1][1], newworld[BOARD][y][x], tuple([newworld[VALUES][0]-oldworld[VALUES][0]] + list(newworld[VALUES][1:]))]))
                    #print("RULE CORRECTION ", y, x, loc, worldchange); Prettyprint_rule(rule); Prettyprint_rule(rule_new)
                    RuleEvidence, newrules = Hypothesis_Confirmed(FocusSet, RuleEvidence, newrules, newnegrules, rule_new)
                    break
    #Crisp match: Add negative evidence for rules which prediction contradicts observation (in a classical AIRIS implementation restricted to deterministic worlds: this part would remove contradicting rules from the rule set and would ensure they can't be re-induced)
    for y in range(height):
        for x in range(width):
            if not _IsPresentlyObserved(Time, newworld, y, x):
                continue
            for rule in oldrules: #find rules which don't work, and add negative evidence for them (classical AIRIS: remove them and add them to newnegrules)
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
    return FocusSet, RuleEvidence, newrules, newnegrules

#Match hypotheses (rules) preconditions to the world, calculating how AIRIS-confident the prediction would be:
def _MatchHypotheses(FocusSet, oldworld, action, rules):
    positionscores = dict([])
    highesthighscore = 0.0
    AttendPositions = set([])
    for y in range(height):
        for x in range(width):
            if oldworld[BOARD][y][x] in FocusSet:
                AttendPositions.add((y,x))
                for rule in rules:
                    (precondition, consequence) = rule
                    action_score_and_preconditions = list(precondition)
                    for (y_rel, x_rel, requiredstate) in action_score_and_preconditions[2:]:
                        AttendPositions.add((y+y_rel, x+x_rel))
    for y in range(height):
        for x in range(width):
            if (y,x) not in AttendPositions:
                continue
            scores = dict([])
            positionscores[(y,x)] = scores
            highscore = 0.0
            highscorerule = None
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
                if scores[rule] > 0.0 and scores[rule] > highscore or (scores[rule] == highscore and highscorerule is not None and len(rule[0]) > len(highscorerule[0])):
                    highscore = scores.get(rule, 0.0)
                    highscorerule = rule
            positionscores[(y,x)] = (scores, highscore, highscorerule)
            if highscore > highesthighscore:
                highesthighscore = highscore
    return (positionscores, highesthighscore)

#Whether a rule is applicable: only if it matches better than not at all, and as well as the best matching rule
def _RuleApplicable(scores, highscore, highesthighscore, rule):
    if highscore > 0.0 and scores.get(rule, 0.0) == highesthighscore:
        return True
    return False

#Print score value taking its semantics regarding its value range semantics for planning into account
def NACE_PrintScore(score):
    if score >= 0.0 and score <= 1.0:
        print("certainty:", score)
    else:
        print("desired: True")
