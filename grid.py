from constants import *
import numpy as np
import tool
import math
import random

class Grid() :
    def __init__ (self, width, height, snakelength : int, rand = True, trap = 0) :
        """
        Grid
        snakelength : initial snake length
        """
        self.grid = []
        self.width = width
        self.height = height
        self.rand = rand
        self.trap_num = trap
        self.snakelength = snakelength
        for i in range (self.width) :
            self.grid.append([])
            for _ in range(self.height) :
                self.grid[i].append(None)
        if self.rand :   
            self.snake = Snake(*tool.randposlist(self.snakelength, self.width, self.height))
        else :
            # self.s_init = tool.randposlist(self.snakelength, self.width, self.height)
            self.s_init = [[self.width-3,self.height-3]]
            self.snake = Snake(self.s_init,0)
        for pos in self.snake.get_list() :
            self.grid[pos[0]][pos[1]] = self.snake
        self.apples = []
        self.traps = []
        self.t_init = []
        # self.create_apple()
        self.a_init = [1,1]
        self.create_apple(self.a_init)
        for _ in range(self.trap_num) :
            self.create_trap()
        self.control_size = 3
        self.info = np.array(self.get_state()).shape

    def action_size(self) :
        return self.control_size

    def state_size(self) :
        return self.info

    def create_trap(self, pos = None) :
        if pos == None :
            tmpos = tool.randpos(0, self.width-1, 0, self.height-1)
            while self.grid[tmpos[0]][tmpos[1]] != None :
                tmpos = tool.randpos(0, self.width-1, 0, self.height-1)
            if not self.rand :
                self.t_init.append(tmpos)
        else :
            tmpos = pos
        self.traps.append(Trap(tmpos))
        self.grid[tmpos[0]][tmpos[1]] = self.traps[-1]

    def create_apple(self, pos = None) :
        if pos == None :
            tmpos = tool.randpos(0, self.width-1, 0, self.height-1)
            while self.grid[tmpos[0]][tmpos[1]] != None :
                tmpos = tool.randpos(0, self.width-1, 0, self.height-1)
            if not self.rand :
                self.a_init = tmpos
        else :
            tmpos = pos
        self.apples.append(Apple(tmpos))
        self.grid[tmpos[0]][tmpos[1]] = self.apples[-1]

    def get_obj (self) :
        """
        returns
        {type(object) : list of pos}
        """
        d = {}
        d[Snake] = self.snake.get_list()
        a = []
        t = []
        for apple in self.apples :
            a.append(apple.get_pos())
        d[Apple] = a
        for trp in self.traps :
            t.append(trp.get_pos())
        d[Trap] = t
        return d

    def snake_health (self) :
        return self.snake.get_health()

    def snake_head(self) :
        return self.snake.get_head()

    def apple(self) :
        """
        returns the first apple's pos
        """
        return self.apples[0].get_pos()
        
    def reward(self, move_direction) :
        """
        gets action (direction to move)
        returns reward, done
        done : bool
        """
        trgt = self.snake_head()
        tail = self.snake.get_tail()
        bef = trgt.copy()
        app = self.apple()
        state = None
        direction, health = self.snake.move(move_direction)

        trgt[0] += DIRECTION_LIST[direction][0]
        trgt[1] += DIRECTION_LIST[direction][1]

        if (trgt[0] > self.width-1 or
            trgt[0] < 0 or
            trgt[1] > self.height-1 or
            trgt[1] < 0 or
            health < 0)  :
            state = DEAD
        if state == DEAD :
            return Reward_dead, True
        else :
            aft = trgt.copy()

        if self.grid[trgt[0]][trgt[1]] == None :
            self.grid[tail[0]][tail[1]] = None
            self.grid[trgt[0]][trgt[1]] = self.snake
            state =  MOVED
        elif isinstance(self.grid[trgt[0]][trgt[1]], (Snake, Trap)) :
            state = DEAD
        elif isinstance(self.grid[trgt[0]][trgt[1]], Apple) :
            if self.rand :
                self.apples.remove(self.grid[trgt[0]][trgt[1]])
                self.grid[trgt[0]][trgt[1]] = self.snake
                self.create_apple()
                self.snake.eat_apple()
            state = GROW
        
        if state == DEAD :
            return Reward_dead, True
        elif state == MOVED :
            befdist = abs(bef[0]-app[0]) + abs(bef[1]-app[1])
            aftdist = abs(aft[0]-app[0]) + abs(aft[1]-app[1])
            tmp = befdist - aftdist
            if tmp < 0 :
                return Reward_movement_far, False
            else :
                return Reward_movement_close, False
        elif state == GROW :
            return Reward_grow, False

    def get_state(self) :
        r, l, u, d = 0, 0, 0, 0
        head = self.snake_head()
        direction = self.snake.get_direction()
        x = head[0]
        y = head[1]
        for column in self.grid[x+1: ] :
            if isinstance(column[y], (Snake, Trap)):
                break
            else :
                r += 1
        for column in reversed(self.grid[:x]) :
            if isinstance(column[y], (Snake, Trap)) :
                break
            else :
                l += 1
        for row in self.grid[x][y+1:] :
            if isinstance(row, (Snake, Trap)) :
                break
            else :
                d += 1
        for row in reversed(self.grid[x][:y]) :
            if isinstance(row, (Snake, Trap)) :
                break
            else :
                u += 1
        ap = np.array((self.apple()[0]-x, self.apple()[1]-y))
        # x_len = len(self.grid)
        # y_len = len(self.grid[0])
        ap = np.sign(ap)
        ap = np.dot(ROTATION_ARRAY[direction], ap)
        raw = np.array([r,u,l,d])
        conv = np.array([0,0,0])
        conv[RIGHT] = raw[DIRECTION_CONVERT[direction][RIGHT]]
        conv[UP] = raw[DIRECTION_CONVERT[direction][UP]]
        conv[LEFT] = raw[DIRECTION_CONVERT[direction][LEFT]]
        if np.all(conv != np.zeros(len(conv))) :
            conv = conv/np.linalg.norm(conv)
        answer = np.append(conv,ap)
        return answer.flatten()
    
    def current_snake_length(self) :
        return len(self.snake)
                
    def get_snake_length(self) :
        return self.snakelength

    def set_snake_length(self, l : int) :
        self.snakelength = l

    def reset(self) :
        for i in range (self.width) :
            for j in range(self.height) :
                self.grid[i][j] = None
        if self.rand :   
            self.snake = Snake(*tool.randposlist(self.snakelength, self.width, self.height))
        else :
            self.snake = Snake(self.s_init, 0)
        for pos in self.snake.get_list() :
            self.grid[pos[0]][pos[1]] = self.snake
        self.apples = []
        if not self.rand:
            self.create_apple(self.a_init)
        else :
            self.create_apple()
        self.traps = []
        if not self.rand :
            for tpos in self.t_init :
                self.create_trap(tpos)
        else :
            for _ in range(self.trap_num) :
                self.create_trap()

