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
from prettyprint import *

#Register operations in case euclidean space operation alignment assumptions should be exploited which helps data efficiency
def Hypothesis_UseMovementOpAssumptions(leftOp, rightOp, upOp, downOp, DisableOpSymmetryAssumptionFlag):
    global left, right, up, down, DisableOpSymmetryAssumption
    left, right, up, down, DisableOpSymmetryAssumption = (leftOp, rightOp, upOp, downOp, DisableOpSymmetryAssumptionFlag)

#The truth value of a hypothesis can be obtained directly from the positive and negative evidence counter
def Hypothesis_TruthValue(wpn):
    (wp, wn) = wpn
    frequency = wp / (wp + wn)
    confidende = (wp + wn) / (wp + wn + 1)
    return (frequency, confidende)

#The truth expectation calculation based on the truth value (frequency, confidence) tuple
def Hypothesis_TruthExpectation(tv):
    (f, c) = tv
    return (c * (f - 0.5) + 0.5)

#When two hypotheses predict a different outcome for the same conditions, the higher truth exp one is chosen
def Hypothesis_Choice(RuleEvidence, rule1, rule2):
    T1 = Hypothesis_TruthValue(RuleEvidence[rule1])
    T2 = Hypothesis_TruthValue(RuleEvidence[rule2])
    if Hypothesis_TruthExpectation(T1) > Hypothesis_TruthExpectation(T2):
        return rule1
    return rule2

#Negative evidence was found for the hypothesis/rule
def Hypothesis_Contradicted(RuleEvidence, ruleset, negruleset, rule):
    RuleEvidence = _AddEvidence(RuleEvidence, rule, False)
    if "silent" not in sys.argv:
        print("Neg. revised: ", end="");  Prettyprint_rule(RuleEvidence, Hypothesis_TruthValue, rule)
        #in a deterministic setting this would have sufficed however
        #simply excluding rules does not work in non-deterministic ones
        #if rule in ruleset:
        #    print("RULE REMOVAL: ", end=""); Prettyprint_rule(RuleEvidence, Hypothesis_TruthValue, rule)
        #    ruleset.remove(rule)
        #negruleset.add(rule)
    return RuleEvidence, ruleset, negruleset

#Positive evidence was found for the hypothesis/rule
def Hypothesis_Confirmed(FocusSet, RuleEvidence, ruleset, negruleset, rule): #try location symmetry
    variants = _Variants(FocusSet, rule)
    for i, r in enumerate(variants):
        if i>0: #abduced hypotheses
            if r in RuleEvidence: #this derived hypothesis already exists
                continue
        RuleEvidence = _AddEvidence(RuleEvidence, r, True)
        if "silent" not in sys.argv:
            print("Pos. revised: ", end="");  Prettyprint_rule(RuleEvidence, Hypothesis_TruthValue, r)
        if r not in negruleset:
            if r not in ruleset:
                #print("RULE ADDITION: ", end=""); Prettyprint_rule(rule)
                ruleset.add(r)
    return RuleEvidence, ruleset

#Valid condition predicate defining the accepted neighbourhood between conclusion and condition cells
def Hypothesis_ValidCondition(cond):  #restrict to neighbours (CA assumption)
    (y, x, v) = cond
    if y == 0 and x == 0: #self
        return True
    if y == 0 and (x == -1 or x == -2): #left
        return True
    if (y == -1 or y == -2) and x == 0: #up
        return True
    if y == 0 and (x == 1 or x == 2):  #right
        return True
    if (y == 1 or y == 2) and x == 0:  #down
        return True
    return False

