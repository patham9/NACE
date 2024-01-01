def Prettyprint_plan(actionlist):
    return [_prettyaction(x) for x in actionlist[1:]]

def Prettyprint_rule(RuleEvidence, Hypothesis_TruthValue, rule):
    actions_values_preconditions = rule[0]
    action = _prettyaction(actions_values_preconditions[0])
    precons = actions_values_preconditions[2:]
    print("<(", end="")
    for i, x in enumerate(actions_values_preconditions[1]):
        name = "keys"
        print(f"{_prettyVarValue(name, x)}", end="")
        print(f" &| ", end="")
    for i, x in enumerate(precons):
        print(f"{_prettyTriplet(x)}", end="")
        if i != len(precons)-1:
            print(f" &| ", end="")
    scoreInc = f"<s_{rule[1][3][0]} --> scorePlus>"
    keys = f"<k_{rule[1][3][1]} --> keys>"
    print(") &/", action, "=/> (" + _prettyTriplet(rule[1]) + " &| " + scoreInc + " &| " + keys + ")>.", Hypothesis_TruthValue(RuleEvidence[rule]))

def _prettyVarValue(name, value):
    return f"<k_{value} --> {name}>"

def _prettyTriplet(triplet):
    (y, x, value) = triplet[:3]
    if x == 0 and y == 0:
        return f"<(mid * '{value}') --> shape>"
    if x == 1 and y == 0:
        return f"<(right * '{value}') --> shape>"
    if x == -1 and y == 0:
        return f"<(left * '{value}') --> shape>"
    if x == 0 and y == 1:
        return f"<(down * '{value}') --> shape>"
    if x == 0 and y == -1:
        return f"<(up * '{value}') --> shape>"
    return triplet

def _prettyaction(action):
    return "^" + str(action).split("<function ")[1].split(" at")[0]
