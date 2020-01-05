import pygame
import grid
from constants import *
import boxes
import Qlearn as ql
import math
import time

class Main() :
    def __init__ (self, width = 720, height = 720, fps = 60, trap = 15) :
        pygame.init()
        self.fps = fps
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.background = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        self.background.fill((0,0,0))
        self.background.convert()
        self.clock = pygame.time.Clock()
        self.allgroup = pygame.sprite.LayeredDirty()
        self.g_x = self.width // B_size
        self.g_y = self.height // B_size
        self.grid = grid.Grid(self.g_x, self.g_y, 1, False, trap)
        self.groupsetter()
        self.boxes = {grid.Snake : [],
                      grid.Apple : [],
                      grid.Trap : []}
        self.point = 1
        self.qtable = ql.Qtable(self.g_x, self.g_y)

    def reset(self) :
        self.grid.reset()
        self.b_update()
        self.point = 1

    def groupsetter(self) :
        boxes.Box.groups = self.allgroup

    def run(self) :
        mainloop = True
        self.screen.blit(self.background, (0,0))
        self.b_update()
        # time.sleep(3)
        while mainloop :
            result = None
            reward = 0
            rst = False
            milliseconds = self.clock.tick(self.fps)
            head = self.grid.snake_head()
            apple = self.grid.apple()
            befdist = math.sqrt(abs(head[0]-apple[0])**2 + abs(head[1]-apple[1])**2)
            direction = self.qtable.action(head, befdist, self.point)
            result = self.grid.update(direction)
            new_head = self.grid.snake_head()
            aftdist = math.sqrt(abs(new_head[0]-apple[0])**2 + abs(new_head[1]-apple[1])**2)
            self.b_update()
            ###escape
            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    mainloop = False
                elif event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_ESCAPE :
                            mainloop = False 
                            return
            ######################################
                    if event.key == pygame.K_LEFT :
                        result = self.grid.update(LEFT)
                        self.b_update()
                    elif event.key == pygame.K_RIGHT :
                        result = self.grid.update(RIGHT)
                        self.b_update()
                    elif event.key == pygame.K_UP :
                        result = self.grid.update(UP)
                        self.b_update()
                    elif event.key == pygame.K_DOWN :
                        result = self.grid.update(DOWN)
                        self.b_update()

            self.allgroup.clear(self.screen, self.background)
            self.allgroup.draw(self.screen)
            if result == MOVED or result == GROW :
                self.point += 1
            if befdist * aftdist != 0 :
                reward = befdist - aftdist
            if result == GROW :
                reward = 10
                rst = True
            cap = '[FPS] : {0:.1f}, Moved : {1}, Health : {2}, Loop : {3}'.format(\
                self.clock.get_fps(), self.point, self.grid.snake_health(), self.qtable.get_loop())
            pygame.display.set_caption(cap)
            pygame.display.flip()
            if result == DEAD :
                reward = -0.1
                rst = True
            self.qtable.update(head, direction, reward)
            if rst :
                self.qtable.looped()
                self.reset()

    def b_update (self) :
        dic = self.grid.get_obj()
        for obj in dic :
            if len(self.boxes[obj]) < len(dic[obj]) :
                for _ in range(len(dic[obj])-len(self.boxes[obj])) :
                    self.boxes[obj].append(boxes.Box(obj))
            elif len(self.boxes[obj]) > len(dic[obj]) :
                for _ in range(len(self.boxes[obj])-len(dic[obj])) :
                    tmp = self.boxes[obj].pop()
                    tmp.kill()
            for n in range(len(self.boxes[obj])) :
                self.boxes[obj][n].update(dic[obj][n])

if __name__ == '__main__' :
    Main(width = 800, height = 800, fps=60, trap = 100).run()