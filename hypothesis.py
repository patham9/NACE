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

left, right, up, down = (None, None, None, None)
def Hypothesis_UseMovementOpAssumptions(leftOp, rightOp, upOp, downOp):
    global left, right, up, down
    left, right, up, down = (leftOp, rightOp, upOp, downOp)

def Hypothesis_TruthValue(wpn):
    (wp, wn) = wpn
    frequency = wp / (wp + wn)
    confidende = (wp + wn) / (wp + wn + 1)
    return (frequency, confidende)

def Hypothesis_TruthExpectation(tv):
    (f, c) = tv
    return (c * (f - 0.5) + 0.5)

def Hypothesis_Choice(rule1, rule2):
    T1 = Hypothesis_TruthValue(RuleEvidence[rule1])
    T2 = Hypothesis_TruthValue(RuleEvidence[rule2])
    if Hypothesis_TruthExpectation(T1) > Hypothesis_TruthExpectation(T2):
        return rule1
    return rule2

def Hypothesis_Contradicted(RuleEvidence, ruleset, negruleset, rule):
    for r in _Variants(rule):
        RuleEvidence = _AddEvidence(RuleEvidence, rule, False)
        if "silent" not in sys.argv:
            print("Neg. revised: ", end="");  Prettyprint_rule(RuleEvidence, Hypothesis_TruthValue, rule)
        #in a deterministic setting this would have sufficed however
        #simply excluding rules does not work in non-deterministic ones
        #if rule in ruleset:
        #    print("RULE REMOVAL: ", end=""); Prettyprint_rule(rule)
        #    ruleset.reWorld_Move(rule)
        #negruleset.add(rule)
    return RuleEvidence, ruleset, negruleset

def Hypothesis_Confirmed(RuleEvidence, ruleset, negruleset, rule): #try location symmetry
    variants = _Variants(rule)
    for rule in variants:
        RuleEvidence = _AddEvidence(RuleEvidence, rule, True)
        if "silent" not in sys.argv:
            print("Pos. revised: ", end="");  Prettyprint_rule(RuleEvidence, Hypothesis_TruthValue, rule)
        if rule not in negruleset:
            if rule not in ruleset:
                #print("RULE ADDITION: ", end=""); Prettyprint_rule(rule)
                ruleset.add(rule)
    return RuleEvidence, ruleset

def Hypothesis_ValidCondition(cond):  #restrict to neighbours (CA assumption)
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

def _OpRotate(op):
    if op == right:
        return down
    if op == down:
        return left
    if op == left:
        return up
    if op == up:
        return right

def _ConditionRotate(cond):
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

def _Variants(rule): #location symmetry (knowledge about World_Movement operations for faster learning)
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
    conditionlist2 = sorted([_ConditionRotate(x) for x in conditions])
    conditionlist3 = sorted([_ConditionRotate(x) for x in conditionlist2])
    conditionlist4 = sorted([_ConditionRotate(x) for x in conditionlist3])
    action2 = _OpRotate(action)
    action3 = _OpRotate(action2)
    action4 = _OpRotate(action3)
    rules.append((tuple([action2, action_values_precons[1]] + conditionlist2), rule[1]))
    rules.append((tuple([action3, action_values_precons[1]] + conditionlist3), rule[1]))
    rules.append((tuple([action4, action_values_precons[1]] + conditionlist4), rule[1]))
    return rules

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

