import pygame as pg
import pygame.image
from pygame.math import Vector2 as vector
from forHelp.helpers import *
from Code.forHelp import autoload as autol





class Gun(pg.sprite.Sprite):
    def __init__(self, start_pos,operator):
        super().__init__()
        autol.all_sprites.add(self)

        self.scale =2

        self.org_sprite = pygame.image.load('../Jpgs/rewolwer.png')
        self.org_sprite = pg.transform.scale(self.org_sprite,\
                        (self.org_sprite.get_width()*self.scale, self.org_sprite.get_height()* self.scale))
        self.org_sprite.set_colorkey((255,255,255))

        self.operator = operator

        self.image = pg.Surface((pg.display.get_window_size()[0]*1.5,pg.display.get_window_size()[1]*1.5))
        self.image.fill((255,255,255))
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect(center = start_pos)

    def set_place_image(self):
        self.image = pg.Surface((pg.display.get_window_size()[0]*1.5,pg.display.get_window_size()[1]*1.5))
        self.image.fill((255,255,255))
        self.image.set_colorkey((255,255,255))

    def rotate_handler(self):
        if 90<self.operator.arm_angle<270:
            self.blit_sprite = pg.transform.rotate(pg.transform.flip(self.org_sprite,0,1),self.operator.arm_angle)
            #TODO add muzzle positions
        else:
            self.blit_sprite = pg.transform.rotate(self.org_sprite,self.operator.arm_angle)


    def update(self):
        self.set_place_image()
        self.rect.center =self.operator.arm_pos
        self.rotate_handler()
        self.image.blit(self.blit_sprite,(self.image.get_width()/2 - self.blit_sprite.get_width()/2, \
                         self.image.get_height()/2- self.blit_sprite.get_height()/2))



class Dice(pg.sprite.Sprite):
    def __init__(self, start_pos, direction, operator):
        super().__init__()
        autol.all_sprites.add(self)

        self.image = pg.Surface((10,10))
        self.image.fill((0,0,255))
        self.rect = self.image.get_rect(center = start_pos)


        self.operator = operator

        #move variable
        self.force = 13
        self.mov_var = vector(self.force,0)
        self.mov_var = self.mov_var.rotate(-direction)
        self.gravity = 0.3

    def collide_handler(self):
        for collider in autol.collision_sprites:
            if collider.rect.colliderect(self.rect) and collider != self.operator:
                self.kill() #TODO for later




    def update(self):
        self.collide_handler()

        self.rect.x += self.mov_var.x
        self.mov_var.y += self.gravity
        self.rect.y += self.mov_var.y