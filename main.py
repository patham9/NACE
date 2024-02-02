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

from matplotlib.animation import FuncAnimation
import sys
import time
print("Welcome to NACE!")
if "debug" in sys.argv:
    print('Debugger: enter to let agent World_Move, w/a/s/d for manual World_Movement in simulated world, v for switching to imagined world, l to list hypotheses, p to look through the predicted plan step-wise, q to exit imagined world')
else:
    print('Pass "debug" parameter for interactive debugging, "silent" for hiding hypothesis formation output, "manual" for trying the environment as a human, "nosleep" to remove simulation visualization delay, "hidepredictions" to hide prediction rectangles, "nogui" to hide GUI.')
from nace import *

#Configure hypotheses to use euclidean space properties if desired
Hypothesis_UseMovementOpAssumptions(left, right, up, down, "DisableOpSymmetryAssumption" in sys.argv)
#Run the simulation in a loop for up to k steps:
Time = -1
behavior = "BABBLE"
def Step(inject_key=""):
    global usedRules, FocusSet, RuleEvidence, loc, observed_world, rules, negrules, world, debuginput, values, planworld, behavior, Time
    Time+=1
    start_time = time.time()
    usedRules, FocusSet, RuleEvidence, loc, observed_world, rules, negrules, world, debuginput, values, planworld, behavior = NACE_Cycle(Time, FocusSet, RuleEvidence, loc, observed_world, rules, negrules, deepcopy(world), inject_key)
    end_time = time.time()
    print("score=" + str(world[VALUES][0]) + ", vars="+str(list(world[VALUES][1:])), end="")
    if "manual" in sys.argv:
        print()
    else:
        print(",", "focus="+str(FocusSet))
    elapsed_time = end_time - start_time
    if elapsed_time < 1.0 and "nosleep" not in sys.argv and "debug" not in sys.argv and "manual" not in sys.argv:
        time.sleep(1.0 - elapsed_time)
    if "debug" in sys.argv and debuginput != "" and debuginput not in ["w", "a", "s", "d", "l", "p"]:
        predworld = deepcopy(observed_world)
        score = 0.0
        while True:
            print("\033[1;1H\033[2J")
            print("\033[0mImagined map:\033[97;43m")
            World_Print(predworld)
            print("\033[0m")
            NACE_PrintScore(score)
            print("values:", values)
            d = input()
            score = 0.0
            if d == 'q':
                break
            if d == 'r':
                predworld = deepcopy(observed_world)
            if d == 'a':
                predworld, score, age, values = NACE_Predict(Time, FocusSet, deepcopy(predworld), left, usedRules)
            if d == 'd':
                predworld, score, age, values = NACE_Predict(Time, FocusSet, deepcopy(predworld), right, usedRules)
            if d == 'w':
                predworld, score, age, values = NACE_Predict(Time, FocusSet, deepcopy(predworld), up, usedRules)
            if d == 's':
                predworld, score, age, values = NACE_Predict(Time, FocusSet, deepcopy(predworld), down, usedRules)
            if d == 'l':
                for x in rules:
                    Prettyprint_rule(RuleEvidence, Hypothesis_TruthValue, x)
                input()
            if d == 'n':
                for x in negrules:
                    Prettyprint_rule(x)
                input()

if "nogui" in sys.argv:
    for Time in range(300):
        Step()
if "nogui" in sys.argv:
    exit()
else:
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch
    import matplotlib.colors as mc
    from nace import _IsPresentlyObserved
    import colorsys

    def lighten_color(color, amount=0.5):
        try:
            c = mc.cnames[color]
        except:
            c = color
        c = colorsys.rgb_to_hls(*mc.to_rgb(c))
        return colorsys.hls_to_rgb(c[0], 1 - amount * (1 - c[1]), c[2])

    def plot_pattern(pattern, values):
        rows = len(pattern)
        cols = len(pattern[0])
        ax.clear()
        for i in range(rows):
            for j in range(cols):
                color = colors.get(pattern[i][j], 'white')
                if "manual" not in sys.argv:
                    if not _IsPresentlyObserved(Time, observed_world, i, j) and color != "gray":
                        if color == "white":
                            color = "lightgray"
                        else:
                            color = lighten_color(color, 1.2)
                ax.add_patch(Rectangle((j, -i), 1, 1, facecolor=color, edgecolor='none'))
                if "manual" not in sys.argv and "hidepredictions" not in sys.argv and observed_world[BOARD][i][j] != planworld[BOARD][i][j]:
                    color = colors.get(planworld[BOARD][i][j], 'white')
                    if not _IsPresentlyObserved(Time, observed_world, i, j) and color != "gray":
                        if color == "white":
                            color = "lightgray"
                        else:
                            color = lighten_color(color, 1.2)
                    ax.add_patch(Rectangle((j+0.4, -i+0.4), 0.2, 0.2, facecolor=color, edgecolor='none'))
                
        ax.set_aspect('equal', adjustable='box')
        ax.set_xticks(range(cols+1))
        ax.set_yticks(range(-rows+1, 1))
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.grid(False)
        plt.title(behavior + " score=" + str(values[0]) + " vars="+str(list(values[1:])))
        plt.draw()

    def on_key(event):
        #if event.key == 'r':
            # Example: Rotate the pattern 90 degrees clockwise
        if event.key in ["w", "s", "a", "d"]:
            Step(inject_key = event.key)
                #global pattern
                #pattern = [''.join(row) for row in zip(*pattern[::-1])]
            plot_pattern(observed_world[BOARD], observed_world[VALUES])
        if event.key == "s":
            event.stop = True

    def update(wat):
        Step()
        plot_pattern(observed_world[BOARD], observed_world[VALUES])

    planworld = [[["." for x in world[BOARD][i]] for i in range(len(world[BOARD]))], world[VALUES], world[TIMES]]
    pattern = [
        "............",
        "............",
        "............",
        "............",
        "............",
        "............",
        "............"
    ]
    colors = {
        ' ': 'white',
        ROBOT: 'red',
        '.': 'gray',
        #food level:
        WALL: 'blue',
        FOOD: 'green',
        ARROW_DOWN: 'purple',
        ARROW_UP: 'darkblue',
        #cup table level:
        CUP: 'cyan', #purple
        TABLE: 'orange',
        #door key battery level:
        DOOR: 'cyan', 
        KEY: 'magenta',
        BATTERY: 'green',
        #pong
        BALL: 'green',
        #egg level:
        EGG: 'orange',
        EGGPLACE: 'cyan',
        CHICKEN: 'green',
        #soccer:
        GOAL: 'green',
        SBALL: 'orange',
    }
    fig, ax = plt.subplots()
    plt.rcParams['keymap.save'].remove('s')
    plt.rcParams['keymap.quit'].remove('q')
    plot_pattern(pattern, [0, 0])
    fig.canvas.mpl_connect('key_press_event', on_key)
    if "manual" not in sys.argv and "debug" not in sys.argv:
        ani = FuncAnimation(fig, update, interval=1000)  # Update every 1000 milliseconds (1 second)
    plt.show()

