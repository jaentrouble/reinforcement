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
        self.width = width
        self.height = height
        self.grid = np.full((width,height), G_EMPTY)
        self.answer_buffer = None
        self.answer_buffer_filled = False
        self.rand = rand
        self.trap_num = trap
        self.snakelength = snakelength
        if self.rand :   
            self.snake = Snake(*tool.randposlist(self.snakelength, self.width, self.height))
        else :
            self.s_init = tool.randposlist(self.snakelength, self.width, self.height)
            # self.s_init = [[self.width-3,self.height-3]]
            self.snake = Snake(*self.s_init)
        for pos in self.snake.get_list() :
            self.grid[pos[0]][pos[1]] = G_SNAKE
        self.apples = []
        self.traps = []
        self.t_init = []
        # self.create_apple()
        self.a_init = [1,1]
        self.create_apple(self.a_init)
        for _ in range(self.trap_num) :
            self.create_trap()
        self.control_choice = 3
        self.info = self.get_state().shape

    def action_size(self) :
        return self.control_choice

    def state_size(self) :
        return self.info

    def create_trap(self, pos = None) :
        if pos == None :
            tmpos = tool.randpos(0, self.width-1, 0, self.height-1)
            while self.grid[tmpos[0]][tmpos[1]] != G_EMPTY :
                tmpos = tool.randpos(0, self.width-1, 0, self.height-1)
            if not self.rand :
                self.t_init.append(tmpos)
        else :
            tmpos = pos
        self.traps.append(tmpos)
        self.grid[tmpos[0]][tmpos[1]] = G_TRAP

    def create_apple(self, pos = None) :
        if pos == None :
            tmpos = tool.randpos(0, self.width-1, 0, self.height-1)
            while self.grid[tmpos[0]][tmpos[1]] != G_EMPTY :
                tmpos = tool.randpos(0, self.width-1, 0, self.height-1)
            # if not self.rand :
            #     self.a_init = tmpos
        else :
            tmpos = pos
        self.apples.append(tmpos)
        self.grid[tmpos[0]][tmpos[1]] = G_APPLE

    def get_obj (self) :
        """
        returns
        {type(object) : list of pos}
        """
        d = {}
        d[G_SNAKE] = self.snake.get_list()
        d[G_APPLE] = self.apples
        d[G_TRAP] = self.traps
        return d

    def snake_health (self) :
        return self.snake.get_health()

    def snake_head(self) :
        return self.snake.get_head()

    def apple(self) :
        """
        returns the first apple's pos
        """
        return self.apples[0]
        
    def reward(self, move_direction) :
        """
        gets action (direction to move)
        returns reward, done
        done : bool
        """
        self.grid_buffer = self.grid.copy()
        trgt = self.snake_head()
        tail = self.snake.get_tail()
        bef = trgt.copy()
        app = self.apple()
        state = None
        direction, _ = self.snake.move(move_direction)

        trgt[0] += DIRECTION_LIST[direction][0]
        trgt[1] += DIRECTION_LIST[direction][1]

        if (trgt[0] > self.width-1 or
            trgt[0] < 0 or
            trgt[1] > self.height-1 or
            trgt[1] < 0)  :
            
            return Reward_dead, True
        else :
            aft = trgt.copy()

        if self.grid[trgt[0]][trgt[1]] == G_EMPTY :
            self.grid[tail[0]][tail[1]] = G_EMPTY
            self.grid[trgt[0]][trgt[1]] = G_SNAKE
            state =  MOVED
        elif self.grid[trgt[0]][trgt[1]] in (G_SNAKE, G_TRAP) :
            state = DEAD
        elif self.grid[trgt[0]][trgt[1]] == G_APPLE :
            # if self.rand :
            self.apples.remove(trgt)
            self.grid[trgt[0]][trgt[1]] = G_SNAKE
            self.create_apple()
            self.snake.eat_apple()
            state = GROW
        
        if self.snake.get_health() < 0 :
            starve = True
        else :
            starve = False

        if state == DEAD :
            return Reward_dead, True
        elif state == MOVED :
            befdist = abs(bef[0]-app[0]) + abs(bef[1]-app[1])
            aftdist = abs(aft[0]-app[0]) + abs(aft[1]-app[1])
            tmp = befdist - aftdist
            if tmp < 0 :
                return Reward_movement_far, starve
            else :
                return Reward_movement_close, starve
        elif state == GROW :
            return Reward_grow, False

    def get_state(self) :
        r, l, u, d = 0, 0, 0, 0
        ru, lu, ld, rd = 0, 0, 0, 0
        head = self.snake_head()
        direction = self.snake.get_direction()
        x = head[0]
        y = head[1]
        for column in self.grid[x+1: ] :
            if column[y] in (G_SNAKE, G_TRAP) :
                break
            else :
                r += 1
        for column in reversed(self.grid[:x]) :
            if column[y] in (G_SNAKE, G_TRAP) :
                break
            else :
                l += 1
        for row in self.grid[x][y+1:] :
            if row in (G_SNAKE, G_TRAP) :
                break
            else :
                d += 1
        for row in reversed(self.grid[x][:y]) :
            if row in (G_SNAKE, G_TRAP) :
                break
            else :
                u += 1
        for delta in range(1, min(self.width-x, y+1)):
            if self.grid[x+delta, y-delta] in (G_SNAKE, G_TRAP) :
                break
            else :
                ru += 1
        for delta in range(1, min(x+1, y+1)) :
            if self.grid[x-delta, y-delta] in (G_SNAKE, G_TRAP) :
                break
            else :
                lu += 1
        for delta in range(1, min(x+1, self.height-y)) :
            if self.grid[x-delta, y+delta] in (G_SNAKE, G_TRAP) :
                break
            else :
                ld += 1
        for delta in range(1, min(self.width-x, self.height-y)) :
            if self.grid[x+delta, y+delta] in (G_SNAKE, G_TRAP) :
                break
            else :
                rd += 1
        ap = [self.apple()[0]-x, self.apple()[1]-y]
        ap = np.dot(ROTATION_ARRAY[direction], ap)
        raw_straight = [r,u,l,d]
        conv_straight = [0,0,0]
        conv_straight[RIGHT] = raw_straight[DIRECTION_CONVERT[direction][RIGHT]]
        conv_straight[UP] = raw_straight[DIRECTION_CONVERT[direction][UP]]
        conv_straight[LEFT] = raw_straight[DIRECTION_CONVERT[direction][LEFT]]
        raw_diag = [ru,lu,ld,rd]
        conv_diag = [0,0,0,0]
        conv_diag[RU] = raw_diag[DIRECTION_CONVERT[direction][RU]]
        conv_diag[LU] = raw_diag[DIRECTION_CONVERT[direction][LU]]
        conv_diag[LD] = raw_diag[DIRECTION_CONVERT[direction][LD]]
        conv_diag[RD] = raw_diag[DIRECTION_CONVERT[direction][RD]]
        answer = np.concatenate((conv_straight,conv_diag,ap))
        if not self.answer_buffer_filled :
            self.answer_buffer = answer
            self.answer_buffer_filled = True
        return np.stack((self.answer_buffer, answer), axis = -1)
    
    def current_snake_length(self) :
        return len(self.snake)
                
    def get_snake_length(self) :
        return self.snakelength

    def set_snake_length(self, l : int) :
        self.snakelength = l

    def reset(self) :
        self.grid = np.full((self.width, self.height), G_EMPTY)
        if self.rand :
            self.snake = Snake(*tool.randposlist(self.snakelength, self.width, self.height))
        else :
            self.snake = Snake(*self.s_init)
        for pos in self.snake.get_list() :
            self.grid[pos[0]][pos[1]] = G_SNAKE
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

# class Apple() :
#     def __init__(self, pos : list) :
#         self.pos = pos

#     def get_pos(self) :
#         return self.pos.copy()

# class Trap() :
#     def __init__(self, pos : list) :
#         self.pos = pos

#     def get_pos(self) :
#         return self.pos.copy()