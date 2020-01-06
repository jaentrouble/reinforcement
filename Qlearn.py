import random
from constants import *
import math

class Qtable() :
    def __init__(self, width : int, height : int):
        self.table = []
        self.width = width
        self.height = height
        for i in range(width) :
            self.table.append([])
            for _ in range(height) :
                self.table[i].append([0,0,0,0])
        self.loop = 1

    def action(self, pos : list, dist, steps) :
        if random.random() < Q_e/self.loop :
            return random.randint(0,3)
        elif steps > 1000 :
            return random.randint(0,3)
        else:
            return self.rargmax(pos)

    def looped(self) :
        self.loop += 1

    def get_loop(self) :
        return self.loop
    
    def rargmax(self, pos : list) :
        vector = self.table[pos[0]][pos[1]]
        m = max(vector)
        indices = [i for i, x in enumerate(vector) if x == m]
        return random.choice(indices)

    def qmax(self, pos : list) :
        return max(self.table[pos[0]][pos[1]])

    def update(self, pos : list, direction : int, reward) :
        vector = self.table[pos[0]][pos[1]]
        if direction == RIGHT :
            if pos[0] +1 == self.width :
                vector[direction] = (1-Q_alpha)*vector[direction] + Q_alpha*(reward)
            else :
                vector[direction] = (1-Q_alpha)*vector[direction] + Q_alpha*(reward + Q_gamma *self.qmax([pos[0]+1,pos[1]]))
        elif direction == LEFT :
            if pos[0] == 0 :
                vector[direction] = (1-Q_alpha)*vector[direction] + Q_alpha*(reward)
            else :
                vector[direction] = (1-Q_alpha)*vector[direction] + Q_alpha*(reward + Q_gamma *self.qmax([pos[0]-1,pos[1]]))
        elif direction == UP :
            if pos[1] == 0 :
                vector[direction] = (1-Q_alpha)*vector[direction] + Q_alpha*(reward)
            else :
                vector[direction] = (1-Q_alpha)*vector[direction] + Q_alpha*(reward + Q_gamma *self.qmax([pos[0],pos[1]-1]))
        elif direction == DOWN :
            if pos[1] +1 == self.height :
                vector[direction] = (1-Q_alpha)*vector[direction] + Q_alpha*(reward)
            else :
                vector[direction] = (1-Q_alpha)*vector[direction] + Q_alpha*(reward + Q_gamma *self.qmax([pos[0],pos[1]+1]))