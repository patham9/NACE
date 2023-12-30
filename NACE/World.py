import numpy as np
import random
from copy import deepcopy
from .Constants import *
from .Action import Action


class WorldNode:
    def __init__(self, board: np.ndarray, values: tuple, times: np.ndarray, loc_robot: tuple) -> None:
        self.board = board
        self.values = values
        self.times = times
        self.loc_robot = loc_robot

    
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

    # _actions_mapping = {Action.U: up, Action.D: down, Action.L: left, Action.R: right}

    
    @staticmethod
    def cupIsOnTable(world: 'WorldNode'):
        width, height = world.board.shape
        for x in range(width):
            for y in range(height-1):
                if world.board[y+1, x] == 'T' and world.board[y, x] == 'u':
                    return True
        return False

    def board_to_tuple(self) -> tuple:
        return tuple(tuple(line) for line in self.board)


    @staticmethod
    def pretty_str(board: np.ndarray) -> str:
        return '\n'.join(''.join(line) for line in board)

    def __str__(self) -> str:
        return World.pretty_str(self.board)

    def __deepcopy__(self, memo):
        return WorldNode(np.copy(self.board), (*self.values,), np.copy(self.times), self.loc_robot)


    def __getitem__(self, key):
        if key == BOARD:
            return self.board
        elif key == VALUES:
            return self.values
        elif key == TIMES:
            return self.times

    def __setitem__(self, key, value):
        if key == BOARD:
            self.board = value
        elif key == VALUES:
            self.values = value
        elif key == TIMES:
            self.times = value


class World(WorldNode): 
    def __init__(self, board: np.ndarray, values: tuple, times: np.ndarray, loc_robot: tuple, slippery=False, actions=None):
        super().__init__(board, values, times, loc_robot)
        # self.loc_robot = loc_robot # y, x
        self.height, self.width = board.shape
        self.slippery = slippery
        # self.actions = [Action.U, Action.D, Action.L, Action.R] if actions is None else actions
        self.actions = actions

    def move(world, action):
        loc = world.loc_robot
        height, width = world.height, world.width
        if world.slippery and random.random() > 0.9:  # agent still believes it did the proper action
            action = random.choice(world.actions)  # but the world is slippery!
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
                    world[BOARD][random.choice(
                        range(1, height-1))][width-1] = BALL
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
            world[VALUES] = tuple(
                [world[VALUES][0]] + [world[VALUES][1] + 1] + list(world[VALUES][2:]))
        # DOOR
        if world[BOARD][newloc[1]][newloc[0]] == DOOR and world[VALUES][1] > 0:
            world[BOARD][loc[1]][loc[0]] = FREE
            loc = newloc
            world[BOARD][loc[1]][loc[0]] = ROBOT
            # the second value +1 and the rest stays
            world[VALUES] = tuple(
                [world[VALUES][0]] + [world[VALUES][1] - 1] + list(world[VALUES][2:]))
        # BALL
        if oldworld[BOARD][newloc[1]][newloc[0]] == BALL:
            world[BOARD][loc[1]][loc[0]] = FREE
            loc = newloc
            world[BOARD][loc[1]][loc[0]] = ROBOT
            # the first value +1 and the rest stays
            world[VALUES] = tuple(
                [world[VALUES][0] + 1] + list(world[VALUES][1:]))
        # BATTERY
        if world[BOARD][newloc[1]][newloc[0]] == BATTERY:
            world[BOARD][loc[1]][loc[0]] = FREE
            loc = newloc
            world[BOARD][loc[1]][loc[0]] = ROBOT
            # the first value +1 and the rest stays
            world[VALUES] = tuple(
                [world[VALUES][0] + 1] + list(world[VALUES][1:]))
        # FOOD
        if world[BOARD][newloc[1]][newloc[0]] == FOOD:
            world[BOARD][loc[1]][loc[0]] = FREE
            loc = newloc
            world[BOARD][loc[1]][loc[0]] = ROBOT
            # the first value +1 and the rest stays
            world[VALUES] = tuple(
                [world[VALUES][0] + 1] + list(world[VALUES][1:]))
            while True:
                x, y = (random.randint(0, width-1),
                        random.randint(0, height-1))
                if world[BOARD][y][x] == FREE:
                    world[BOARD][y][x] = FOOD
                    break
        # FREE SPACE
        if world[BOARD][newloc[1]][newloc[0]] == FREE or world[BOARD][newloc[1]][newloc[0]] == BALL:
            world[BOARD][loc[1]][loc[0]] = FREE
            loc = newloc
            world[BOARD][loc[1]][loc[0]] = ROBOT

        world.loc_robot = loc
        return world

    def motorbabbling(self):
        return random.choice(self.actions)

    def __deepcopy__(self, memo):
        return World(np.copy(self.board), (*self.values,), np.copy(self.times), (*self.loc_robot,), self.slippery, self.actions)