class Snake() :
    def __init__(self, bodypos : list, direction : int) :
        """
        Snake
        bodypos : head -> tail order
        """
        self.body = bodypos.copy()
        self.health = Init_health
        self.direction = direction
        self.temp = None

    def __len__ (self) :
        return len(self.body)

    def move(self, move_direction) :
        """
        return head direction, health
        """
        trgt = self.body[0].copy()
        self.direction = DIRECTION_CONVERT[move_direction][self.direction]
        trgt[0] += DIRECTION_LIST[self.direction][0]
        trgt[1] += DIRECTION_LIST[self.direction][1]
        self.body.insert(0,trgt)
        self.health -= Consume_health
        self.temp = self.body.pop()
        
        return self.direction, self.health

    def get_list (self) :
        return self.body.copy()

    def get_head (self) :
        return self.body[0].copy()

    def get_tail (self) :
        return self.body[-1].copy()

    def get_health(self) :
        return self.health

    def eat_apple (self) :
        self.body.append(self.temp)
        self.health += Apple_health

    def get_direction(self):
        return self.direction

class Apple() :
    def __init__(self, pos : list) :
        self.pos = pos

    def get_pos(self) :
        return self.pos.copy()

class Trap() :
    def __init__(self, pos : list) :
        self.pos = pos

    def get_pos(self) :
        return self.pos.copy()