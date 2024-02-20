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
import random
from copy import deepcopy

#The worlds:
world = """
oooooooooooo
o   o   f  o
o          o
o   oooooooo
o x        o
o       u  o
oooooooooooo
"""
_world2 = """
oooooooooooo
o          o
o   u      o
o     ooooTo
o x        o
o          o
oooooooooooo
"""
_world3 = """
oooooooooooo
o   k o   ko
o     D b  o
o     oooooo
o x   D b  o
o     o   ko
oooooooooooo
"""
_world4 = """
oooooooooooo
o  vo   f  o
o          o
o   oooooooo
o x        o
o       u  o
oooooooooooo
"""
_world5 = """
oooooooooooo
oo          
oo          
oo         c
oox         
oo          
oooooooooooo
"""
_world6 = """
oooooooooooo
o O  4  O  o
o          o
o          o
o x  O  O  o
o          o
oooooooooooo
"""
_world7 = """
oooooooooooo
o          o
o  0 0     o
o       H  o
o x0 0     o
o          o
oooooooooooo
"""
_world8 = """
oooooooooooo
o     zzzzzo
o f z z    o
o   z z zz o
o x z z z  o
o   z   z  o
oooooooooooo
"""
_world9 = """
            
            
            
            
            
            
            
            
"""

_challenge_input = ""
for arg in sys.argv:
    if arg.startswith("world="):
        _challenge_input = arg.split("world=")[1]
_slippery_input = ""
for arg in sys.argv:
    if arg.startswith("slippery="):
        _slippery_input = arg.split("slippery=")[1]
#Description for world choice
if "manual" in sys.argv:
    print("Enter one of 1-7 to try a world:")
else:
    print('Food collecting (1), cup on table challenge (2), doors and keys (3), food collecting with moving object (4), pong (5), bring eggs to chicken (6), soccer (7), shock world (8), input "1", "2", "3", "4", "5", "6", or "7":')
if _challenge_input == "":
    _challenge = input()
else:
    _challenge = _challenge_input
print('Slippery ground y/n (n default)? Causes the chosen action to have the consequence of another action in 10% of cases.')
if _slippery_input == "":
    _slippery = "y" in input()
else:
    _slippery = "y" in _slippery_input
_isWorld5 = False
if "2" in _challenge:
    world = _world2
if "3" in _challenge:
    world = _world3
if "4" in _challenge:
    world = _world4
if "5" in _challenge:
    world = _world5
    _isWorld5 = True
if "6" in _challenge:
    world = _world6
if "7" in _challenge:
    world = _world7
if "8" in _challenge:
    world = _world8
#World states:
loc = (2,4)
env = None
dir_right = 0
dir_down = 1
dir_left = 2
dir_up = 3
action_left = 0
action_right = 1
action_forward = 2
action_pick = 3
action_drop = 4
action_toggle = 5
direction = None
env = None
lastimage = None
lastreward = None

def minigrid_digest(state):
    global direction, loc, lastimage, lastreward
    #print(state[0]["direction"]); exit(0)
    direction = state[0]["direction"]
    #print(state[0]['image'].shape); exit(0)
    loc = env.agent_pos
    lastimage = state[0]["image"]
    if len(state) == 5 and (lastreward == 0 or lastreward == None):
        lastreward = state[1]

isWorld9 = False
if "9" in _challenge:
    import gymnasium as gym
    from minigrid.wrappers import *
    direction = dir_down
    env = gym.make("MiniGrid-BlockedUnlockPickup-v0", render_mode='human')
    observation_reward_and_whatever = env.reset()
    minigrid_digest(observation_reward_and_whatever)
    print("Observation:", observation_reward_and_whatever)
    env.render()
    world = _world9
    isWorld9 = True
    loc = env.agent_pos
VIEWDISTX, VIEWDISTY = (3, 2)
WALL, ROBOT, CUP, FOOD, BATTERY, FREE, TABLE, GOAL, KEY, DOOR, ARROW_DOWN, ARROW_UP, BALL, EGG, EGGPLACE, CHICKEN, SBALL, SHOCK  = \
      ('o', 'x', 'u', 'f', 'b', ' ', 'T', 'H', 'k', 'D', 'v', '^', 'c', 'O', '_', '4', '0', 'z')
