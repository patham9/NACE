from enum import Enum

class Action(Enum):
    U = '^up'
    D = '^down'
    L = '^left'
    R = '^right'

    def rotate(self):
        if self is Action.R:
            return Action.D
        if self == Action.D:
            return Action.L
        if self == Action.L:
            return Action.U
        if self == Action.U:
            return Action.R