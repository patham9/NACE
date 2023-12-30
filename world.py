import random
from copy import deepcopy
import numpy as np
from constants import *
from NACE.World import World, WorldNode

loc = (2, 4)

world: World = None
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
    world = [np.array([[*x] for x in world[1:-1].split("\n")]), tuple([0, 0])]
    if isWorld5:
        actions = [World.up, World.down, World.left]
    else:
        actions = [World.left, World.right, World.up, World.down]

    height, width = (len(world[BOARD]), len(world[BOARD][0]))
    world.append(np.array([[float("inf") for i in range(width)] for j in range(height)]))
    world = World(world[BOARD], world[VALUES], world[TIMES], loc, slippery, actions)
    observed_world = WorldNode(np.array([[" " for x in world[BOARD][i]]
                       for i in range(len(world[BOARD]))]), world[VALUES], world[TIMES], world.loc_robot)
    # observed_world = [[[" " for x in world[BOARD][i]]
    #                    for i in range(len(world[BOARD]))], world[VALUES], world[TIMES]]


# MOVE FUNCTIONS TAKING WALLS INTO ACCOUNT
def left(loc): pass
def right(loc): pass
def up(loc): pass
def down(loc): pass
def move(world, action): pass


left = World.left
right = World.right
up = World.up
down = World.down
move = World.move


def localObserve(world: World):
    global observed_world
    loc = world.loc_robot
    for y in range(VIEWDISTY*2+1):
        for x in range(VIEWDISTX*2+1):
            Y = loc[1]+y-VIEWDISTY
            X = loc[0]+x-VIEWDISTX
            if Y >= 0 and Y < height and \
               X >= 0 and X < width:
                observed_world[BOARD][Y][X] = world[BOARD][Y][X]
                observed_world[TIMES][Y][X] = t
    observed_world[VALUES] = deepcopy(world[VALUES])
