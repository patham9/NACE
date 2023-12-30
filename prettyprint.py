from constants import *
import world as W
import knowledge as K


def printworld(world):
    for line in world[BOARD]:
        print("".join(line))


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
    print(") &/", action, "=/> (" + prettyTriplet(
        rule[1]) + " &| " + scoreInc + " &| " + keys + ")>.", K.TruthValue(K.RuleEvidence[rule]))


def prettyaction(action):
    M = {W.left: "^left", W.right: "^right", W.up: "^up", W.down: "^down"}
    return M[action]


def plan_prettystring(actionlist):
    return [prettyaction(x) for x in actionlist[1:]]
