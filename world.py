import sys
import random
from copy import deepcopy

# THE WORLD
world = """
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
o  k  o   ko
o     D b  o
o     oooooo
o x   D b  o
o     o   ko
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
loc = (2,4)

print('Food collecting (1), cup on table challenge (2), doors and keys (3), food collecting with moving object (4), pong (5), input "1", "2", "3", "4", or "5":')
challenge = input()
print('Slippery ground y/n (n default)? Causes the chosen action to have the consequence of another action in 10% of cases.')
slippery = "y" in input()
isWorld5 = False
if "2" in challenge:
    world = world2
if "3" in challenge:
    world = world3
if "4" in challenge:
    world = world4
if "5" in challenge:
    world = world5
    isWorld5 = True

VIEWDISTX, VIEWDISTY = (3, 2)
WALL, ROBOT, CUP, FOOD, BATTERY, FREE, TABLE, KEY, DOOR, ARROW_DOWN, ARROW_UP, BALL = ('o', 'x', 'u', 'f', 'b', ' ', 'T', 'k', 'D', 'v', '^', 'c')
world=[[[*x] for x in world[1:-1].split("\n")], tuple([0, 0])]
BOARD, VALUES, TIMES = (0, 1, 2)
def printworld(world):
    for line in world[BOARD]:
        print("".join(line))
height, width = (len(world[BOARD]), len(world[BOARD][0]))
world.append([[float("-inf") for i in range(width)] for j in range(height)])

# MOVE FUNCTIONS TAKING WALLS INTO ACCOUNT
def left(loc):
    return (loc[0]-1, loc[1])
def right(loc):
    return (loc[0]+1, loc[1])
def up(loc):
    return (loc[0],   loc[1]-1)
def down(loc):
    return (loc[0],   loc[1]+1)
def move(loc, world, action):
    if slippery and random.random() > 0.9: #agent still believes it did the proper action
        action = random.choice(actions)    #but the world is slippery!
    newloc = action(loc)
    oldworld = deepcopy(world)
    #ROBOT MOVEMENT ON FREE SPACE
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
    #BALL
    if oldworld[BOARD][newloc[1]][newloc[0]] == BALL:
        world[BOARD][loc[1]][loc[0]] = FREE
        loc = newloc
        world[BOARD][loc[1]][loc[0]] = ROBOT
        world[VALUES] = tuple([world[VALUES][0] + 1] + list(world[VALUES][1:])) #the first value +1 and the rest stays
    #BATTERY
    if world[BOARD][newloc[1]][newloc[0]] == BATTERY:
        world[BOARD][loc[1]][loc[0]] = FREE
        loc = newloc
        world[BOARD][loc[1]][loc[0]] = ROBOT
        world[VALUES] = tuple([world[VALUES][0] + 1] + list(world[VALUES][1:])) #the first value +1 and the rest stays
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
    #FREE SPACE
    if world[BOARD][newloc[1]][newloc[0]] == FREE or world[BOARD][newloc[1]][newloc[0]] == BALL:
        world[BOARD][loc[1]][loc[0]] = FREE
        loc = newloc
        world[BOARD][loc[1]][loc[0]] = ROBOT
    return loc, [world[BOARD], world[VALUES], world[TIMES]]

actions = [left, right, up, down]

if isWorld5:
    actions = [up, down, left]

def MovementOps():
    return [left, right, up, down]

def get_robot_position(world):
    robotcnt = 0
    robot_position = None
    for y in range(height):
        for x in range(width):
            if world[BOARD][y][x] == ROBOT:
                robot_position = (y, x)
                robotcnt += 1
    return robot_position, robotcnt

def cupIsOnTable(world):
    for x in range(width):
        for y in range(height-1):
            if world[BOARD][y+1][x] == 'T' and world[BOARD][y][x] == 'u':
                return True
    return False
