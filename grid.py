import pygame
from constants import *
import tool

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
            self.snake = Snake(tool.randposlist(self.snakelength, self.width, self.height))
        else :
            # self.s_init = tool.randposlist(self.snakelength, self.width, self.height)
            self.s_init = [[self.width-3,self.height-3]]
            self.snake = Snake(self.s_init)
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
        
    def update(self, direction) :
        trgt = self.snake.get_head()
        if direction == RIGHT :
            trgt[0] += 1
            if trgt[0] > self.width-1 :
                return DEAD
        elif direction == UP :
            trgt[1] -= 1
            if trgt[1] < 0 :
                return DEAD
        elif direction == LEFT :
            trgt[0] -= 1
            if trgt[0] < 0 :
                return DEAD
        elif direction == DOWN :
            trgt[1] += 1
            if trgt[1] > self.height-1 :
                return DEAD

        if self.grid[trgt[0]][trgt[1]] == None :
            tail = self.snake.get_tail()
            self.grid[tail[0]][tail[1]] = None
            self.grid[trgt[0]][trgt[1]] = self.snake
            self.snake.move(direction)
            return MOVED
        elif isinstance(self.grid[trgt[0]][trgt[1]], (Snake, Trap)) :
            return DEAD
        elif isinstance(self.grid[trgt[0]][trgt[1]], Apple) :
            if self.rand :
                self.apples.remove(self.grid[trgt[0]][trgt[1]])
                self.grid[trgt[0]][trgt[1]] = self.snake
                self.snake.move(direction, True)
                self.create_apple()
            return GROW

    def reset(self) :
        for i in range (self.width) :
            for j in range(self.height) :
                self.grid[i][j] = None
        if self.rand :   
            self.snake = Snake(tool.randposlist(self.snakelength, self.width, self.height))
        else :
            self.snake = Snake(self.s_init)
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
    def __init__(self, bodypos : list) :
        """
        Snake
        bodypos : head -> tail order
        """
        self.body = bodypos.copy()
        self.health = Init_health

    def __len__ (self) :
        return len(self.body)

    def move(self, direction, apple : bool = False) :
        trgt = self.body[0].copy()
        if direction == RIGHT :
            trgt[0] += 1
        elif direction == UP :
            trgt[1] -= 1
        elif direction == LEFT :
            trgt[0] -= 1
        elif direction == DOWN :
            trgt[1] += 1
        self.body.insert(0,trgt)
        self.health -= Consume_health

        if not apple :
            self.body.pop()
        else :
            self.eat_apple()

    def get_list (self) :
        return self.body.copy()

    def get_head (self) :
        return self.body[0].copy()

    def get_tail (self) :
        return self.body[-1].copy()

    def get_health(self) :
        return self.health

    def eat_apple (self) :
        self.health += Apple_health

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