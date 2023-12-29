from copy import deepcopy
from environment import WorldNode, Action, VIEWDISTX, VIEWDISTY, ROBOT
from typing import List, Tuple
from learner import Rule
from learner.Rule import validCondition, AddRule, RemoveRule, prettyPrintRule
from collections import deque
from nal import Truth_Expectation, TruthValue, RuleEvidence, ChoiceRule, prettyaction
import numpy as np
import sys
import random

def rule_positionscores(oldworld: WorldNode, action: Action, rules: List[Rule]):
    position_scores = dict([])
    highest_high_score = 0.0

    # robot_position, robotcnt = get_robot_position(oldworld)
    # if not robot_position or robotcnt != 1: #OPTIONAL SPEEDUP HACK!
    #     return (positionscores, 0.0)
    # TODO: Isn't there only one robot?

    robot_position = oldworld.loc_robot
    height, width = oldworld.height, oldworld.width
    for y in range(height):
        for x in range(width):
            if y < robot_position[0] - (VIEWDISTY - 1) or y > robot_position[0] + (VIEWDISTY - 1) or \
               x < robot_position[1] - (VIEWDISTX - 1) or x > robot_position[1] + (VIEWDISTX - 1):
                continue  # DISABLES PREDICTION OUTSIDE OF VIEW RELATED TO PREDICTED POSITION OF ROBOT
            # OPTIONAL SPEEDUP HACK!
            if robot_position and (abs(robot_position[0]-y) > 1 or abs(robot_position[1]-x) > 1):
                continue
            scores = dict([])

            position_scores[(y, x)] = scores
            high_score = 0.0

            for rule in rules:
                (precondition, consequence) = rule
                # precondition is a list, composed of action, values, and conditions
                precondition: Tuple[Action, Tuple[int, ...],
                                    Tuple[int, int, str], Tuple[int, int, str]]

                action_score_and_preconditions = list(precondition)
                values = action_score_and_preconditions[1]
                # 1. action must match
                if action_score_and_preconditions[0] == action:
                    scores[rule] = 0.0
                else:
                    continue
                CONTINUE = False
                # 2. values must match
                for i in range(len(values)):
                    if values[i] != oldworld.values[i+1]:
                        CONTINUE = True
                        print("VALUE MISMATCH", values[i], oldworld.values[i+1])
                if CONTINUE:
                    continue
                # 3. conditions must match
                for (y_rel, x_rel, requiredstate) in action_score_and_preconditions[2:]:
                    if y+y_rel >= height or y+y_rel < 0 or x+x_rel >= width or x+x_rel < 0:
                        CONTINUE = True
                        print("OUT OF BOUNDS", y+y_rel, x+x_rel)
                        break
                    if oldworld.board[y+y_rel][x+x_rel] == requiredstate:
                        scores[rule] += 1.0
                if CONTINUE:
                    continue
                scores[rule] /= (len(precondition)-2)
                if scores[rule] > 0.0 and scores[rule] > high_score:
                    high_score = scores.get(rule, 0.0)

            position_scores[(y, x)] = (scores, high_score)

    highest_high_score = max((score for _, score in position_scores.values()))

    return (position_scores, highest_high_score)


def ruleApplicable(scores, high_score, highest_high_score, rule):
    if high_score > 0.0 and scores.get(rule, 0.0) == highest_high_score:
        return True
    return False

def to_tuple(lst):
    return tuple(to_tuple(i) if isinstance(i, list) else i for i in lst)


def plan_prettystring(actionlist):
    return [prettyaction(x) for x in actionlist[1:]]


