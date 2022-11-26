import pygame as pg
from Code.forHelp.autoload import *





class Block(pg.sprite.Sprite):
    def __init__(self, start_pos):
        super().__init__([all_sprites, collision_sprites])
        self.scale = 2
        self.image = pg.Surface((32 * self.scale,32 * self.scale))
        self.image.fill((0,0,0))
        self.rect = self.image.get_rect(topleft = start_pos)