initvals = tuple([0, 0])
#if "9" in _challenge:
#    initvals = tuple([0, 0, "none"])
world=[[[*x] for x in world[1:-1].split("\n")], initvals]

BOARD, VALUES, TIMES = (0, 1, 2)
height, width = (len(world[BOARD]), len(world[BOARD][0]))
world.append([[float("-inf") for i in range(width)] for j in range(height)])

#Move operations to move the agent in the world:
def left(loc):
    return (loc[0]-1, loc[1])

def right(loc):
    if _isWorld5:
        return loc
    return (loc[0]+1, loc[1])

def up(loc):
    return (loc[0],   loc[1]-1)

def down(loc):
    return (loc[0],   loc[1]+1)

def pick(loc): return loc
def drop(loc): return loc
def toggle(loc): return loc

def pick_left(loc): return loc
def drop_left(loc): return loc
def toggle_left(loc): return loc

def pick_right(loc): return loc
def drop_right(loc): return loc
def toggle_right(loc): return loc

def pick_up(loc): return loc
def drop_up(loc): return loc
def toggle_up(loc): return loc

def pick_down(loc): return loc
def drop_down(loc): return loc
def toggle_down(loc): return loc


lastseen = set([])

#Applies the effect of the movement operations, considering how different grid cell types interact with each other
def World_Move(loc, world, action):
    global lastseen, lastreward
    lastseen = set([])
    lastreward = 0
    ActionIsPick = action == pick_left or action == pick_right or action == pick_down or action == pick_up
    ActionIsDrop = action == drop_left or action == drop_right or action == drop_down or action == drop_up
    ActionIsToggle = action == toggle_left or action == toggle_right or action == toggle_down or action == toggle_up
    if env is not None:
        if action == left or action == pick_left or action == drop_left or action == toggle_left:
            if direction == dir_left:
                if ActionIsPick:
                    minigrid_digest(env.step(action_pick))
                elif ActionIsDrop:
                    minigrid_digest(env.step(action_drop))
                elif ActionIsToggle:
                    minigrid_digest(env.step(action_toggle))
                if True:
                    minigrid_digest(env.step(action_forward))
            if direction == dir_down:
                minigrid_digest(env.step(action_right))
                if ActionIsPick:
                    minigrid_digest(env.step(action_pick))
                elif ActionIsDrop:
                    minigrid_digest(env.step(action_drop))
                elif ActionIsToggle:
                    minigrid_digest(env.step(action_toggle))
                if True:
                    minigrid_digest(env.step(action_forward))
            if direction == dir_up:
                minigrid_digest(env.step(action_left))
                if ActionIsPick:
                    minigrid_digest(env.step(action_pick))
                elif ActionIsDrop:
                    minigrid_digest(env.step(action_drop))
                elif ActionIsToggle:
                    minigrid_digest(env.step(action_toggle))
                if True:
                    minigrid_digest(env.step(action_forward))
            if direction == dir_right:
                minigrid_digest(env.step(action_right))
                minigrid_digest(env.step(action_right))
                if ActionIsPick:
                    minigrid_digest(env.step(action_pick))
                elif ActionIsDrop:
                    minigrid_digest(env.step(action_drop))
                elif ActionIsToggle:
                    minigrid_digest(env.step(action_toggle))
                if True:
                    minigrid_digest(env.step(action_forward))
            """if ActionIsPick:
                minigrid_digest(env.step(action_pick))
            if ActionIsDrop:
                minigrid_digest(env.step(action_drop))
            if ActionIsToggle:
                minigrid_digest(env.step(action_toggle))"""
        if action == right or action == pick_right or action == drop_right or action == toggle_right:
            if direction == dir_right:
                if ActionIsPick:
                    minigrid_digest(env.step(action_pick))
                elif ActionIsDrop:
                    minigrid_digest(env.step(action_drop))
                elif ActionIsToggle:
                    minigrid_digest(env.step(action_toggle))
                if True:
                    minigrid_digest(env.step(action_forward))
            if direction == dir_down:
                minigrid_digest(env.step(action_left))
                if ActionIsPick:
                    minigrid_digest(env.step(action_pick))
                elif ActionIsDrop:
                    minigrid_digest(env.step(action_drop))
                elif ActionIsToggle:
                    minigrid_digest(env.step(action_toggle))
                if True:
                    minigrid_digest(env.step(action_forward))
            if direction == dir_up:
                minigrid_digest(env.step(action_right))
                if ActionIsPick:
                    minigrid_digest(env.step(action_pick))
                elif ActionIsDrop:
                    minigrid_digest(env.step(action_drop))
                elif ActionIsToggle:
                    minigrid_digest(env.step(action_toggle))
                if True:
                    minigrid_digest(env.step(action_forward))
            if direction == dir_left:
                minigrid_digest(env.step(action_right))
                minigrid_digest(env.step(action_right))
                if ActionIsPick:
                    minigrid_digest(env.step(action_pick))
                elif ActionIsDrop:
                    minigrid_digest(env.step(action_drop))
                elif ActionIsToggle:
                    minigrid_digest(env.step(action_toggle))
                if True:
                    minigrid_digest(env.step(action_forward))
            """if ActionIsPick:
                minigrid_digest(env.step(action_pick))
            if ActionIsDrop:
                minigrid_digest(env.step(action_drop))
            if ActionIsToggle:
                minigrid_digest(env.step(action_toggle))"""
        if action == up or action == pick_up or action == drop_up or action == toggle_up:
            if direction == dir_up:
                if ActionIsPick:
                    minigrid_digest(env.step(action_pick))
                elif ActionIsDrop:
                    minigrid_digest(env.step(action_drop))
                elif ActionIsToggle:
                    minigrid_digest(env.step(action_toggle))
                if True:
                    minigrid_digest(env.step(action_forward))
            if direction == dir_right:
                minigrid_digest(env.step(action_left))
                if ActionIsPick:
                    minigrid_digest(env.step(action_pick))
                elif ActionIsDrop:
                    minigrid_digest(env.step(action_drop))
                elif ActionIsToggle:
                    minigrid_digest(env.step(action_toggle))
                if True:
                    minigrid_digest(env.step(action_forward))
            if direction == dir_left:
                minigrid_digest(env.step(action_right))
                if ActionIsPick:
                    minigrid_digest(env.step(action_pick))
                elif ActionIsDrop:
                    minigrid_digest(env.step(action_drop))
                elif ActionIsToggle:
                    minigrid_digest(env.step(action_toggle))
                if True:
                    minigrid_digest(env.step(action_forward))
            if direction == dir_down:
                minigrid_digest(env.step(action_right))
                minigrid_digest(env.step(action_right))
                if ActionIsPick:
                    minigrid_digest(env.step(action_pick))
                elif ActionIsDrop:
                    minigrid_digest(env.step(action_drop))
                elif ActionIsToggle:
                    minigrid_digest(env.step(action_toggle))
                if True:
                    minigrid_digest(env.step(action_forward))
            """if ActionIsPick:
                minigrid_digest(env.step(action_pick))
            if ActionIsDrop:
                minigrid_digest(env.step(action_drop))
            if ActionIsToggle:
                minigrid_digest(env.step(action_toggle))"""
        if action == down or action == pick_down or action == drop_down or action == toggle_down:
            if direction == dir_down:
                if ActionIsPick:
                    minigrid_digest(env.step(action_pick))
                elif ActionIsDrop:
                    minigrid_digest(env.step(action_drop))
                elif ActionIsToggle:
                    minigrid_digest(env.step(action_toggle))
                if True:
                    minigrid_digest(env.step(action_forward))
            if direction == dir_right:
                minigrid_digest(env.step(action_right))
                if ActionIsPick:
                    minigrid_digest(env.step(action_pick))
                elif ActionIsDrop:
                    minigrid_digest(env.step(action_drop))
                elif ActionIsToggle:
                    minigrid_digest(env.step(action_toggle))
                if True:
                    minigrid_digest(env.step(action_forward))
            if direction == dir_left:
                minigrid_digest(env.step(action_left))
                if ActionIsPick:
                    minigrid_digest(env.step(action_pick))
                elif ActionIsDrop:
                    minigrid_digest(env.step(action_drop))
                elif ActionIsToggle:
                    minigrid_digest(env.step(action_toggle))
                if True:
                    minigrid_digest(env.step(action_forward))
            if direction == dir_up:
                minigrid_digest(env.step(action_right))
                minigrid_digest(env.step(action_right))
                if ActionIsPick:
                    minigrid_digest(env.step(action_pick))
                elif ActionIsDrop:
                    minigrid_digest(env.step(action_drop))
                elif ActionIsToggle:
                    minigrid_digest(env.step(action_toggle))
                if True:
                    minigrid_digest(env.step(action_forward))
            """if ActionIsPick:
                minigrid_digest(env.step(action_pick))
            if ActionIsDrop:
                minigrid_digest(env.step(action_drop))
            if ActionIsToggle:
                minigrid_digest(env.step(action_toggle))"""
        newloc = env.agent_pos
        oldworld = deepcopy(world)
        
        M = {1: FREE, 2: WALL, 4: DOOR, 5: KEY, 6: BALL, 7: FREE, 8: FOOD}
        for i in range(7):
            for j in reversed(range(7)):
                if lastimage[i,j][0] == 0:
                    break
                if direction == dir_right:
                    X = newloc[0] + (7-(j+1))
                    Y = newloc[1] + i - 3
                    lastseen.add((Y,X))
                    #print(lastimage); exit(0)
                    V = lastimage[i,j][0]
                    if V != 0:       
                        #print("!!!", (X,Y), (i,j), V)
                        world[BOARD][Y][X] = M[V]
                if direction == dir_left:
                    X = newloc[0] - (7-(j+1))
                    Y = newloc[1] - i + 3
                    #print(lastimage); exit(0)
                    lastseen.add((Y,X))
                    V = lastimage[i,j][0]
                    if V != 0:       
                        #print("!!!", (X,Y), (i,j), V)
                        world[BOARD][Y][X] = M[V]
                
                if direction == dir_up:
                    Y = newloc[1] - (7-(j+1))
                    X = newloc[0] + i - 3
                    #print(lastimage); exit(0)
                    lastseen.add((Y,X))
                    V = lastimage[i,j][0]
                    if V != 0:       
                        #print("!!!", (X,Y), (i,j), V)
                        world[BOARD][Y][X] = M[V]
                if direction == dir_down:
                    Y = newloc[1] + (7-(j+1))
                    X = newloc[0] - i + 3
                    #print(lastimage); exit(0)
                    lastseen.add((Y,X))
                    V = lastimage[i,j][0]
                    if V != 0:       
                        #print("!!!", (X,Y), (i,j), V)
                        world[BOARD][Y][X] = M[V]
        
        world[BOARD][loc[1]][loc[0]] = FREE
        world[BOARD][newloc[1]][newloc[0]] = ROBOT
        loc = newloc
        i_inventory = 3
        j_inventory = 6
        V_inventory = lastimage[i_inventory,j_inventory][0]
        """lastaction = "none"
        if action == pick:
            lastaction = pick
        elif action == drop:
            lastaction = drop
        elif action == toggle:
            lastaction = toggle"""
        world[VALUES] = (lastreward, V_inventory) #, lastaction)
        return loc, [world[BOARD], world[VALUES], world[TIMES]]
    
    
    if _slippery and random.random() > 0.9: #agent still believes it did the proper action
        action = random.choice(actions)    #but the world is slippery!
    newloc = action(loc)
    oldworld = deepcopy(world)
    #ROBOT MOVEMENT ON FREE SPACE
    if oldworld[BOARD][newloc[1]][newloc[0]] == FREE and (newloc[0] == width-1 or oldworld[BOARD][newloc[1]][newloc[0]+1] != BALL):
        world[BOARD][loc[1]][loc[0]] = FREE
        loc = newloc
        world[BOARD][loc[1]][loc[0]] = ROBOT
    oldworld = deepcopy(world)
    for y in range(height):
        for x in range(width):
            if oldworld[BOARD][y][x] == BALL and oldworld[BOARD][y][x-1] == FREE:
                world[BOARD][y][x-1] = BALL
                world[BOARD][y][x] = FREE
            if oldworld[BOARD][y][x] == BALL and oldworld[BOARD][y][x-1] == WALL:
                world[BOARD][y][x] = FREE
                world[BOARD][random.choice(range(1, height-1))][width-1] = BALL
            if oldworld[BOARD][y][x] == BALL and oldworld[BOARD][y][x-1] == ROBOT:
                world[BOARD][y][x] = FREE
                world[BOARD][random.choice(range(1, height-1))][width-1] = BALL
                world[VALUES] = tuple([world[VALUES][0] + 1] + list(world[VALUES][1:])) #the first value +1 and the rest stays
            if oldworld[BOARD][y][x] == ARROW_DOWN and oldworld[BOARD][y+1][x] == FREE:
                world[BOARD][y+1][x] = ARROW_DOWN
                world[BOARD][y][x] = FREE
            if oldworld[BOARD][y][x] == ARROW_UP and oldworld[BOARD][y-1][x] == FREE:
                world[BOARD][y-1][x] = ARROW_UP
                world[BOARD][y][x] = FREE
            if oldworld[BOARD][y][x] == ARROW_DOWN and oldworld[BOARD][y+1][x] == WALL:
                world[BOARD][y][x] = ARROW_UP
            if oldworld[BOARD][y][x] == ARROW_UP and oldworld[BOARD][y-1][x] == WALL:
                world[BOARD][y][x] = ARROW_DOWN
            if oldworld[BOARD][y][x] == CUP and oldworld[BOARD][y+1][x] == TABLE:
                world[BOARD][y][x] = FREE
                while True:
                    xr, yr = (random.randint(0, width-1), random.randint(0, height-1))
                    if oldworld[BOARD][yr][xr] == FREE:
                        world[BOARD][yr][xr] = CUP
                        break
    #CUP
    if world[BOARD][newloc[1]][newloc[0]] == CUP: #an object the system could shift around
        world[BOARD][loc[1]][loc[0]] = CUP
        loc = newloc
        world[BOARD][loc[1]][loc[0]] = ROBOT
    #KEY
    if world[BOARD][newloc[1]][newloc[0]] == KEY:
        world[BOARD][loc[1]][loc[0]] = FREE
        loc = newloc
        world[BOARD][loc[1]][loc[0]] = ROBOT
        world[VALUES] = tuple([world[VALUES][0]] + [world[VALUES][1] + 1] + list(world[VALUES][2:])) #the second value +1 and the rest stays
    #DOOR
    if world[BOARD][newloc[1]][newloc[0]] == DOOR and world[VALUES][1] > 0:
        world[BOARD][loc[1]][loc[0]] = FREE
        loc = newloc
        world[BOARD][loc[1]][loc[0]] = ROBOT
        world[VALUES] = tuple([world[VALUES][0]] + [world[VALUES][1] - 1] + list(world[VALUES][2:])) #the second value +1 and the rest stays
    #BATTERY
    if world[BOARD][newloc[1]][newloc[0]] == BATTERY:
        world[BOARD][loc[1]][loc[0]] = FREE
        loc = newloc
        world[BOARD][loc[1]][loc[0]] = ROBOT
        world[VALUES] = tuple([world[VALUES][0] + 1] + list(world[VALUES][1:])) #the first value +1 and the rest stays
    #SHOCK
    if world[BOARD][newloc[1]][newloc[0]] == SHOCK:
        world[BOARD][loc[1]][loc[0]] = FREE
        loc = newloc
        world[BOARD][loc[1]][loc[0]] = ROBOT
        world[VALUES] = tuple([world[VALUES][0] - 1] + list(world[VALUES][1:])) #the first value -1 and the rest stays
    #FOOD
    if world[BOARD][newloc[1]][newloc[0]] == FOOD:
        world[BOARD][loc[1]][loc[0]] = FREE
        loc = newloc
        world[BOARD][loc[1]][loc[0]] = ROBOT
        world[VALUES] = tuple([world[VALUES][0] + 1] + list(world[VALUES][1:])) #the first value +1 and the rest stays
        while True:
            x, y = (random.randint(0, width-1), random.randint(0, height-1))
            if world[BOARD][y][x] == FREE:
                world[BOARD][y][x] = FOOD
                break
    #EGG
    if world[BOARD][newloc[1]][newloc[0]] == EGG and world[VALUES][1] == 0: #can only carry 1
        world[BOARD][newloc[1]][newloc[0]] = EGGPLACE
        world[VALUES] = tuple([world[VALUES][0]] + [world[VALUES][1] + 1] + list(world[VALUES][2:]))
    elif world[BOARD][newloc[1]][newloc[0]] == EGGPLACE and world[VALUES][1] > 0:
        world[BOARD][newloc[1]][newloc[0]] = EGG
        world[VALUES] = tuple([world[VALUES][0]] + [world[VALUES][1] - 1] + list(world[VALUES][2:]))
    elif world[BOARD][newloc[1]][newloc[0]] == CHICKEN and world[VALUES][1] > 0:
        world[VALUES] = tuple([world[VALUES][0]] + [world[VALUES][1] - 1] + list(world[VALUES][2:]))
        world[VALUES] = tuple([world[VALUES][0] + 1] + list(world[VALUES][1:])) # 1 food
    #Football
    crateloc = action(newloc)
    if crateloc[1] < height and crateloc[0] < width and crateloc[1] >= 0 and crateloc[0] >= 0:
        if world[BOARD][crateloc[1]][crateloc[0]] == FREE:
            if world[BOARD][newloc[1]][newloc[0]] == SBALL:
                world[BOARD][loc[1]][loc[0]] = FREE
                loc = newloc
                world[BOARD][loc[1]][loc[0]] = ROBOT
                world[BOARD][crateloc[1]][crateloc[0]] = SBALL
        if world[BOARD][crateloc[1]][crateloc[0]] == GOAL and world[BOARD][newloc[1]][newloc[0]] == SBALL:
            world[BOARD][loc[1]][loc[0]] = FREE
            loc = newloc
            world[BOARD][newloc[1]][newloc[0]] = ROBOT
            world[VALUES] = tuple([world[VALUES][0] + 1] + list(world[VALUES][1:])) #the first value +1 and the rest stays
            while True:
                xr, yr = (random.randint(0, width-1), random.randint(0, height-1))
                if oldworld[BOARD][yr][xr] == FREE and xr > 1 and yr > 1 and xr < width-2 and yr < height-2 and \
                   oldworld[BOARD][yr+1][xr] == FREE and oldworld[BOARD][yr-1][xr] == FREE and \
                   oldworld[BOARD][yr][xr+1] == FREE and oldworld[BOARD][yr][xr-1] == FREE:
                    world[BOARD][yr][xr] = SBALL
                    break
    return loc, [world[BOARD], world[VALUES], world[TIMES]]

