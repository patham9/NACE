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
