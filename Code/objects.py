import pygame as pg
import pygame.image

from Code.forHelp import autoload as autol





class Gun(pg.sprite.Sprite):
    def __init__(self, start_pos,operator):
        super().__init__()
        autol.all_sprites.add(self)

        self.scale =2

        self.sprite = pygame.image.load('../Jpgs/rewolwer.png')
        self.sprite = pg.transform.scale(self.sprite,\
                        (self.sprite.get_width()*self.scale, self.sprite.get_height()* self.scale))

        self.operator = operator

        self.image = self.sprite
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect(center = start_pos)

    def update(self, dt):
        self.rect.center =self.operator.rect.center