#Whether there is a cup on the table (user-given goal demo)
def World_CupIsOnTable(world):
    for x in range(width):
        for y in range(height-1):
            if world[BOARD][y+1][x] == 'T' and world[BOARD][y][x] == 'u':
                return True
    return False

#Print the world into the terminal
def World_Print(world):
    for line in world[BOARD]:
        print("".join(line))

#The limited field of view the agent can observe dependent on view distance (partial observability)
def World_FieldOfView(Time, loc, observed_world, world):
    """if env is not None:
        for y in range(height):
            for x in range(width):
                observed_world[BOARD][y][x] = world[BOARD][y][x]
                if (y,x) in lastseen:
                    observed_world[TIMES][y][x] = Time
        observed_world[VALUES] = deepcopy(world[VALUES])
        return observed_world"""
    for Y in range(height):
        for X in range(width):
            #if (Y, X) in lastseen:
            if observed_world[TIMES][Y][X] == Time:
                observed_world[TIMES][Y][X] = Time - 1 #WHY can this ever happen??? DEBUG!
            if observed_world[BOARD][Y][X] == ROBOT:
                observed_world[BOARD][Y][X] = FREE
                    #exit(0)
    for Y in range(height):
        for X in range(width):
            if (Y, X) in lastseen:
                if Y >= 0 and Y < height and \
                   X >= 0 and X < width:
                    observed_world[BOARD][Y][X] = world[BOARD][Y][X]
                    observed_world[TIMES][Y][X] = Time
    observed_world[VALUES] = deepcopy(world[VALUES])
    return observed_world

#The world component represented as an immutable tuple
def World_AsTuple(worldpart):
    return tuple(World_AsTuple(i) if isinstance(i, list) else i for i in worldpart)

#The actions the agent can take dependent on the chosen world:
actions = [left, right, up, down]
if _isWorld5:
    actions = [up, down, left]
    VIEWDISTX, VIEWDISTY = (4, 3)
if isWorld9:
    actions = [left, right, up, down, 
               pick_left, drop_left, toggle_left, 
               pick_right, drop_right, toggle_right,
               pick_up, drop_up, toggle_up,
               pick_down, drop_down, toggle_down]
