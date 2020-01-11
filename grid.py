from constants import *
import numpy as np
import tool
import math

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
        self.control_choice = 4 
        self.info = len(self.get_state())

    def action_size(self) :
        return self.control_choice

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
        
    def reward(self, direction) :
        """
        gets action (direction to move)
        returns reward, done
        done : bool
        """
        trgt = self.snake_head()
        bef = trgt.copy()
        app = self.apple()
        state = None

        if direction == RIGHT :
            trgt[0] += 1
            if trgt[0] > self.width-1 :
                state =  DEAD
        elif direction == UP :
            trgt[1] -= 1
            if trgt[1] < 0 :
                state = DEAD
        elif direction == LEFT :
            trgt[0] -= 1
            if trgt[0] < 0 :
                state = DEAD
        elif direction == DOWN :
            trgt[1] += 1
            if trgt[1] > self.height-1 :
                state = DEAD
        if state == DEAD :
            return Reward_dead, True
        else :
            aft = trgt.copy()

        if self.grid[trgt[0]][trgt[1]] == None :
            tail = self.snake.get_tail()
            self.grid[tail[0]][tail[1]] = None
            self.grid[trgt[0]][trgt[1]] = self.snake
            self.snake.move(direction)
            if self.snake_health() < 0 :
                state = DEAD
            else :
                state =  MOVED
        elif isinstance(self.grid[trgt[0]][trgt[1]], (Snake, Trap)) :
            state = DEAD
        elif isinstance(self.grid[trgt[0]][trgt[1]], Apple) :
            if self.rand :
                self.apples.remove(self.grid[trgt[0]][trgt[1]])
                self.grid[trgt[0]][trgt[1]] = self.snake
                self.snake.move(direction, True)
                self.create_apple()
            state = GROW
        
        if state == DEAD :
            return Reward_dead, True
        elif state == MOVED :
            befdist = math.sqrt(abs(bef[0]-app[0])**2 + abs(bef[1]-app[1])**2)
            aftdist = math.sqrt(abs(aft[0]-app[0])**2 + abs(aft[1]-app[1])**2)
            tmp = befdist - aftdist
            if tmp < 0 :
                return -1 * Reward_movement, False
            else :
                return 0, False
        elif state == GROW :
            return Reward_grow, False

    def get_state(self) :
        """
        returns [xp, xn, yp, yn, apple_x, apple_y]
        """
        xp, xn, yp, yn = 1, 1, 1, 1
        head = self.snake_head()
        x = head[0]
        y = head[1]
        for column in self.grid[x+1: ] :
            if isinstance(column[y], (Snake, Trap)):
                break
            else :
                xp += 1
        for column in reversed(self.grid[:x]) :
            if isinstance(column[y], (Snake, Trap)) :
                break
            else :
                xn += 1
        for row in self.grid[x][y+1:] :
            if isinstance(row, (Snake, Trap)) :
                break
            else :
                yp += 1
        for row in reversed(self.grid[x][:y]) :
            if isinstance(row, (Snake, Trap)) :
                break
            else :
                yn += 1
        ap = np.array(self.apple())
        ap = np.tanh(ap)
        return [1/xp, 1/xn, 1/yp, 1/yn, ap[0], ap[1],]
                
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