class Learner:
    worldchange = set()

    def __init__(self) -> None:
        """"""
        self.rules = set()
        self.negrules = set()


    def world_observe(self, oldworld: WorldNode, action: Action, newworld: WorldNode, oldrules, oldnegrules, predictedworld: WorldNode = None):
        """APPLY MOVE TO THE REAL WORLD AND EXTRACT NEW RULES FROM THE OBSERVATIONS"""
        worldchange = Learner.worldchange
        newrules = deepcopy(oldrules)
        newnegrules = deepcopy(oldnegrules)

        robot_position = newworld.loc_robot

        # 0: positions where the new world and the old world are different;
        # 1: positions where the new world and the predicted world are different;
        change_sets = [set(), set()]

        ''' Get difference between the old world and the new world, as well as the difference between the predicted world and the new world
        '''
        obs_new = newworld.observe()
        obs_old = oldworld.observe()
        obs_pred = predictedworld.observe() if predictedworld else None
        y_robot, x_robot = robot_position
        for y_rel, y in enumerate(range(y_robot-(obs_new.shape[0]-1)//2, y_robot-(obs_new.shape[0]+1)//2)):
            for x_rel, x in enumerate(range(x_robot-(obs_new.shape[1]-1)//2, x_robot-(obs_new.shape[1]+1)//2)):
                if obs_new[y_rel, x_rel] != obs_old[y_rel, x_rel]:
                    change_sets[0].add((y, x))
                if obs_pred and obs_pred[y_rel, x_rel] != obs_old[y_rel, x_rel]:
                    change_sets[1].add((y, x))

        ''' Build new rules from the changes
        '''
        for change_set in change_sets: # Why use a for-loop? It breaks after the first iteration anyway.
            for (y1_abs, x1_abs) in change_set:
                action_values_precondition = [action, oldworld.values[1:]]
                preconditions = []
                for (y2_abs, x2_abs) in change_set:
                    (y2_rel, x2_rel) = (y2_abs-y1_abs, x2_abs-x1_abs)
                    condition = (y2_rel, x2_rel,
                                 oldworld.board[y2_abs][x2_abs])
                    if validCondition(condition):
                        preconditions.append(condition)
                preconditions = sorted(preconditions)
                for pr in preconditions:
                    action_values_precondition.append(pr)

                if len(preconditions) == 2:
                    rule = Rule(
                        action,
                        oldworld.values[1:],
                        preconditions,
                        (0, 0, newworld.board[y1_abs][x1_abs],
                            tuple(
                            newworld.values[0]-oldworld.values[0],
                            *newworld.values[1:]
                        )))
                    AddRule(newrules, newnegrules, rule)
            break  # speedup

        # build a more specialized rule which has the precondition and conclusion corrected!
        (position_scores, highest_high_score) = rule_positionscores(
            oldworld, action, self.rules)
        
        height, width = oldworld.height, oldworld.width
        for y in range(height):
            for x in range(width):
                if y < robot_position[0] - (VIEWDISTY - 1) or y > robot_position[0] + (VIEWDISTY - 1) or \
                        x < robot_position[1] - (VIEWDISTX - 1) or x > robot_position[1] + (VIEWDISTX - 1):
                    continue
                if (y, x) not in position_scores:
                    continue
                scores, highscore = position_scores[(y, x)]
                for rule in oldrules:
                    rule: Rule
                    if ruleApplicable(scores, highscore, highest_high_score, rule):
                        if rule.consequence[2] != newworld.board[y, x] and oldworld.board[y, x] == newworld.board[y, x] and rule in scores and scores[rule] == highest_high_score:
                            (precondition, consequence) = rule
                            action_score_and_preconditions = list(precondition)
                            values = action_score_and_preconditions[1]
                            corrected_preconditions = []
                            CONTINUE = False
                            has_condition_in_worldchange = False
                            has_robot_condition = False  # TODO!!!
                            for (y_rel, x_rel, requiredstate) in action_score_and_preconditions[2:]:
                                if y+y_rel >= height or y+y_rel < 0 or x+x_rel >= width or x+x_rel < 0:
                                    CONTINUE = True
                                    break
                                if (y+y_rel, x+x_rel) in worldchange:
                                    has_condition_in_worldchange = True
                                if oldworld.board[y+y_rel, x+x_rel] == ROBOT:
                                    has_robot_condition = True
                                corrected_preconditions.append(
                                    (y_rel, x_rel, oldworld.board[y+y_rel][x+x_rel]))
                            corrected_preconditions = sorted(
                                corrected_preconditions)
                            if CONTINUE or not has_condition_in_worldchange or not has_robot_condition:
                                continue
                            rule_new = (tuple([action_score_and_preconditions[0], action_score_and_preconditions[1]]
                                              + corrected_preconditions), tuple([rule.consequence[0], rule.consequence[1], newworld.board[y][x], tuple([newworld.values[0]-oldworld.values[0]] + list(newworld.values[1:]))]))
                            if has_robot_condition:
                                # print("RULE CORRECTION ", y, x, loc, worldchange); prettyPrintRule(rule); prettyPrintRule(rule_new)
                                AddRule(newrules, newnegrules, rule_new)
                            break
        # CRISP MATCH: REMOVE CONTRADICTING RULES FROM RULE SET
        for y in range(height):
            for x in range(width):
                if y < robot_position[0] - (VIEWDISTY - 1) or y > robot_position[0] + (VIEWDISTY - 1) or \
                        x < robot_position[1] - (VIEWDISTX - 1) or x > robot_position[1] + (VIEWDISTX - 1):
                    continue
                for rule in oldrules:  # find rules which don't work, and remove them adding them to newnegrules
                    (precondition, consequence) = rule
                    action_score_and_preconditions = list(precondition)
                    values = action_score_and_preconditions[1]
                    CONTINUE = False
                    # rule did not apply
                    if action_score_and_preconditions[0] != action:
                        continue
                    for i in range(len(values)):
                        # value didn't match, rule did not apply
                        if values[i] != oldworld.values[i+1]:
                            CONTINUE = True
                            break
                    for (y_rel, x_rel, requiredstate) in action_score_and_preconditions[2:]:
                        if y+y_rel >= height or y+y_rel < 0 or x+x_rel >= width or x+x_rel < 0:
                            CONTINUE = True
                            break
                        if oldworld.board[y+y_rel][x+x_rel] != requiredstate:
                            CONTINUE = True
                            break
                    if CONTINUE:
                        continue
                    if rule.consequence[3][0] != newworld.values[0] - oldworld.values[0]:
                        # score increase did not happen
                        RemoveRule(newrules, newnegrules, rule)
                        continue
                    for k in range(1, len(rule.consequence[3])):  # wrong value prediction
                        if rule.consequence[3][k] != newworld.values[k]:
                            RemoveRule(newrules, newnegrules, rule)
                            CONTINUE = True
                            break
                    if CONTINUE:
                        continue
                    if rule.consequence[2] != newworld.board[y][x]:
                        RemoveRule(newrules, newnegrules, rule)
        worldchange = deepcopy(change_sets[0])
        return newrules, newnegrules


    def world_predict(self, oldworld: WorldNode, action: Action, rules: List[Rule], customGoal = None, t = 0):
        """
        APPLY MOVE TO THE WORLD MODEL WHEREBY WE USE THE EXISTING RULES TO DECIDE HOW A GRID ELEMENT CHANGES
        """
        newworld = deepcopy(oldworld)
        used_rules_sumscore = 0.0
        used_rules_amount = 0
        (positionscores, highesthighscore) = rule_positionscores(oldworld, action, rules)
        height, width = oldworld.height, oldworld.width
        for y in range(height):
            for x in range(width):
                if (y,x) not in positionscores:
                    continue
                scores, highscore = positionscores[(y,x)]
                for rule in rules:
                    if ruleApplicable(scores, highscore, highesthighscore, rule):
                        if highscore == 1.0:
                            newworld.values = rule.consequence[3]
                        newworld.board[y][x] = rule.consequence[2]
                        used_rules_sumscore += scores.get(rule, 0.0)
                        used_rules_amount += 1
        score = used_rules_sumscore/used_rules_amount if used_rules_amount > 0 else 1.0 #AIRIS confidence
        robot_position = newworld.loc_robot
        age = 0
        if robot_position:
            age = (t - newworld.times[robot_position[0]][robot_position[1]])
        #but if the predicted world has higher value, then set prediction score to the best it can be
        if (newworld.values[0] == 1 and score == 1.0)  or (customGoal and customGoal(newworld)):
            score = float('-inf')
        return newworld, score, age 

    def max_depth__breadth_first_search(self, world: np.ndarray, rules: List[Rule], actions, max_depth=100, customGoal = None):
        """PLAN FORWARD SEARCHING FOR SITUATIONS OF HIGHEST UNCERTAINTY (TODO ALSO CONSIDER VALUE)"""
        queue = deque([(world, [], 0)])  # Initialize queue with world state, empty action list, and depth 0
        encountered = dict([])
        best_score = float("inf")
        best_actions = []
        best_action_combination_for_revisit = []
        oldest_age = 0.0
        while queue:
            current_world, planned_actions, depth = queue.popleft()  # Dequeue from the front
            if depth > max_depth:  # If maximum depth is reached, stop searching
                continue
            world_BOARD_VALUES = to_tuple([current_world.board]) #, current_world[VALUES][1:]]) #-- 1!!!
            if world_BOARD_VALUES in encountered and depth >= encountered[world_BOARD_VALUES]:
                continue
            if world_BOARD_VALUES not in encountered or depth < encountered[world_BOARD_VALUES]:
                encountered[world_BOARD_VALUES] = depth
            for action in actions:
                new_world, new_score, new_age = self.world_predict(deepcopy(current_world), action, rules, customGoal)
                new_planned_actions = planned_actions + [action]
                if new_score < best_score or (new_score == best_score and len(new_planned_actions) < len(best_actions)):
                    best_actions = new_planned_actions
                    best_score = new_score
                if new_age > oldest_age or (new_age == oldest_age and len(new_planned_actions) < len(best_action_combination_for_revisit)):
                    best_action_combination_for_revisit = new_planned_actions
                    oldest_age = new_age
                if new_score == 1.0:
                    # _, robot_cnt = get_robot_position(new_world)
                    # if robot_cnt == 1:
                    queue.append((new_world, new_planned_actions, depth + 1))  # Enqueue children at the end
        return best_actions, best_score, best_action_combination_for_revisit, oldest_age

    def airis_step(self, rulesin, negrules, oldworld: WorldNode):
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
        observed_world = oldworld.localObserve()
        favoured_actions, airis_score, favoured_actions_for_revisit, oldest_age = self.max_depth__breadth_first_search(observed_world, rules, oldworld.actions, customGoal = WorldNode.cupIsOnTable)
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
                action = oldworld.motorbabbling()
        else:
            print("ACHIEVE" if airis_score == float("-inf") else "CURIOUS", plan_prettystring(favoured_actions), airis_score)#, rules)
            action = favoured_actions[0]
            plan = favoured_actions
        if debuginput == "w":
            action = Action.U
        if debuginput == "s":
            action = Action.D
        if debuginput == "a":
            action = Action.L
        if debuginput == "d":
            action = Action.R
        if debuginput == 'l':
            for x in rules:
                prettyPrintRule(x)
            input()
        newworld = oldworld.move(action)
        observed_world_old: WorldNode = deepcopy(observed_world)
        observed_world = newworld.localObserve()
        predicted_world, _, __ = self.world_predict(deepcopy(observed_world_old), action, rules)
        print(f"\033[0mWorld t={t} beliefs={len(rules)}:\033[97;40m")
        print(newworld)
        print("\033[0mMental map:\033[97;44m")
        print(observed_world)
        print("\033[0mPredicted end:\033[97;41m")
        planworld: WorldNode = deepcopy(predicted_world)
        for i in range(1, len(plan)):
            planworld, _, __ = self.world_predict(deepcopy(planworld), plan[i], rules)
        print(planworld)
        print("\033[0m")
        (newrules, newnegrules) = self.world_observe(deepcopy(observed_world_old), action, observed_world, rules, negrules, predicted_world)
        for rule in rulesExcluded: #add again so we won't loose them
            newrules.add(rule)
        return newrules, newnegrules, newworld, debuginput
