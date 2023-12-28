from narsese import *
from environment import *

RuleEvidence = dict([])

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

def prettyaction(action: Action):
    M = {Action.L: "^left", Action.R: "^right", Action.U: "^up", Action.D: "^down"}
    return M[action]

def AddRuleEvidence(rule, positive, w_max = 20):
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
        print("Neg. revised: ", end="");  prettyPrintRule(rule)
        #in a deterministic setting this would have sufficed however
        #simply excluding rules does not work in non-deterministic ones
        #if rule in ruleset:
        #    print("RULE REMOVAL: ", end=""); prettyPrintRule(rule)
        #    ruleset.remove(rule)
        #negruleset.add(rule)


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
    action: Action = action_values_precons[0]
    for (y,x,v) in conditions: #unnecessary
        if (action is Action.L or action is Action.R) and y != 0:
            return []
        if (action is Action.U or action is Action.D) and x != 0:
            return []
    rules = [rule]
    if action is not Action.L and action is not Action.R and action is not Action.D and action is not Action.U: #not such an op where symmetry would apply
        return rules
    conditionlist2 = sorted([ConditionRotate(x) for x in conditions])
    conditionlist3 = sorted([ConditionRotate(x) for x in conditionlist2])
    conditionlist4 = sorted([ConditionRotate(x) for x in conditionlist3])
    action2: Action = action.rotate()
    action3: Action = action2.rotate()
    action4: Action = action3.rotate()
    rules.append((tuple([action2, action_values_precons[1]] + conditionlist2), rule[1]))
    rules.append((tuple([action3, action_values_precons[1]] + conditionlist3), rule[1]))
    rules.append((tuple([action4, action_values_precons[1]] + conditionlist4), rule[1]))
    return rules

def AddRule(ruleset, negruleset, rule): #try location symmetry
    variants = ruleVariants(rule)
    variantsadded = set([])
    for rule in variants:
        AddRuleEvidence(rule, True)
        print("Pos. revised: ", end="");  prettyPrintRule(rule)
        if rule not in negruleset:
            if rule not in ruleset:
                #print("RULE ADDITION: ", end=""); prettyPrintRule(rule)
                ruleset.add(rule)
                variantsadded.add(rule)
    return variantsadded

def ChoiceRule(rule1, rule2):
    T1 = TruthValue(RuleEvidence[rule1])
    T2 = TruthValue(RuleEvidence[rule2])
    if Truth_Expectation(T1) > Truth_Expectation(T2):
        return rule1
    return rule2
