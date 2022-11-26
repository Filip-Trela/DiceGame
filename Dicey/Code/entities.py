import pygame as pg
import pygame.draw
from objects import Gun
from Code.forHelp import autoload as autol
from pygame.math import Vector2 as vector
from Code.forHelp.helpers import *


class Entity(pg.sprite.Sprite):
    def update(self,dt):
        pass



class Player(Entity):
    def __init__(self, start_pos):
        super().__init__()
        autol.all_sprites.add(self)
        #import variable
        self.scale = 3

        self.image = pg.Surface((16 * self.scale,32 * self.scale))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect(topleft = start_pos)

        #input variables
        self.input_vec = vector(0,0)
        self.jump_inp = 0

        #movement variables
        self.acceleration = 1 * self.scale
        self.max_speed = 3 * self.scale
        self.gravity = 0.2* self.scale
        self.jump_strenght = 6 * self.scale
        self.mov_vec = vector(0,0)

        #arm variables
        self.arm_pos = vector()
        self.arm_lenght = 20
        self.arm_angle = 0

        #gun vars
        self.gun = Gun(self.rect.center, self)

    def input(self):
        self.input_vec.x = inputHandler(pg.K_d) - inputHandler(pg.K_a)
        self.jump_inp = inputHandler(pg.K_w)

    def x_axis_movement(self,dt):
        self.mov_vec.x = move_towards(self.mov_vec.x,self.acceleration *dt,self.max_speed * self.input_vec.x *dt)
        self.rect.centerx += int(self.mov_vec.x)
        self.x_axis_collision()
    def x_axis_collision(self):
        for sprite in autol.collision_sprites:
            #TODO change rect into collision rect when colliding with world
            if self.rect.colliderect(sprite.rect):
                if self.mov_vec.x >0: #prawo
                    self.rect.right = sprite.rect.left
                elif self.mov_vec.x <0: #lewo
                    self.rect.left = sprite.rect.right
                self.mov_vec.x = 0
    def y_axis_movement(self,dt):
        #TODO jump depends on holidng key
        self.mov_vec.y += self.gravity
        self.rect.centery += self.mov_vec.y* dt
        self.y_axis_collision()
    def y_axis_collision(self):
        for sprite in autol.collision_sprites:
            #TODO change rect into collision rect when colliding with world, but y axis
            #TODO when stepped out tile and in air for some moment, you can do a jump
            if self.rect.colliderect(sprite.rect):
                if self.mov_vec.y >0: #dol
                    self.rect.bottom = sprite.rect.top
                    self.mov_vec.y = 0
                    if self.jump_inp:
                        self.mov_vec.y = -self.jump_strenght
                elif self.mov_vec.y <0: #gora
                    self.rect.top = sprite.rect.bottom
                    self.mov_vec.y = 0

    def arm_handler(self):
        autol.vec = self.rect.center + vector(20,0)


    def update(self,dt):
        self.x_axis_movement(dt)
        self.y_axis_movement(dt)
        self.arm_handler()





