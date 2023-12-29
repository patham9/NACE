from environment import Action
from typing import Set, List
from learner import Rule
from nal import AddRuleEvidence, prettyaction, prettyTriplet, prettyVarValue, prettyValue, RuleEvidence


class Rule:
    def __init__(self, action: Action, value, precondition, consequence) -> None:
        self.action = action
        self.value = value
        self.preconditions = precondition
        self.consequence = consequence


def RemoveRule(ruleset, negruleset, rule):
    for r in ruleVariants(rule):
        AddRuleEvidence(rule, False)
        print("Neg. revised: ", end="")
        prettyPrintRule(rule)
        # in a deterministic setting this would have sufficed however
        # simply excluding rules does not work in non-deterministic ones
        # if rule in ruleset:
        #    print("RULE REMOVAL: ", end=""); prettyPrintRule(rule)
        #    ruleset.remove(rule)
        # negruleset.add(rule)


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


# location symmetry (knowledge about movement operations for faster learning)
def ruleVariants(rule: Rule) -> List[Rule]:
    # action_values_precons = rule[0]
    conditions = rule.preconditions
    action: Action = rule.action
    for (y, x, v) in conditions:  # unnecessary
        if (action is Action.L or action is Action.R) and y != 0:
            return []
        if (action is Action.U or action is Action.D) and x != 0:
            return []
    rules = [rule]
    # not such an op where symmetry would apply
    if action is not Action.L and action is not Action.R and action is not Action.D and action is not Action.U:
        return rules
    conditionlist2 = sorted([ConditionRotate(x) for x in conditions])
    conditionlist3 = sorted([ConditionRotate(x) for x in conditionlist2])
    conditionlist4 = sorted([ConditionRotate(x) for x in conditionlist3])
    action2: Action = action.rotate()
    action3: Action = action2.rotate()
    action4: Action = action3.rotate()
    rules.append(Rule(action2, rule.value, conditionlist2, rule.consequence))
    rules.append(Rule(action3, rule.value, conditionlist3, rule.consequence))
    rules.append(Rule(action4, rule.value, conditionlist4, rule.consequence))
    return rules


def AddRule(ruleset: Set[Rule], negruleset: Set[Rule], rule: Rule):  # try location symmetry
    variants = ruleVariants(rule)
    variantsadded = set([])
    for rule in variants:
        AddRuleEvidence(rule, True)
        print("Pos. revised: ", end="")
        prettyPrintRule(rule)
        if rule not in negruleset:
            if rule not in ruleset:
                # print("RULE ADDITION: ", end=""); prettyPrintRule(rule)
                ruleset.add(rule)
                variantsadded.add(rule)
    return variantsadded


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
    print(") &/", action, "=/> (" + prettyTriplet(
        rule[1]) + " &| " + scoreInc + " &| " + keys + ")>.", TruthValue(RuleEvidence[rule]))
