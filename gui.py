from matplotlib.animation import FuncAnimation
from matplotlib.patches import FancyArrow
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
import matplotlib.colors as mc
from nace import _IsPresentlyObserved
import colorsys
import sys
import os
from copy import deepcopy
from world import BOARD, VALUES, TIMES
from world import TRASH, HUMAN,COFFEEMACHINE, WALL, ROBOT, CUP, FOOD, BATTERY, FREE, TABLE, GOAL, KEY, DOOR, ARROW_DOWN, ARROW_UP, BALL, EGG, EGGPLACE, CHICKEN, SBALL, SHOCK

def GUI_INIT(Stepval, NACE_Predictval, worldval, locval, leftval, rightval, upval, downval, pickval, dropval, toggleval, widthval, heightval, behaviorval, planval, observed_worldval):
    global Step, NACE_Predict, planworld, lastplanworld, lastloc, direction, M, pattern, colors, left, right, up, down, pick, drop, toggle, width, height, behavior, plan, observed_world
    Step = Stepval
    NACE_Predict = NACE_Predictval
    left = leftval
    right = rightval
    up = upval
    down = downval
    pick = pickval
    drop = dropval
    toggle = toggleval
    width = widthval
    height = heightval
    behavior = behaviorval
    world = worldval
    plan = planval
    observed_world = observed_worldval
    planworld = [[["." for x in world[BOARD][i]] for i in range(len(world[BOARD]))], world[VALUES], world[TIMES]]
    lastplanworld = planworld
    lastloc = locval
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
        COFFEEMACHINE: "black",
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
        SHOCK: "yellow",
        TRASH: "magenta"
    }
    import main #TODO
    GUI_RUN()

def lighten_color(color, amount=0.5):
    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    return colorsys.hls_to_rgb(c[0], 1 - amount * (1 - c[1]), c[2])

predicted_certainty = None
def plot_pattern(pattern, values, DrawPredictions=True):
    global loc, predicted_certainty, plan
    import main
    if DrawPredictions and "nopredictions" in sys.argv:
        DrawPredictions = False
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
            if "manual" not in sys.argv and DrawPredictions and observed_world[BOARD][i][j] != planworld[BOARD][i][j]:
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
    action_dict = {left: (-1, 0), right: (1, 0), up: (0, 1), down: (0, -1), pick: (0, 0), drop: (0, 0), toggle: (0, 0)}
    # Plot path
    if len(plan) > 0 and DrawPredictions:
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
            nextstepworld, predscore, __, ___ = NACE_Predict(Time, FocusSet, deepcopy(nextstepworld), action, usedRules)
            #now check if there is indeed a robot predicted to be there
            #(to take into account that the agent indeed knows how location is affected, which matters for visualization, as in egg world)
            tx = x + dx
            ty = y + dy
            tvizloc = action(vizloc)
            if tvizloc[1] >= 0 and tvizloc[1] < height and tvizloc[0] >= 0 and tvizloc[0] < width and nextstepworld[BOARD][tvizloc[1]][tvizloc[0]] == ROBOT:
                (x, y, vizloc) = (tx, ty, tvizloc)
    ax.set_xlim(0, width)  # Set the desired x-axis limits
    ax.set_ylim(-rows+1, 1)  # Set the desired y-axis limits
    ax.set_aspect('equal', adjustable='box')
    ax.set_xticks(range(cols+1))
    ax.set_yticks(range(-rows+1, 1))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.grid(False)
    plt.title(behavior + " score=" + str(values[0]) + " vars="+str(list(values[1:])) + ("" if predicted_certainty is None else " certainty="+str(predicted_certainty)))
    plt.draw()

def updateloc(key=""):
    global lastloc, direction
    if loc[0] > lastloc[0] or key == "d":
        direction = "right"
    if loc[0] < lastloc[0] or key == "a":
        direction = "left"
    lastloc = loc

predworldi = None
def on_key(event):
    global predworldi, predicted_certainty, usedRules, FocusSet, RuleEvidence, loc, observed_world, rules, negrules, world, debuginput, values, lastplanworld, planworld, behavior, plan, Time
    predicted_certainty = None
    if event.key in ["w", "s", "a", "d", "p", "enter", "r", "b", "n", "t"]:
        if predworldi is None and event.key != 'r':
            usedRules, FocusSet, RuleEvidence, loc, observed_world, rules, negrules, world, debuginput, values, lastplanworld, planworld, behavior, plan, Time = Step(inject_key = event.key)
            updateloc(event.key)
            plot_pattern(observed_world[BOARD], observed_world[VALUES], event.key not in ["w", "s", "a", "d", "b", "n", "t"])
        else:
            if event.key == 'r':
                predworldi = deepcopy(observed_world)
                predicted_certainty = 1.0
            else:
                score = 1.0
                if event.key == 'a':
                    predworldi, score, age, values = NACE_Predict(Time, FocusSet, deepcopy(predworldi), left, usedRules)
                if event.key == 'd':
                    predworldi, score, age, values = NACE_Predict(Time, FocusSet, deepcopy(predworldi), right, usedRules)
                if event.key == 'w':
                    predworldi, score, age, values = NACE_Predict(Time, FocusSet, deepcopy(predworldi), up, usedRules)
                if event.key == 's':
                    predworldi, score, age, values = NACE_Predict(Time, FocusSet, deepcopy(predworldi), down, usedRules)
                if event.key == 'b':
                    predworldi, score, age, values = NACE_Predict(Time, FocusSet, deepcopy(predworldi), pick, usedRules)
                if event.key == 'n':
                    predworldi, score, age, values = NACE_Predict(Time, FocusSet, deepcopy(predworldi), drop, usedRules)
                if event.key == 't':
                    predworldi, score, age, values = NACE_Predict(Time, FocusSet, deepcopy(predworldi), toggle, usedRules)
                if score >= 0.0 and score <= 1.0:
                    predicted_certainty = score
            plot_pattern(predworldi[BOARD], predworldi[VALUES], DrawPredictions=False)
    if event.key == "i":
        if predworldi is None:
            predworldi = deepcopy(observed_world)
        else:
            predworldi = None
    if event.key == "l":
        for x in rules:
            Prettyprint_rule(RuleEvidence, Hypothesis_TruthValue, x)
    if event.key == "u":
        for x in usedRules:
            Prettyprint_rule(RuleEvidence, Hypothesis_TruthValue, x)
    if event.key == "x":
        for x in rules - usedRules:
            Prettyprint_rule(RuleEvidence, Hypothesis_TruthValue, x)
frame = 1
def update(wat):
    global lastloc, direction, frame, usedRules, FocusSet, RuleEvidence, loc, observed_world, rules, negrules, world, debuginput, values, lastplanworld, planworld, behavior, plan, Time
    start = 1
    for arg in sys.argv:
        if arg.startswith("startframe="):
            start = int(arg.split("startframe=")[1])
    if frame >= start:
        usedRules, FocusSet, RuleEvidence, loc, observed_world, rules, negrules, world, debuginput, values, lastplanworld, planworld, behavior, plan, Time = Step()
        updateloc()
    plot_pattern(observed_world[BOARD], observed_world[VALUES])
    frame += 1

def GUI_RUN():
    global fig, ax
    fig, ax = plt.subplots()
    try:
        plt.rcParams['keymap.save'].remove('s')
    except:
        None
    try:
        plt.rcParams['keymap.quit'].remove('q')
    except:
        None
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

