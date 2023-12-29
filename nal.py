from narsese import *
from environment import *
from typing import Set
from learner import Rule

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


def prettyaction(action: Action):
    M = {Action.L: "^left", Action.R: "^right",
         Action.U: "^up", Action.D: "^down"}
    return M[action]


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



def ChoiceRule(rule1, rule2):
    T1 = TruthValue(RuleEvidence[rule1])
    T2 = TruthValue(RuleEvidence[rule2])
    if Truth_Expectation(T1) > Truth_Expectation(T2):
        return rule1
    return rule2
