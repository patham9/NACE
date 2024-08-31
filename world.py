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
oooooooooooo
o          o
o     u    o
o  T     G o
o x   H    o
o          o
oooooooooooo
"""
_worldminus1 = """
oooooooooooo
ozb  o toooo
oz t 0   boo
o 0  o to oo
ooxooo0oo oo
oo obzt   oo
oooooooooooo
"""
_world0 = """
oooooooooooo
o          o
oo oooooo oo
o    f     o
o x     o  o
o          o
oooooooooooo
"""
_world_empty = """
            
            
            
            
            
            
            
            
            
            
            
"""
_world_empty_large = """
                         
                         
                         
                         
                         
                         
                         
                         
                         
                         
                         
                         
                         
                         
                         
                         
                         
                         
                         
                         
                         
                         
                         
                         
                         
"""


_challenge_input = ""
for arg in sys.argv:
    if arg.startswith("world="):
        _challenge_input = arg.split("world=")[1]
#Description for world choice
if "manual" in sys.argv:
    if _challenge_input == "":
        print("Enter one of 1-9 to try a world:")
else:
    print("""
Food collecting (1),
cup on table challenge (2),
doors and keys (3),
food collecting with moving object (4),
pong (5),
bring eggs to chicken (6),
soccer (7),
shock world (8),

