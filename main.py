import pygame
import grid
from constants import *
import boxes
import Qlearn as ql
import math
import time
import DQ as dq
import tracemalloc

class Main() :
    def __init__ (self, width = 720, height = 720, fps = 60, trap = 15, load = False) :
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
        self.grid = grid.Grid(self.g_x, self.g_y, 3, True, trap)
        self.groupsetter()
        self.boxes = {grid.Snake : [],
                      grid.Apple : [],
                      grid.Trap : []}
        self.point = 1
        self.player = dq.Player(self.grid)
        if load :
            self.player.load_weight()
        self.loop = 0
        # self.qtable = ql.Qtable(self.g_x, self.g_y)

    def reset(self) :
        self.grid.reset()
        self.b_update()
        self.point = 1
        self.loop += 1

    def groupsetter(self) :
        boxes.Box.groups = self.allgroup
        

    def run(self) :
        tracemalloc.start(25)
        mainloop = True
        self.screen.blit(self.background, (0,0))
        self.b_update()
        # time.sleep(3)
        while mainloop :
            self.clock.tick(self.fps)
            # result = None
            # reward = 0
            # head = self.grid.snake_head()
            # apple = self.grid.apple()
            # befdist = math.sqrt(abs(head[0]-apple[0])**2 + abs(head[1]-apple[1])**2)
            # direction = self.qtable.action(head, befdist, self.point)
            # result = self.grid.update(direction)
            # new_head = self.grid.snake_head()
            # aftdist = math.sqrt(abs(new_head[0]-apple[0])**2 + abs(new_head[1]-apple[1])**2)
            ###escape
            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    mainloop = False
                elif event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_ESCAPE :
                        mainloop = False 
                        return
            ######################################
                    # if event.key == pygame.K_t :
                    #     snapshot = tracemalloc.take_snapshot()
                    #     top_stats = snapshot.statistics('traceback')
                    #     stat = top_stats[0]
                    #     print("%s memory blocks: %.1f KiB" % (stat.count, stat.size / 1024))
                    #     for line in stat.traceback.format() :
                    #         print(line)
                    
                    # if event.key == pygame.K_LEFT :
                    #     result = self.grid.update(LEFT)
                    #     self.b_update()
                    # elif event.key == pygame.K_RIGHT :
                    #     result = self.grid.update(RIGHT)
                    #     self.b_update()
                    # elif event.key == pygame.K_UP :
                    #     result = self.grid.update(UP)
                    #     self.b_update()
                    # elif event.key == pygame.K_DOWN :
                    #     result = self.grid.update(DOWN)
                    #     self.b_update()
                    if event.key == pygame.K_s :
                        self.player.save_weight()
            # if result == MOVED or result == GROW :
            #     self.point += 1
            # if Reward_apple_distance:
            #     reward = befdist - aftdist
            # if result == GROW :
            #     reward = Reward_grow
            #     rst = True
            # if result == DEAD :
            #     reward = Reward_dead
            #     rst = True
            done = self.player.update()
            self.b_update()
            self.allgroup.clear(self.screen, self.background)
            self.allgroup.draw(self.screen)
            cap = '[FPS] : {0:.1f} length : {1} Lp : {2}'.format(\
                self.clock.get_fps(), self.grid.current_snake_length(), self.player.get_count())
            pygame.display.set_caption(cap)
            pygame.display.flip()
            
            # self.qtable.update(head, direction, reward)
            if done :
                # self.qtable.looped()
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
    Main(width = 400, height = 400, fps=60, trap = 0, load = True).run()