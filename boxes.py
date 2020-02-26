import pygame
import grid
from constants import *

class Box (pygame.sprite.DirtySprite) :
    base_box = pygame.Surface((B_size, B_size))
    color_dic = {G_SNAKE : (255,255,255),
                 G_APPLE : (255,0,0),
                 G_TRAP : (0,255,0)}
    img = {}
    for obj in color_dic :
        img[obj] = base_box.copy()
        img[obj].fill(color_dic[obj])

    def __init__(self, obj) :
        """
        Box
        pos : in grid
        """
        pygame.sprite.DirtySprite.__init__(self, self.groups)
        self.pos = [0,0]
        self.image = Box.img[obj]
        self.rect = self.image.get_rect()
        
    def update(self, pos : list) :
        """
        pos : in grid
        """
        bef = self.rect.copy()
        self.pos = pos.copy()
        self.rect.x = self.pos[0] * B_size
        self.rect.y = self.pos[1] * B_size
        if bef != self.rect :
            self.dirty = 1