NEW WORLDS:
Puzzleworld (-1) "minus 1 indeed"
Minigrid worlds (11-20, interesting), (30-37, empty grid)
world with MeTTa-Narsese console input demanding MeTTa-NARS installation (9),
Input the corresponding world number and press enter:
""")
if _challenge_input == "":
    _challenge = input()
else:
    _challenge = _challenge_input
#print('Slippery ground y/n (n default)? Causes the chosen action to have the consequence of another action in 10% of cases.')
_slippery = "slippery" in sys.argv
_isWorld5 = False
_isWorld9 = False
_isWorld0 = False
def getIsWorld9():
    return _isWorld9
def getIsWorld0():
    return _isWorld0

#Whether there is a cup on the table (user-given goal demo)
def World_CupIsOnTable(world):
    for x in range(width):
        for y in range(height-1):
            if world[BOARD][y+1][x] == 'T' and world[BOARD][y][x] == 'u':
                return True
    return False

World_objective = None
if "2" == _challenge:
    world = _world2
    World_objective = World_CupIsOnTable
if "3" == _challenge:
    world = _world3
if "4" == _challenge:
    world = _world4
if "5" == _challenge:
    world = _world5
    _isWorld5 = True
if "6" == _challenge:
    world = _world6
if "7" == _challenge:
    world = _world7
if "8" == _challenge:
    world = _world8
if "9" == _challenge:
    world = _world9
    _isWorld9 = True
if "-1" == _challenge:
    world = _worldminus1
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

episode_id = 0
run_id = -1
episodes = -1
max_steps = -1 #1000
evalsteps = -1
step = 0
totalstep = 0
seed = -1
for arg in sys.argv:
    if arg.startswith("maxsteps="):
        max_steps = int(arg.split("maxsteps=")[1])
    if arg.startswith("runid="):
        run_id = int(arg.split("runid=")[1])
        seed = run_id - 1
    if arg.startswith("evalsteps="):
        evalsteps = int(arg.split("evalsteps=")[1])
    if arg.startswith("episodes="):
        episodes = int(arg.split("episodes=")[1])
def minigrid_digest(state):
    global direction, loc, lastimage, lastreward, step, totalstep
    step += 1
    totalstep += 1
    #print(state[0]["direction"]); exit(0)
    direction = state[0]["direction"]
    #print(state[0]['image'].shape); exit(0)
    loc = env.agent_pos
    lastimage = state[0]["image"]
    if len(state) == 5 and (lastreward == 0 or lastreward == None) and state[1] != 0:
        lastreward = state[1]
        reward = state[1]

worldstr = "MiniGrid-DoorKey-8x8-v0"
if "0" == _challenge:
    world = _world0
    _isWorld0 = True
if "11" == _challenge:
    worldstr = "BabyAI-GoToRedBallNoDists-v0"
if "12" == _challenge:
    worldstr = "MiniGrid-DistShift2-v0"
if "13" == _challenge:
    worldstr = "MiniGrid-LavaGapS7-v0"
if "14" == _challenge:
    worldstr = "MiniGrid-SimpleCrossingS11N5-v0"
if "15" == _challenge:
    worldstr = "MiniGrid-LavaCrossingS11N5-v0"
if "16" == _challenge:
    worldstr = "MiniGrid-Unlock-v0"
if "17" == _challenge:
    worldstr = "MiniGrid-DoorKey-8x8-v0"
if "18" == _challenge:
    worldstr = "MiniGrid-UnlockPickup-v0"
if "19" == _challenge:
    worldstr = "MiniGrid-BlockedUnlockPickup-v0"
if "20" == _challenge: #EXT 1
    worldstr = "MiniGrid-DoorKey-16x16-v0"
    _world_empty = _world_empty_large
if "30" == _challenge:
    worldstr = "MiniGrid-Empty-6x6-v0"
    _challenge = "10"
if "31" == _challenge:
    worldstr = "MiniGrid-Empty-8x8-v0"
    _challenge = "10"
if "32" == _challenge:
    worldstr = "MiniGrid-Empty-16x16-v0"
    _world_empty = _world_empty_large
    _challenge = "10"
if "33" == _challenge:
    worldstr = "MiniGrid-Empty-Random-5x5-v0"
    _challenge = "10"
if "34" == _challenge:
    worldstr = "MiniGrid-Empty-Random-6x6-v0"
    _challenge = "10"
if "35" == _challenge:
    worldstr = "MiniGrid-FourRooms-v0"
    _world_empty = _world_empty_large
    _challenge = "10"
if "36" == _challenge:
    worldstr = "MiniGrid-MultiRoom-N6-v0"
    _world_empty = _world_empty_large
    _challenge = "10"
if "37" == _challenge:
    worldstr = "MiniGrid-SimpleCrossingS9N2"

isMinigridWorld = int(_challenge) >= 10 #Minigrid challenges start at that index
def getisMinigridWorld():
    return isMinigridWorld

if isMinigridWorld: #"9" in _challenge:
    import gymnasium as gym
    from minigrid.wrappers import *
    _isWorld5 = False #TODO
    direction = dir_down
    if "nominigrid" not in sys.argv:
        if max_steps != -1:
            env = gym.make(worldstr, render_mode='human', max_steps=max_steps)
        else:
            env = gym.make(worldstr, render_mode='human')
            max_steps = env.max_steps
            if max_steps == 0:
                max_steps = 256
                env = gym.make(worldstr, render_mode='human', max_steps=max_steps)
    else:
        if max_steps != -1:
            env = gym.make(worldstr, max_steps=max_steps)
        else:
            env = gym.make(worldstr)
            max_steps = env.max_steps
            if max_steps == 0:
                max_steps = 256
                env = gym.make(worldstr, render_mode='human', max_steps=max_steps)
    for arg in sys.argv:
        if arg.startswith("seed="):
            seed = int(arg.split("seed=")[1])
        if seed != -1:
            observation_reward_and_whatever = env.reset(seed=seed)
        else:
            observation_reward_and_whatever = env.reset()
    minigrid_digest(observation_reward_and_whatever)
    print("Observation:", observation_reward_and_whatever)
    if "nominigrid" not in sys.argv:
        env.render()
    world = _world_empty
    loc = env.agent_pos
VIEWDISTX, VIEWDISTY = (3, 2)
TRASH, HUMAN,COFFEEMACHINE, WALL, ROBOT, CUP, FOOD, BATTERY, FREE, TABLE, GOAL, KEY, DOOR, ARROW_DOWN, ARROW_UP, BALL, EGG, EGGPLACE, CHICKEN, SBALL, SHOCK  = \
      ('t', 'w','G', 'o', 'x', 'u', 'f', 'b', ' ', 'T', 'H', 'k', 'D', 'v', '^', 'c', 'O', '_', '4', '0', 'z')
world=[[[*x] for x in world[1:-1].split("\n")], tuple([0, 0])]
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

def pick(loc):
    return loc
def drop(loc):
    return loc
def toggle(loc):
    return loc

lastseen = set([])

def help(action):
    if action != drop:
        minigrid_digest(env.step(action_toggle))
        minigrid_digest(env.step(action_pick))

def cntEntry(world, VAL):
    cnt = 0
    for y in range(height):
        for x in range(width):
            if world[BOARD][y][x] == VAL:
                cnt += 1
    return cnt

hasReset = 0
resetscore = 0
acummulatedScore = 0
lastevaltime = -1
lastseed = seed

#Applies the effect of the movement operations, considering how different grid cell types interact with each other
def World_Move(loc, world, action):
    global lastseen, lastreward, hasReset, resetscore, acummulatedScore, step, episode_id, lastevaltime, seed, lastseed
    lastseen = set([])
    lastreward = 0
    if env is not None:
        """if action == pick:
            minigrid_digest(env.step(action_pick))
            minigrid_digest(env.step(action_right))
            minigrid_digest(env.step(action_pick))
            minigrid_digest(env.step(action_right))
            minigrid_digest(env.step(action_pick))
            minigrid_digest(env.step(action_right))
            minigrid_digest(env.step(action_pick))
            minigrid_digest(env.step(action_right))
        if action == drop:
            minigrid_digest(env.step(action_drop))
            minigrid_digest(env.step(action_right))
            minigrid_digest(env.step(action_drop))
            minigrid_digest(env.step(action_right))
            minigrid_digest(env.step(action_drop))
            minigrid_digest(env.step(action_right))
            minigrid_digest(env.step(action_drop))
            minigrid_digest(env.step(action_right))
        if action == toggle:
            minigrid_digest(env.step(action_toggle))
            minigrid_digest(env.step(action_right))
            minigrid_digest(env.step(action_toggle))
            minigrid_digest(env.step(action_right))
            minigrid_digest(env.step(action_toggle))
            minigrid_digest(env.step(action_right))
            minigrid_digest(env.step(action_toggle))
            minigrid_digest(env.step(action_right))"""


        if action == drop: #drop below always
            if direction == dir_down:
                help(action);minigrid_digest(env.step(action_drop))
            elif direction == dir_left:
                minigrid_digest(env.step(action_left))
                help(action);minigrid_digest(env.step(action_drop))
            elif direction == dir_right:
                minigrid_digest(env.step(action_right))
                help(action);minigrid_digest(env.step(action_drop))
            elif direction == dir_up:
                minigrid_digest(env.step(action_right))
                minigrid_digest(env.step(action_right))
                help(action);minigrid_digest(env.step(action_drop))
        if action == left:
            if direction == dir_left:
                help(action);minigrid_digest(env.step(action_forward))
            if direction == dir_down:
                minigrid_digest(env.step(action_right))
                help(action);minigrid_digest(env.step(action_forward))
            if direction == dir_up:
                minigrid_digest(env.step(action_left))
                help(action);minigrid_digest(env.step(action_forward))
            if direction == dir_right:
                minigrid_digest(env.step(action_right))
                minigrid_digest(env.step(action_right))
                help(action);minigrid_digest(env.step(action_forward))
            """if lastActionIsPick:
                minigrid_digest(env.step(action_pick))
            if lastActionIsDrop:
                minigrid_digest(env.step(action_drop))
            if lastActionIsToggle:
                minigrid_digest(env.step(action_toggle))"""
        if action == right:
            if direction == dir_right:
                help(action);minigrid_digest(env.step(action_forward))
            if direction == dir_down:
                minigrid_digest(env.step(action_left))
                help(action);minigrid_digest(env.step(action_forward))
            if direction == dir_up:
                minigrid_digest(env.step(action_right))
                help(action);minigrid_digest(env.step(action_forward))
            if direction == dir_left:
                minigrid_digest(env.step(action_right))
                minigrid_digest(env.step(action_right))
                help(action);minigrid_digest(env.step(action_forward))
            """if lastActionIsPick:
                minigrid_digest(env.step(action_pick))
            if lastActionIsDrop:
                minigrid_digest(env.step(action_drop))
            if lastActionIsToggle:
                minigrid_digest(env.step(action_toggle))"""
        if action == up:
            if direction == dir_up:
                help(action);minigrid_digest(env.step(action_forward))
            if direction == dir_right:
                minigrid_digest(env.step(action_left))
                help(action);minigrid_digest(env.step(action_forward))
            if direction == dir_left:
                minigrid_digest(env.step(action_right))
                help(action);minigrid_digest(env.step(action_forward))
            if direction == dir_down:
                minigrid_digest(env.step(action_right))
                minigrid_digest(env.step(action_right))
                help(action);minigrid_digest(env.step(action_forward))
            """if lastActionIsPick:
                minigrid_digest(env.step(action_pick))
            if lastActionIsDrop:
                minigrid_digest(env.step(action_drop))
            if lastActionIsToggle:
                minigrid_digest(env.step(action_toggle))"""
        if action == down:
            if direction == dir_down:
                help(action);minigrid_digest(env.step(action_forward))
            if direction == dir_right:
                minigrid_digest(env.step(action_right))
                help(action);minigrid_digest(env.step(action_forward))
            if direction == dir_left:
                minigrid_digest(env.step(action_left))
                help(action);minigrid_digest(env.step(action_forward))
            if direction == dir_up:
                minigrid_digest(env.step(action_right))
                minigrid_digest(env.step(action_right))
                help(action);minigrid_digest(env.step(action_forward))
            """if lastActionIsPick:
                minigrid_digest(env.step(action_pick))
            if lastActionIsDrop:
                minigrid_digest(env.step(action_drop))
            if lastActionIsToggle:
                minigrid_digest(env.step(action_toggle))"""
        #help(action)
        newloc = env.agent_pos
        oldworld = deepcopy(world)

        M = {(1,0): FREE, (2,0): WALL, (4,0): FREE, (4,1): FREE, (4,2): DOOR, (5,0): KEY, (6,0): BALL, (7,0): TABLE, (8,0): GOAL, (9,0): SHOCK}
        for i in range(7):
            for j in reversed(range(7)):
                if lastimage[i,j][0] == 0:
                    break
                if direction == dir_right:
                    X = newloc[0] + (7-(j+1))
                    Y = newloc[1] + i - 3
                    lastseen.add((Y,X))
                    #print(lastimage); exit(0)
                    V = (lastimage[i,j][0], lastimage[i,j][2])
                    if V[0] != 0 and Y >= 0 and X >= 0 and Y < height and X < width:
                        #print("!!!", (X,Y), (i,j), V)
                        world[BOARD][Y][X] = M[V]
                if direction == dir_left:
                    X = newloc[0] - (7-(j+1))
                    Y = newloc[1] - i + 3
                    #print(lastimage); exit(0)
                    lastseen.add((Y,X))
                    V = (lastimage[i,j][0], lastimage[i,j][2])
                    if V[0] != 0 and Y >= 0 and X >= 0 and Y < height and X < width:
                        #print("!!!", (X,Y), (i,j), V)
                        world[BOARD][Y][X] = M[V]

                if direction == dir_up:
                    Y = newloc[1] - (7-(j+1))
                    X = newloc[0] + i - 3
                    #print(lastimage); exit(0)
                    lastseen.add((Y,X))
                    V = (lastimage[i,j][0], lastimage[i,j][2])
                    if V[0] != 0 and Y >= 0 and X >= 0 and Y < height and X < width:
                        #print("!!!", (X,Y), (i,j), V)
                        world[BOARD][Y][X] = M[V]
                if direction == dir_down:
                    Y = newloc[1] + (7-(j+1))
                    X = newloc[0] - i + 3
                    #print(lastimage); exit(0)
                    lastseen.add((Y,X))
                    V = (lastimage[i,j][0], lastimage[i,j][2])
                    if V[0] != 0 and Y >= 0 and X >= 0 and Y < height and X < width:  
                        #print("!!!", (X,Y), (i,j), V)
                        world[BOARD][Y][X] = M[V]
        world[BOARD][loc[1]][loc[0]] = FREE
        world[BOARD][newloc[1]][newloc[0]] = ROBOT
        loc = newloc
        i_inventory = 3
        j_inventory = 6
        V_inventory = lastimage[i_inventory,j_inventory][0]
        if (cntEntry(oldworld, TABLE) > cntEntry(world, TABLE)) or \
           (cntEntry(oldworld, GOAL) > cntEntry(world, GOAL)) or \
           (cntEntry(oldworld, SHOCK) > cntEntry(world, SHOCK)) or lastreward != 0:
            if lastreward > 0 or (cntEntry(oldworld, TABLE) > cntEntry(world, TABLE)) or (cntEntry(oldworld, GOAL) > cntEntry(world, GOAL)):
                lastreward = 1 #minigrid is not giving so we provide own reward
            else:
                lastreward = -1
            episode_id += 1
            acummulatedScore += lastreward
            world[VALUES] = (acummulatedScore, V_inventory)
            hasReset = 2 #ugly double reset hack is needed
            resetscore = world[VALUES][0]
            lastseed = seed
            if seed != -1:
                #Ali used seed 0-4, so we also alternate between these seeds:
                seed += 1
                if seed > 4:
                    seed = 0
            if seed != -1:
                minigrid_digest(env.reset(seed=seed))
            else:
                minigrid_digest(env.reset())
            if run_id != -1 and lastreward != 0:
                reward = 1 - 0.9 * (step / max_steps)
                if lastreward < 0:
                    reward = -1
                if (episodes != -1 and episode_id < episodes) or \
                   (evalsteps != -1 and totalstep < evalsteps):
                    eval_time = int(totalstep/100)*100+100
                    if lastevaltime == -1 and episodes == -1:
                        for missed_time in range(0, eval_time-100, 100):
                            with open("run_world"+str(_challenge_input)+"_"+str(run_id)+".run", "a") as f:
                                f.write(f"episode_id={0} timesteps={missed_time+100} length={max_steps} reward={0.0} seed={lastseed}\n")
                    if lastevaltime != eval_time or episodes != -1:
                        lastevaltime = eval_time
                        with open("run_world"+str(_challenge_input)+"_"+str(run_id)+".run", "a") as f:
                            f.write(f"episode_id={episode_id} timesteps={eval_time} length={step} reward={reward} seed={lastseed}\n")
                    if eval_time == evalsteps:
                        exit(0) #no need to evaluate further
                if episodes != -1 and episode_id >= episodes:
                    exit(0)
                if evalsteps != -1 and totalstep >= evalsteps:
                    exit(0)
                step = 0
        else:
            acummulatedScore += lastreward
            world[VALUES] = (acummulatedScore, V_inventory)
        return loc, [world[BOARD], world[VALUES], world[TIMES]]
    if _slippery and random.random() > 0.9: #agent still believes it did the proper action
        action = random.choice(actions)    #but the world is slippery!
    newloc = action(loc)
    oldworld = deepcopy(world)
    #ROBOT MOVEMENT ON FREE SPACE
    movedAgent = False
    if oldworld[BOARD][newloc[1]][newloc[0]] == FREE:
        world[BOARD][loc[1]][loc[0]] = FREE
        loc = newloc
        world[BOARD][loc[1]][loc[0]] = ROBOT
        movedAgent = True
    oldoldworld = deepcopy(oldworld)
    oldworld = deepcopy(world)
    for y in range(height):
        for x in range(width):
            if oldworld[BOARD][y][x] == BALL and world[BOARD][y][x-1] == FREE and oldoldworld[BOARD][y][x-1] == FREE:
                world[BOARD][y][x-1] = BALL
                world[BOARD][y][x] = FREE
            if oldworld[BOARD][y][x] == BALL and oldworld[BOARD][y][x-1] == WALL:
                world[BOARD][y][x] = FREE
                world[BOARD][random.choice(range(1, height-1))][width-1] = BALL
            if oldworld[BOARD][y][x] == BALL and oldoldworld[BOARD][y][x-1] == ROBOT:
                world[BOARD][y][x] = FREE
                world[BOARD][random.choice(range(1, height-1))][width-1] = BALL
                if not movedAgent:
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
                if not _isWorld9:
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
    #TRASH
    if world[BOARD][newloc[1]][newloc[0]] == TRASH:
        world[BOARD][loc[1]][loc[0]] = FREE
        loc = newloc
        world[BOARD][loc[1]][loc[0]] = ROBOT
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
        if world[BOARD][crateloc[1]][crateloc[0]] == FREE or world[BOARD][crateloc[1]][crateloc[0]] == SHOCK:
            if world[BOARD][newloc[1]][newloc[0]] == SBALL:
                world[BOARD][loc[1]][loc[0]] = FREE
                loc = newloc
                world[BOARD][loc[1]][loc[0]] = ROBOT
                if world[BOARD][crateloc[1]][crateloc[0]] == SHOCK:
                     world[BOARD][crateloc[1]][crateloc[0]] = FREE
                else:
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

def World_Criteria(world):
    return World_objective(world)

def World_SetObjective(func):
    global World_objective
    World_objective = func

def World_GetObjective():
    return World_objective

#Print the world into the terminal
def World_Print(world):
    for line in world[BOARD]:
        print("".join(line))

#The limited field of view the agent can observe dependent on view distance (partial observability)
def World_FieldOfView(Time, loc, observed_world, world):
    global hasReset
    for Y in range(height):
        for X in range(width):
            if observed_world[TIMES][Y][X] == Time:
                observed_world[TIMES][Y][X] = Time - 1 #WHY can this ever happen??? DEBUG!
    if env is None:
        for y in range(VIEWDISTY*2+1):
            for x in range(VIEWDISTX*2+1):
                Y = loc[1]+y-VIEWDISTY
                X = loc[0]+x-VIEWDISTX
                if Y >= 0 and Y < height and \
                   X >= 0 and X < width:
                    observed_world[BOARD][Y][X] = world[BOARD][Y][X]
                    observed_world[TIMES][Y][X] = Time
    else:
        if hasReset > 0:
            world[VALUES] = (resetscore, 0)
            for y in range(height):
                for x in range(width):
                    observed_world[BOARD][y][x] = '.'
                    world[BOARD][y][x] = FREE
                    observed_world[TIMES][y][x] = Time - 1000
            observed_world[VALUES] = (resetscore, 0)
            world[VALUES] = (resetscore, 0)
            hasReset -= 1
            #PRINT("RESET!!!!!!!!!!!!")
            return observed_world
        for Y in range(height):
            for X in range(width):
                if observed_world[BOARD][Y][X] == ROBOT:
                    observed_world[BOARD][Y][X] = FREE
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
    actions = [up, down, right]
    VIEWDISTX, VIEWDISTY = (4, 3)
if isMinigridWorld and int(_challenge) >= 16 and int(_challenge) < 30:
    actions = [left, right, up, down, drop] #, pick, drop, toggle]
def World_Num5():
    return _isWorld5
