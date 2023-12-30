import random
from copy import deepcopy
from constants import *


loc = (2, 4)

world = None
observed_world = None
slippery = False

width, height = None, None
actions = None

t = None

# THE WORLDS
world1 = """
oooooooooooo
o   o   f  o
o          o
o   oooooooo
o x        o
o       u  o
oooooooooooo
"""
world2 = """
oooooooooooo
o          o
o   u      o
o     ooooTo
o x        o
o          o
oooooooooooo
"""
world3 = """
oooooooooooo
o  k  o    o
o     D b ko
o     oooooo
o x   D b ko
o     o    o
oooooooooooo
"""
world4 = """
oooooooooooo
o   o   f  o
o          o
o   oooooooo
o x v      o
o       u  o
oooooooooooo
"""
world5 = """
oooooooooooo
oo          
oo          
oo         c
oox         
oo          
oooooooooooo
"""


def choose_world(challenge):
    global world, actions, observed_world, width, height
    isWorld5 = False
    if "1" in challenge:
        world = world1
    if "2" in challenge:
        world = world2
    if "3" in challenge:
        world = world3
    if "4" in challenge:
        world = world4
    if "5" in challenge:
        world = world5
        isWorld5 = True
    world = [[[*x] for x in world[1:-1].split("\n")], tuple([0, 0])]
    if isWorld5:
        actions = [up, down, left]
    else:
        actions = [left, right, up, down]

    height, width = (len(world[BOARD]), len(world[BOARD][0]))
    world.append([[float("inf") for i in range(width)] for j in range(height)])
    observed_world = [[[" " for x in world[BOARD][i]]
                       for i in range(len(world[BOARD]))], world[VALUES], world[TIMES]]


# MOVE FUNCTIONS TAKING WALLS INTO ACCOUNT
def left(loc):
    return (loc[0]-1, loc[1])


def right(loc):
    return (loc[0]+1, loc[1])


def up(loc):
    return (loc[0], loc[1]-1)


def down(loc):
    return (loc[0], loc[1]+1)


def move(world, action):
    global loc
    if slippery and random.random() > 0.9:  # agent still believes it did the proper action
        action = random.choice(actions)  # but the world is slippery!
    newloc = action(loc)
    oldworld = deepcopy(world)
    # ROBOT MOVEMENT ON FREE SPACE
    if oldworld[BOARD][newloc[1]][newloc[0]] == FREE:
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
                    xr, yr = (random.randint(0, width-1),
                              random.randint(0, height-1))
                    if oldworld[BOARD][yr][xr] == FREE:
                        world[BOARD][yr][xr] = CUP
                        break
    # CUP
    if world[BOARD][newloc[1]][newloc[0]] == CUP:  # an object the system could shift around
        world[BOARD][loc[1]][loc[0]] = CUP
        loc = newloc
        world[BOARD][loc[1]][loc[0]] = ROBOT
    # KEY
    if world[BOARD][newloc[1]][newloc[0]] == KEY:
        world[BOARD][loc[1]][loc[0]] = FREE
        loc = newloc
        world[BOARD][loc[1]][loc[0]] = ROBOT
        # the second value +1 and the rest stays
        world[VALUES] = tuple([world[VALUES][0]] +
                              [world[VALUES][1] + 1] + list(world[VALUES][2:]))
    # DOOR
    if world[BOARD][newloc[1]][newloc[0]] == DOOR and world[VALUES][1] > 0:
        world[BOARD][loc[1]][loc[0]] = FREE
        loc = newloc
        world[BOARD][loc[1]][loc[0]] = ROBOT
        # the second value +1 and the rest stays
        world[VALUES] = tuple([world[VALUES][0]] +
                              [world[VALUES][1] - 1] + list(world[VALUES][2:]))
    # BALL
    if oldworld[BOARD][newloc[1]][newloc[0]] == BALL:
        world[BOARD][loc[1]][loc[0]] = FREE
        loc = newloc
        world[BOARD][loc[1]][loc[0]] = ROBOT
        # the first value +1 and the rest stays
        world[VALUES] = tuple([world[VALUES][0] + 1] + list(world[VALUES][1:]))
    # BATTERY
    if world[BOARD][newloc[1]][newloc[0]] == BATTERY:
        world[BOARD][loc[1]][loc[0]] = FREE
        loc = newloc
        world[BOARD][loc[1]][loc[0]] = ROBOT
        # the first value +1 and the rest stays
        world[VALUES] = tuple([world[VALUES][0] + 1] + list(world[VALUES][1:]))
    # FOOD
    if world[BOARD][newloc[1]][newloc[0]] == FOOD:
        world[BOARD][loc[1]][loc[0]] = FREE
        loc = newloc
        world[BOARD][loc[1]][loc[0]] = ROBOT
        # the first value +1 and the rest stays
        world[VALUES] = tuple([world[VALUES][0] + 1] + list(world[VALUES][1:]))
        while True:
            x, y = (random.randint(0, width-1), random.randint(0, height-1))
            if world[BOARD][y][x] == FREE:
                world[BOARD][y][x] = FOOD
                break
    # FREE SPACE
    if world[BOARD][newloc[1]][newloc[0]] == FREE or world[BOARD][newloc[1]][newloc[0]] == BALL:
        world[BOARD][loc[1]][loc[0]] = FREE
        loc = newloc
        world[BOARD][loc[1]][loc[0]] = ROBOT
    return [world[BOARD], world[VALUES], world[TIMES]]


def motorbabbling():
    return random.choice(actions)


def localObserve(world):
    global observed_world, loc
    for y in range(VIEWDISTY*2+1):
        for x in range(VIEWDISTX*2+1):
            Y = loc[1]+y-VIEWDISTY
            X = loc[0]+x-VIEWDISTX
            if Y >= 0 and Y < height and \
               X >= 0 and X < width:
                observed_world[BOARD][Y][X] = world[BOARD][Y][X]
                observed_world[TIMES][Y][X] = t
    observed_world[VALUES] = deepcopy(world[VALUES])
