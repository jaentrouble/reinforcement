import pygame

class Main() :
    def __init__ (self, width = 720, height = 720, fps = 60) :
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

    def run(self) :
        mainloop = True
        self.screen.blit(self.background, (0,0))
        while mainloop :
            milliseconds = self.clock.tick(self.fps)
            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    mainloop = False
                elif event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_ESCAPE :
                            mainloop = False 
                            break
            self.allgroup.clear(self.screen, self.background)
            self.allgroup.draw(self.screen)
            pygame.display.flip()

if __name__ == '__main__' :
    Main().run()