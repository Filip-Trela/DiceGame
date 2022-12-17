import pygame as pg
from pygame.math import Vector2 as vector
from Code.forHelp.autoload import *
from Code.forHelp.helpers import *




class Block(NewSprite):
    def __init__(self, start_pos):
        super().__init__()
        all_sprites.add(self)
        collision_sprites.add(self)

        self.scale = 2
        self.image = pg.Surface((32 * self.scale,32 * self.scale))
        self.image.fill((0,0,0))
        self.rect = self.image.get_rect(topleft = start_pos)
        self.sprite_img = self.image
        self.offsprite_pos = vector(0,0)
