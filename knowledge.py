import world as W
import prettyprint as P

RuleEvidence = dict([])


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


def AddRuleEvidence(rule, positive, w_max=20):
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


def RemoveRule(ruleset, negruleset, rule):
    for r in ruleVariants(rule):
        AddRuleEvidence(rule, False)
        print("Neg. revised: ", end="")
        P.prettyPrintRule(rule)
        # in a deterministic setting this would have sufficed however
        # simply excluding rules does not work in non-deterministic ones
        # if rule in ruleset:
        #    print("RULE REMOVAL: ", end=""); prettyPrintRule(rule)
        #    ruleset.remove(rule)
        # negruleset.add(rule)


def AddRule(ruleset, negruleset, rule):  # try location symmetry
    variants = ruleVariants(rule)
    variantsadded = set([])
    for rule in variants:
        AddRuleEvidence(rule, True)
        print("Pos. revised: ", end="")
        P.prettyPrintRule(rule)
        if rule not in negruleset:
            if rule not in ruleset:
                # print("RULE ADDITION: ", end=""); prettyPrintRule(rule)
                ruleset.add(rule)
                variantsadded.add(rule)
    return variantsadded


# location symmetry (knowledge about movement operations for faster learning)
def ruleVariants(rule):
    action_values_precons = rule[0]
    conditions = action_values_precons[2:]
    action = action_values_precons[0]
    for (y, x, v) in conditions:  # unnecessary
        if (action == W.left or action == W.right) and y != 0:
            return []
        if (action == W.up or action == W.down) and x != 0:
            return []
    rules = [rule]
    # not such an op where symmetry would apply
    if action != W.left and action != W.right and action != W.down and action != W.up:
        return rules
    conditionlist2 = sorted([ConditionRotate(x) for x in conditions])
    conditionlist3 = sorted([ConditionRotate(x) for x in conditionlist2])
    conditionlist4 = sorted([ConditionRotate(x) for x in conditionlist3])
    action2 = OpRotate(action)
    action3 = OpRotate(action2)
    action4 = OpRotate(action3)
    rules.append(
        (tuple([action2, action_values_precons[1]] + conditionlist2), rule[1]))
    rules.append(
        (tuple([action3, action_values_precons[1]] + conditionlist3), rule[1]))
    rules.append(
        (tuple([action4, action_values_precons[1]] + conditionlist4), rule[1]))
    return rules


def OpRotate(op):
    if op == W.right:
        return W.down
    if op == W.down:
        return W.left
    if op == W.left:
        return W.up
    if op == W.up:
        return W.right


def ConditionRotate(cond):
    (y, x, v) = cond
    if y == 0 and x == -1:  # left
        return (-1, 0, v)  # up
    if y == -1 and x == 0:  # up
        return (0, 1, v)  # right
    if y == 0 and x == 1:  # right
        return (1, 0, v)  # down
    if y == 1 and x == 0:  # down
        return (0, -1, v)  # left
    if x == 0 and y == 0:
        return (0, 0, v)


def validCondition(cond):  # restrict to neighbours (CA assumption)
    (y, x, v) = cond
    if y == 0 and x == 0:  # self
        return True
    if y == 0 and x == -1:  # left
        return True
    if y == -1 and x == 0:  # up
        return True
    if y == 0 and x == 1:  # right
        return True
    if y == 1 and x == 0:  # down
        return True
    if x == 0 and y == 0:  # mid stays same
        return True
    return False
