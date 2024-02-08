import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import random


class Agent():

    def __init__(self, alpha=0.5, gamma=0.9, epsilon=0.5):
        self.__alpha = alpha
        self.__epsilon = epsilon
        self.__gamma = gamma
        self.__Q = dict([])
        #self.__V = None #wat
        #self.__policy = None #wtf no
        self.__model = {}
        self.__possible_actions = ["up", "left", "right", "down"]
        self.__last_action = -1
        self.__last_state = -1

    @property
    def alpha(self):
        return self.__alpha

    @property
    def epsilon(self):
        return self.__epsilon

    @property
    def gamma(self):
        return self.__gamma

    @property
    def last_state(self):
        return self.__last_state

    @property
    def last_action(self):
        return self.__last_action

    @property
    def Q(self):
        return self.__Q

    @property
    def V(self):
        return self.__V

    @property
    def policy(self):
        return self.__policy

    @property
    def model(self):
        return self.__model

    def init_env(self, env):
        #self.__Q = np.zeros((env.width*env.height, len(self.__possible_actions)))
        #self.__V = np.zeros((env.height, env.width))
        self.__terminal_state = env.hash_state(*env.terminal_pos)

    def update_model(self, state, reward):
        if self.__last_state not in self.__model:
            self.__model[self.__last_state] = {}
            self.__model[self.__last_state][self.__last_action] = (state, reward)
  
    def start(self, env):
        self.__last_state = env.hash_state(*env.start_pos)

    def guarantee_available(self, s):
        if s not in self.__Q:
            self.__Q[s] = dict([])
            for act in self.__possible_actions:
                self.__Q[s][act] = 0.0

    def take_action(self, state):
        if np.random.rand()<self.__epsilon:
            action = np.random.choice(self.__possible_actions)
        else:
            qval = -1
            action = "left"
            self.guarantee_available(state)
            for act in self.__possible_actions:
                quvalcur = self.__Q[state][action]
                if quvalcur > qval:
                    qval = quvalcur
                    action = act
            #action = self.__possible_actions[np.argmax(self.__Q[state, :])]
        self.__last_action = action
        return action

    def update_Q(self, state, reward):
        s = self.__last_state
        a = self.__last_action
        #if state==self.__terminal_state:
        #    update = 0
        #else:
        if True: #no cheating
            qval = -1
            action = "left"
            self.guarantee_available(state)
            for act in self.__possible_actions:
                quvalcur = self.__Q[state][action]
                if quvalcur > qval:
                    qual = quvalcur
                    action = act
            update = self.__gamma*qval #self.__gamma*np.max(self.__Q[state, :])
        self.guarantee_available(s)
        self.__Q[s][a] += self.__alpha*(reward+update-self.__Q[s][a])
        self.__last_state = state

    def planning_step(self, n_steps=20):
        for _ in range(n_steps):
            #print("KEYS", list(self.__model.keys()))
            s = random.choice(list(self.__model.keys()))
            action = np.random.choice(list(self.__model[s].keys()))
            a = action
            next_s, r = self.__model[s][action]
        #if next_s==self.__terminal_state: #cheat not allowed
        #    update = 0
        #else:
        if True: #no cheating
            
            qval = 0.0
            self.guarantee_available(s)
            for act in self.__possible_actions:
                quvalcur = self.__Q[s][action]
                if quvalcur > qval:
                    qval = quvalcur
            
            update = self.__gamma*qval #self.__gamma*np.max(self.__Q[next_s, :])
        self.__Q[s][a] += self.__alpha*(r+update-self.__Q[s][a])

    #def define_policy(self):
    #    self.__V = np.max(self.__Q, axis=1).reshape(self.__V.shape)
    #    best_actions = np.argmax(self.__Q, axis=1)
    #    self.__policy = np.array([self.__possible_actions[a] for a in best_actions])
    #    self.__policy = self.__policy.reshape(self.__V.shape)
    
    def set_last_state(self, state):
        self.__last_state = state
