import sys
from prettyprint import *

left, right, up, down = (None, None, None, None)
def UseMovementOpAssumptions(leftOp, rightOp, upOp, downOp):
    global left, right, up, down
    left, right, up, down = (leftOp, rightOp, upOp, downOp)

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

def AddHypothesisEvidence(RuleEvidence, rule, positive, w_max = 20):
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

def TruthValue(wpn):
    (wp, wn) = wpn
    frequency = wp / (wp + wn)
    confidende = (wp + wn) / (wp + wn + 1)
    return (frequency, confidende)

def Truth_Expectation(tv):
    (f, c) = tv
    return (c * (f - 0.5) + 0.5)

def HypothesisChoice(rule1, rule2):
    T1 = TruthValue(RuleEvidence[rule1])
    T2 = TruthValue(RuleEvidence[rule2])
    if Truth_Expectation(T1) > Truth_Expectation(T2):
        return rule1
    return rule2
    
def HypothesisContradicted(RuleEvidence, ruleset, negruleset, rule):
    for r in ruleVariants(rule):
        RuleEvidence = AddHypothesisEvidence(RuleEvidence, rule, False)
        if "silent" not in sys.argv:
            print("Neg. revised: ", end="");  prettyPrintRule(RuleEvidence, TruthValue, rule)
        #in a deterministic setting this would have sufficed however
        #simply excluding rules does not work in non-deterministic ones
        #if rule in ruleset:
        #    print("RULE REMOVAL: ", end=""); prettyPrintRule(rule)
        #    ruleset.remove(rule)
        #negruleset.add(rule)
    return RuleEvidence, ruleset, negruleset

def HypothesisConfirmed(RuleEvidence, ruleset, negruleset, rule): #try location symmetry
    variants = ruleVariants(rule)
    for rule in variants:
        RuleEvidence = AddHypothesisEvidence(RuleEvidence, rule, True)
        if "silent" not in sys.argv:
            print("Pos. revised: ", end="");  prettyPrintRule(RuleEvidence, TruthValue, rule)
        if rule not in negruleset:
            if rule not in ruleset:
                #print("RULE ADDITION: ", end=""); prettyPrintRule(rule)
                ruleset.add(rule)
    return RuleEvidence, ruleset
