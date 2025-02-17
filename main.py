import pygame
import grid_1d as grid
from constants import *
import boxes
import time
import DQ_1d as dq

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
        self.boxes = {G_SNAKE : [],
                      G_APPLE : [],
                      G_TRAP : []}
        self.point = 1
        self.player = dq.Player(self.grid)
        if load :
            self.player.load_weight()
        self.loop = 0

    def reset(self) :
        self.grid.reset()
        self.b_update()
        self.point = 1
        self.loop += 1

    def groupsetter(self) :
        boxes.Box.groups = self.allgroup
        

    def run(self) :
        mainloop = True
        self.screen.blit(self.background, (0,0))
        self.b_update()
        # time.sleep(3)
        while mainloop :
            self.clock.tick(self.fps)
            ###escape
            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    mainloop = False
                elif event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_ESCAPE :
                        mainloop = False 
                        return
            ######################################                    
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
            done = self.player.update()
            self.b_update()
            if not (self.player.total_tick +1) % DQ_save_rate :
                self.player.save_weight()
            self.allgroup.clear(self.screen, self.background)
            self.allgroup.draw(self.screen)
            cap = '[FPS] : {0:.1f} Rounds : {1} Score :{2}'.format(self.clock.get_fps(), self.player.rounds, self.player.score)
            pygame.display.set_caption(cap)
            pygame.display.flip()
            
            if done :
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
    Main(width = 200, height = 200, fps=120, trap = 0, load = False).run()