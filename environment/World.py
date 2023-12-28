import numpy as np
import random
from copy import deepcopy
from enum import Enum

VIEWDISTX, VIEWDISTY = (3, 2)
WALL, ROBOT, CUP, FOOD, BATTERY, FREE, TABLE, KEY, DOOR, ARROW_DOWN, ARROW_UP, BALL = (
    'o', 'x', 'u', 'f', 'b', ' ', 'T', 'k', 'D', 'v', '^', 'c')
# world=[[[*x] for x in world[1:-1].split("\n")], tuple([0, 0])]

BOARD, VALUES, TIMES = (0, 1, 2)

class Action(Enum):
    U = 'move up'
    D = 'move down'
    L = 'move left'
    R = 'move right'

    def rotate(self):
        if self is Action.R:
            return Action.D
        if self == Action.D:
            return Action.L
        if self == Action.L:
            return Action.U
        if self == Action.U:
            return Action.R

class World:
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

    def __init__(self, seletion: str, loc: tuple, slippery=False) -> None:
        self.isWorld5 = False
        if "1" in seletion:
            board = World.world1
        if "2" in seletion:
            board = World.world2
        if "3" in seletion:
            board = World.world3
        if "4" in seletion:
            board = World.world4
        if "5" in seletion:
            board = World.world5
            self.isWorld5 = True
        board = np.array([[*x] for x in board[1:-1].split("\n")])
        self.height, self.width = board.shape
        times = np.array([[float("inf") for _ in range(self.width)] for _ in range(self.height)])
        self.slippery = slippery
        actions = [WorldNode.left, WorldNode.up, WorldNode.down] if self.isWorld5 else None
        self.world = WorldNode(board, (0, 0), times, loc, slippery, actions=actions)


class WorldNode:
    def __init__(self, board: np.ndarray, values: tuple, times: np.ndarray, loc_robot: tuple, slippery=False, actions=None) -> None:
        self.height, self.width = board.shape
        self.board = board
        self.values = values
        self.times = times
        self.loc_robot = loc_robot
        self.slippery = slippery
        self.actions = [WorldNode.left, WorldNode.right, WorldNode.up, WorldNode.down] if actions is None else actions

    # MOVE FUNCTIONS TAKING WALLS INTO ACCOUNT
    @staticmethod
    def left(loc):
        return (loc[0]-1, loc[1])

    @staticmethod
    def right(loc):
        return (loc[0]+1, loc[1])

    @staticmethod
    def up(loc):
        return (loc[0], loc[1]-1)

    @staticmethod
    def down(loc):
        return (loc[0], loc[1]+1)
    
    _actions_mapping = {Action.U: up, Action.D: down, Action.L: left, Action.R: right}

    def move(self, action: Action):
        loc = self.loc_robot
        if self.slippery and random.random() > 0.9:  # agent still believes it did the proper action
            action = random.choice(self.actions)  # but the world is slippery!
        
        newloc = WorldNode._actions_mapping[action](loc)

        board = self.board
        newboard = deepcopy(board)
        newvalues = list(self.values)
        x_new, y_new = newloc
        x, y = loc
        # ROBOT MOVEMENT ON FREE SPACE
        if board[y_new, x_new] == FREE:
            newboard[y, x] = FREE
            newboard[y_new, x_new] = ROBOT

        # newboard = deepcopy(world)
        for y in range(self.height):
            for x in range(self.width):
                if board[y, x] == BALL and board[y, x-1] == FREE: 
                    # Ball moves left automatically
                    newboard[y, x-1] = BALL
                    newboard[y, x] = FREE
                if board[y, x] == BALL and board[y, x-1] == WALL: 
                    # Ball moves to a random y-location, and x-location is reset to the rightmost
                    newboard[y][x] = FREE
                    newboard[random.choice(range(1, self.height-1)), self.width-1] = BALL
                if board[y, x] == ARROW_DOWN and board[y+1, x] == FREE:
                    # Arrow `v` moves down automatically
                    newboard[y+1, x] = ARROW_DOWN
                    newboard[y, x] = FREE
                if board[y, x] == ARROW_UP and board[y-1, x] == FREE:
                    # Arrow `^` moves up automatically
                    newboard[y-1, x] = ARROW_UP
                    newboard[y, x] = FREE
                if board[y, x] == ARROW_DOWN and board[y+1, x] == WALL:
                    # Arrow `v` bounces back up and becomes `^` when it hits a wall
                    newboard[y][x] = ARROW_UP
                if board[y, x] == ARROW_UP and board[y-1, x] == WALL:
                    # Arrow `^` bounces back down and becomes `v` when it hits a wall
                    newboard[y, x] = ARROW_DOWN
                if board[y, x] == CUP and board[y+1, x] == TABLE:
                    # Cup `u` move to a random location when it is uppon a table
                    newboard[y, x] = FREE
                    while True:
                        xr, yr = (random.randint(0, self.width-1), random.randint(0, self.height-1))
                        if board[yr, xr] == FREE:
                            newboard[yr, xr] = CUP
                            break
        # CUP
        if newboard[y_new, x_new] == CUP:  # an object the system could shift around
            newboard[y, x] = CUP
            newboard[y_new, x_new] = ROBOT
        # KEY
        if newboard[y_new, x_new] == KEY:
            newboard[y, x] = FREE
            newboard[y_new, x_new] = ROBOT
            # the second value +1 and the rest stays
            newvalues[1] += 1   #tuple(newvalues[0], newvalues[1]+1, *newvalues[2])
        # DOOR
        if newboard[y_new, x_new] == DOOR and newvalues[1] > 0:
            newboard[y, x] = FREE
            newboard[y_new, x_new] = ROBOT
            # the second value -1 and the rest stays
            newvalues[1] -= 1   # = tuple(newvalues[0], newvalues[1] - 1, *newvalues[2:]))
        # BALL
        if board[y_new, x_new] == BALL:
            newboard[y, x] = FREE
            loc = newloc
            newboard[y_new, x_new] = ROBOT
            # the first value +1 and the rest stays
            newvalues[0] += 1 # = tuple(newvalues[0] + 1, *newvalues[1:])
        # BATTERY
        if newboard[y_new, x_new] == BATTERY:
            newboard[y, x] = FREE
            newboard[y_new, x_new] = ROBOT
            # the first value +1 and the rest stays
            newvalues[0] += 1 # = tuple(newvalues[0] + 1, *newvalues[1:])
        # FOOD
        if newboard[y_new, x_new] == FOOD:
            newboard[y, x] = FREE
            newboard[y_new, x_new] = ROBOT
            # the first value +1 and the rest stays
            newvalues[0] += 1 # = tuple(newvalues[0] + 1, *newvalues[1:])
            # generate new food in a random location
            while True:
                xr, yr = (random.randint(0, self.width-1),
                        random.randint(0, self.height-1))
                if newboard[yr, xr] == FREE:
                    newboard[yr, xr] = FOOD
                    break
        # FREE SPACE
        if newboard[y_new, x_new] == FREE or newboard[y_new, x_new] == BALL:
            newboard[y, x] = FREE
            newboard[y_new, x_new] = ROBOT
            
        return WorldNode(newboard, tuple(newvalues), deepcopy(self.times), newloc)

    def motorbabbling(self):
        return random.choice(self.actions)

    def __str__(self) -> str:
        return '\n'.join(''.join(line) for line in self.board)
