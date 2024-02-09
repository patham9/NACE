import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

class Environment():

    def __init__(self,
               width: int,
               height: int,
               start_pos: tuple,
               terminal_pos: tuple,
               move_penalty=-0.05,
               terminal_reward=1,
               walls=None):
        self.__width = width
        self.__height = height

        self.__env = np.ones((self.__height, self.__width))
        self.__annot = np.array([[""]*self.__width for _ in range(self.__height)])

        (x, y) = start_pos
        assert x>=0 and x<height and y>=0 and y<width, "Start position out of bounds"
        self.__annot[x][y] = "S"
        self.__start_pos = (x, y)

        (x, y) = terminal_pos
        assert x>=0 and x<height and y>=0 and y<width, "Terminal position out of bounds"
        self.__annot[x][y] = "T"
        self.__terminal_pos = (x, y)

        self.__move_penalty = move_penalty
        self.__terminal_reward = terminal_reward

        for (x,y) in walls:
            assert x>=0 and x<height and y>=0 and y<width, "Walls positions out of bounds"
            self.__env[x, y] = np.nan
        self.__walls = walls


    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    @property
    def start_pos(self):
        return self.__start_pos

    @property
    def terminal_pos(self):
        return self.__terminal_pos

    @property
    def terminal_reward(self):
        return self.__terminal_reward

    @property
    def move_penalty(self):
        return self.__move_penalty

    @property
    def walls(self):
        return self.__walls

    @property
    def env(self):
        return self.__env

    def show(self):
        return None #++ !!!!!
        sns.heatmap(self.__env, cbar=False, cmap="viridis", linewidths=1, annot=self.__annot, fmt="")
        plt.show()    

    def hash_state(self, x, y):
        return self.__width*x+y

    def pure_state(self, hash_s):
        return (hash_s//self.__width, hash_s%self.__width)

    def __map_action(self, a):
        if a=="up":
            return (-1, 0)
        elif a=="left":
            return (0, -1)
        elif a=="down":
            return (1, 0)
        elif a=="right":
            return (0, 1)

    def get_next_state_and_reward(self, state, action):
        x, y = self.pure_state(state)
        new_x, new_y = x, y
        reward =self.__move_penalty
        delta_x, delta_y = self.__map_action(action)
        if (x+delta_x)>=0 and (x+delta_x)<self.__height:
            if not np.isnan(self.__env[x+delta_x, new_y]):
                new_x = x+delta_x
            else:
                new_x, new_y = (0, 0)
        if (y+delta_y)>=0 and (y+delta_y)<self.__width:
            if not np.isnan(self.__env[new_x, y+delta_y]):
                new_y = y+delta_y
            else:
                new_x, new_y = (0, 0)
        scoreInc = 0
        if (new_x, new_y)==self.__terminal_pos:
            reward = self.__terminal_reward
            scoreInc = 1
        return self.hash_state(new_x, new_y), reward, scoreInc
