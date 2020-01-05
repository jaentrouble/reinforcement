import pygame
from constants import *
import tool

class Grid() :
    def __init__ (self, width, height, snakelength : int) :
        """
        Grid
        snakelength : initial snake length
        """
        self.grid = []
        self.width = width
        self.height = height
        for i in range (width) :
            self.grid.append([])
            for _ in range(height) :
                self.grid[i].append(None)
        self.snake = Snake(tool.randposlist(snakelength, self.width, self.height))
        for pos in self.snake.get_list() :
            self.grid[pos[0]][pos[1]] = self.snake
        self.apples = []
        self.create_apple()

    def create_apple(self) :
        tmpos = tool.randpos(0, self.width-1, 0, self.height-1)
        while self.grid[tmpos[0]][tmpos[1]] != None :
            tmpos = tool.randpos(0, self.width-1, 0, self.height-1)
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
        for apple in self.apples :
            a.append(apple.get_pos())
        d[Apple] = a
        return d

    def snake_health (self) :
        return self.snake.get_health()
        
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
        elif isinstance(self.grid[trgt[0]][trgt[1]], Snake) :
            return DEAD
        elif isinstance(self.grid[trgt[0]][trgt[1]], Apple) :
            self.apples.remove(self.grid[trgt[0]][trgt[1]])
            self.grid[trgt[0]][trgt[1]] = self.snake
            self.snake.move(direction, True)
            self.create_apple()
            return GROW

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
        self.health -= 1

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