#We exclude rules which have more negative evidence than positive, and choose the highest truth-exp ones whenever a different outcome would be predicted for the same conditions
def Hypothesis_BestSelection(rules, rulesExcluded, RuleEvidence, rulesin):
    for i, rule1 in enumerate(rulesin):
        if Hypothesis_TruthExpectation(Hypothesis_TruthValue(RuleEvidence[rule1])) <= 0.5: #exclude rules which are not better than exp (only 0.5+ makes sense here)
            if rule1 in rules:
                rulesExcluded.add(rule1)
                rules.remove(rule1)
        for j, rule2 in enumerate(rulesin): #exclude rules which are worse by truth value
            if i != j:
                if rule1[0] == rule2[0]:
                    rulex = Hypothesis_Choice(RuleEvidence, rule1, rule2)
                    if rulex == rule1:
                        if rule2 in rules:
                            rulesExcluded.add(rule2)
                            rules.remove(rule2)
                            #print("excluded ", end=''); Prettyprint_rule(rule2)
                    else:
                        if rule1 in rules:
                            rulesExcluded.add(rule1)
                            rules.remove(rule1)
                            #print("excluded", end=''); Prettyprint_rule(rule1)
    return rules, rulesExcluded

#Rotate the operation in euclidean space if euclidean op assumptions are allowed to be used
def _OpRotate(op):
    if op == right:
        return down
    if op == down:
        return left
    if op == left:
        return up
    if op == up:
        return right

#Rotate the conditions as well if euclidean op assumptions are allowed to be utilized
def _ConditionRotate(cond):
    (y, x, v) = cond
    if y == 0 and x == -1: #left
        return (-1, 0, v)  #up
    if y == 0 and x == -2: #left
        return (-2, 0, v)  #up
    if y == -1 and x == 0: #up
        return (0, 1, v)   #right
    if y == -2 and x == 0: #up
        return (0, 2, v)   #right
    if y == 0 and x == 1:  #right
        return (1, 0, v)   #down
    if y == 0 and x == 2:  #right
        return (2, 0, v)   #down
    if y == 1 and x == 0:  #down
        return (0, -1, v)  #left
    if y == 2 and x == 0:  #down
        return (0, -2, v)  #left
    if x == 0 and y == 0:
        return (0, 0, v)

#The rule variants, including hypothetical abduced variations for different directions based on euclidean space rotation and "operation-independence" hypotheses
def _Variants(FocusSet, rule): #explots euclidean space properties (knowledge about World_Movement operations for faster learning)
    action_values_precons = rule[0]
    conditions = action_values_precons[2:]
    action = action_values_precons[0]
    max_focus = None
    max_focus_val = False
    if len(FocusSet) > 0:
        max_focus = max(FocusSet, key=lambda k: FocusSet[k])
    if max_focus is not None:
        for (x,y,val) in action_values_precons[2:]:
            if val == max_focus or rule[1][2] == max_focus:
                max_focus_val = True
    for (y,x,v) in conditions:
        if (action == left or action == right) and y != 0:
            return []
        if (action == up or action == down) and x != 0:
            return []
    rules = [rule]
    action2 = _OpRotate(action)
    action3 = _OpRotate(action2)
    action4 = _OpRotate(action3)
    if DisableOpSymmetryAssumption:
        return rules
    if not max_focus_val:
        rules.append((tuple([left, action_values_precons[1]] + list(conditions)), rule[1]))
        rules.append((tuple([right, action_values_precons[1]] + list(conditions)), rule[1]))
        rules.append((tuple([up, action_values_precons[1]] + list(conditions)), rule[1]))
        rules.append((tuple([down, action_values_precons[1]] + list(conditions)), rule[1]))
    if action != left and action != right and action != down and action != up: #not such an op where symmetry would apply
        return rules
    conditionlist2 = sorted([_ConditionRotate(x) for x in conditions])
    conditionlist3 = sorted([_ConditionRotate(x) for x in conditionlist2])
    conditionlist4 = sorted([_ConditionRotate(x) for x in conditionlist3])
    if max_focus_val:
        rules.append((tuple([action2, action_values_precons[1]] + conditionlist2), rule[1]))
        rules.append((tuple([action3, action_values_precons[1]] + conditionlist3), rule[1]))
        rules.append((tuple([action4, action_values_precons[1]] + conditionlist4), rule[1]))
    return rules

#Add positive or negative evidence for a rule, with a certain max. amount of evidence so that non-stationary environments can be handled too
def _AddEvidence(RuleEvidence, rule, positive, w_max = 20):
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

