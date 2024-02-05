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
import time
print("Welcome to NACE!")
if "debug" in sys.argv:
    print('Debugger: enter to let agent World_Move, w/a/s/d for manual World_Movement in simulated world, v for switching to imagined world, l to list hypotheses, p to look through the predicted plan step-wise, q to exit imagined world')
else:
    print('Pass "debug" parameter for interactive debugging, "silent" for hiding hypothesis formation output, "manual" for trying the environment as a human, "nosleep" to remove simulation visualization delay, "nopredictions" to hide prediction rectangles, "nogui" to hide GUI, "notextures" to not render textures in GUI, "colors" to render colors.')
from nace import *

#Configure hypotheses to use euclidean space properties if desired
Hypothesis_UseMovementOpAssumptions(left, right, up, down, "DisableOpSymmetryAssumption" in sys.argv)
#Run the simulation in a loop for up to k steps:
Time = -1
behavior = "BABBLE"
plan = []
def Step(inject_key=""):
    global usedRules, FocusSet, RuleEvidence, loc, observed_world, rules, negrules, world, debuginput, values, lastplanworld, planworld, behavior, plan, Time
    Time+=1
    start_time = time.time()
    usedRules, FocusSet, RuleEvidence, loc, observed_world, rules, negrules, world, debuginput, values, lastplanworld, planworld, behavior, plan = NACE_Cycle(Time, FocusSet, RuleEvidence, loc, observed_world, rules, negrules, deepcopy(world), inject_key)
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
    from matplotlib.animation import FuncAnimation
    from matplotlib.patches import FancyArrow
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle, Circle
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch
    import matplotlib.colors as mc
    from nace import _IsPresentlyObserved
    import colorsys
    import os

    def lighten_color(color, amount=0.5):
        try:
            c = mc.cnames[color]
        except:
            c = color
        c = colorsys.rgb_to_hls(*mc.to_rgb(c))
        return colorsys.hls_to_rgb(c[0], 1 - amount * (1 - c[1]), c[2])

    def plot_pattern(pattern, values):
        global loc
        rows = len(pattern)
        cols = len(pattern[0])
        ax.clear()
        for i in range(rows):
            for j in range(cols):
                color = colors.get(pattern[i][j], 'white')
                lastaction = None
                if len([x for x in plan if x == left or x == right]) > 0:
                    lastaction = [x for x in plan if x == left or x == right][-1]
                if "colors" not in sys.argv:
                    if pattern[i][j] == ".":
                        color = "gray"
                        color = lighten_color(color, 0.6)
                    elif _IsPresentlyObserved(Time, observed_world, i, j):
                        color = "white"
                    else:
                        color = "lightgray"
                else:
                    if not _IsPresentlyObserved(Time, observed_world, i, j) and color != "gray":
                        if color == "white":
                            color = "lightgray"
                        else:
                            color = lighten_color(color, 1.2)
                ax.add_patch(Rectangle((j, -i), 1, 1, facecolor=color, edgecolor='none'))
                if "manual" not in sys.argv and "nopredictions" not in sys.argv and observed_world[BOARD][i][j] != planworld[BOARD][i][j]:
                    color = colors.get(planworld[BOARD][i][j], 'white')
                    if "colors" not in sys.argv:
                        if pattern[i][j] == ".":
                            color = "gray"
                        elif _IsPresentlyObserved(Time, observed_world, i, j):
                            color = "lightgray"
                        else:
                            color = "gray"
                    elif not _IsPresentlyObserved(Time, observed_world, i, j) and color != "gray":
                        if color == "white":
                            color = "lightgray"
                        else:
                            color = lighten_color(color, 1.2)
                    color = lighten_color(color, 1.1)
                    patt = planworld[BOARD][i][j]
                    if behavior == "CURIOUS" and planworld[BOARD][i][j] != lastplanworld[BOARD][i][j]:
                        patt = "what"
                    if patt == ".":
                        patt = "unknown"
                    ax.add_patch(Circle((j+0.5, -i+0.5), 0.25, facecolor=color, edgecolor='none', zorder=50, alpha=0.8))
                    if patt != "what" and (((lastaction is None and direction == "right") or lastaction == right) and patt == ROBOT) or patt.isupper():
                        patt += "2"
                    if "notextures" not in sys.argv and patt != " ":
                        # Display the texture inside the rectangle using imshow
                        ax.imshow(M[patt], extent=(j+0.3, j + 0.7, -i+0.3, -i + 0.7), zorder=100)
                patt = pattern[i][j]
                if (direction == "right" and patt == 'x') or patt.isupper():
                    patt += "2"
                if patt == ".":
                    patt = "unknown"
                if "notextures" not in sys.argv and patt in M:
                    # Display the texture inside the rectangle using imshow
                    ax.imshow(M[patt], extent=(j, j + 1, -i, -i + 1), zorder=10)
        # Map of actions to changes in x and y
        action_dict = {left: (-1, 0), right: (1, 0), up: (0, 1), down: (0, -1)}
        # Plot path
        if len(plan) > 0:
            (x,y) = (loc[0]+0.5,-loc[1]+0.5)
            vizloc = loc
            #nextstepworld, _, __, ___ = NACE_Predict(Time, FocusSet, deepcopy(observed_world), plan[0], usedRules)
            nextstepworld = observed_world
            for i, action in enumerate(plan[1:]):
                dx, dy = action_dict[action]
                if i == len(plan[1:])-1:
                    ax.add_patch(FancyArrow(x, y, dx, dy, color='black', width=0.01, head_width=0.1, head_length=0.2))
                else:
                    ax.add_line(Line2D([x, x + dx], [y, y + dy], color='black'))
                nextstepworld, _, __, ___ = NACE_Predict(Time, FocusSet, deepcopy(nextstepworld), action, usedRules)
                #now check if there is indeed a robot predicted to be there
                #(to take into account that the agent indeed knows how location is affected, which matters for visualization, as in egg world)
                tx = x + dx
                ty = y + dy
                tvizloc = action(vizloc)
                if nextstepworld[BOARD][tvizloc[1]][tvizloc[0]] == ROBOT:
                    (x, y, vizloc) = (tx, ty, tvizloc)
        ax.set_xlim(0, width)  # Set the desired x-axis limits
        ax.set_ylim(-rows+1, 1)  # Set the desired y-axis limits
        ax.set_aspect('equal', adjustable='box')
        ax.set_xticks(range(cols+1))
        ax.set_yticks(range(-rows+1, 1))
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.grid(False)
        plt.title(behavior + " score=" + str(values[0]) + " vars="+str(list(values[1:])))
        plt.draw()

    def updateloc(key=""):
        global lastloc, direction
        if loc[0] > lastloc[0] or key == "d":
            direction = "right"
        if loc[0] < lastloc[0] or key == "a":
            direction = "left"

    def on_key(event):
        if event.key in ["w", "s", "a", "d"]:
            Step(inject_key = event.key)
            updateloc(event.key)
            plot_pattern(observed_world[BOARD], observed_world[VALUES])
        if event.key == "s":
            event.stop = True

    frame = 1
    def update(wat):
        global lastloc, direction, frame
        start = 1
        for arg in sys.argv:
            if arg.startswith("startframe="):
                start = int(arg.split("startframe=")[1])
        if frame >= start:
            Step()
            updateloc()
        plot_pattern(observed_world[BOARD], observed_world[VALUES])
        lastloc = loc
        frame += 1

    lastloc = loc
    direction = "right"
    M = {}
    if "notextures" not in sys.argv:
        # Iterate through files in the folder
        for filename in os.listdir("textures"):
            # Check if the file has a ".png" extension
            if filename.endswith(".png"):
                # Remove the ".png" extension to get the key
                key = os.path.splitext(filename)[0]
                # Add to dictionary M
                M[key] = plt.imread('textures/' + filename)
    planworld = [[["." for x in world[BOARD][i]] for i in range(len(world[BOARD]))], world[VALUES], world[TIMES]]
    lastplanworld = planworld
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
        #eletric shock level
        SHOCK: "yellow"
    }
    fig, ax = plt.subplots()
    plt.rcParams['keymap.save'].remove('s')
    plt.rcParams['keymap.quit'].remove('q')
    plot_pattern(pattern, [0, 0])
    fig.canvas.mpl_connect('key_press_event', on_key)
    if "manual" not in sys.argv and "debug" not in sys.argv:
        frames = 0
        worldname = ""
        for arg in sys.argv:
            if arg.startswith("frames="):
                frames = int(arg.split("frames=")[1])
            if arg.startswith("world="):
                worldname = arg.split("world=")[1]
        if frames > 0:
            ani = FuncAnimation(fig, update, interval=100, repeat=False, frames=frames)  # Update every 100 milliseconds
            ani.save(f'world{worldname}.gif', writer='imagemagick', fps=1)
        else:
            ani = FuncAnimation(fig, update, interval=100)  # Update every 100 milliseconds
    plt.show()

