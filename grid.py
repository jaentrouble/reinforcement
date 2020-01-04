import pygame
from constants import *
import tool

class Grid() :
    def __init__ (self, width, height, pixel, snakelength : int) :
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
        
class Snake() :
    def __init__(self, bodypos : list) :
        """
        Snake
        bodypos : head -> tail order
        """
        self.body = bodypos.copy()

    def move(self, direction, apple : bool = False) :
        new = self.body[0].copy()
        if direction == RIGHT :
            new[0] += 1
        elif direction == UP :
            new[1] -= 1
        elif direction == LEFT :
            new[0] -= 1
        elif direction == DOWN :
            new[1] += 1
        self.body.insert(0,new)

        if not apple :
            self.body.pop()

    def get_list (self) :
        return self.body.copy()