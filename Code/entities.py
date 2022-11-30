import pygame as pg
import pygame.draw
from objects import Gun, Dice
from Code.forHelp import autoload as autol
from pygame.math import Vector2 as vector
from Code.forHelp.helpers import *
import settings


class Entity(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.health_max = 100
        self.health_now = 100
    def update(self,dt):
        pass



class Player(Entity):
    def __init__(self, start_pos):
        super().__init__()
        autol.all_sprites.add(self)
        #import variable

        self.image = pg.Surface((48,96))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect(topleft = start_pos)

        #input variables
        self.input_vec = vector(0,0)
        self.jump_inp = 0

        #movement variables
        self.acceleration = 1.2
        self.max_speed = 9
        self.gravity =0.6
        self.jump_strenght = 18
        self.mov_vec = vector(0,0)
        self.in_air_time = 7
        self.in_air_fps = self.in_air_time #when falling off and still want to jump in run

        #arm variables
        self.arm_pos = vector()
        self.arm_lenght = 40
        self.arm_angle = 0

        #statistics
        self.health_max = autol.player_max_health
        self.health_now = 100

        #gun vars
        self.gun = Gun(self.rect.center, self)

        #cards inventory
        card_inventory = 0

    def input(self):
        self.input_vec.x = inputHandler(pg.K_d) - inputHandler(pg.K_a)
        if inputHandler(pg.K_w):
            if self.in_air_fps >0:
                self.mov_vec.y = -self.jump_strenght
                self.in_air_fps =0

        if inputHandler(pg.K_q):
            Dice(self.arm_pos,self.arm_angle, self)

        #testing
        if inputHandler(pg.K_o) and self.health_now>0: self.health_now -= 1
        elif inputHandler(pg.K_i) and self.health_now < 100: self.health_now += 1
        #testing end


    def x_axis_movement(self):
        self.mov_vec.x = move_towards(self.mov_vec.x,self.acceleration,self.max_speed * self.input_vec.x)
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
    def y_axis_movement(self):
        #TODO jump depends on holidng key
        self.mov_vec.y += self.gravity
        self.rect.centery += self.mov_vec.y
        self.y_axis_collision()
    def y_axis_collision(self):
        for sprite in autol.collision_sprites:
            #TODO change rect into collision rect when colliding with world, but y axis
            #TODO when stepped out tile and in air for some moment, you can do a jump
            if self.rect.colliderect(sprite.rect):
                if self.mov_vec.y >0: #dol
                    self.rect.bottom = sprite.rect.top
                    self.mov_vec.y = 0
                    self.in_air_fps = self.in_air_time
                elif self.mov_vec.y <0: #gora
                    self.rect.top = sprite.rect.bottom
                    self.mov_vec.y = 0

    def arm_handler(self):
        vector_to_norm= vector(pygame.mouse.get_pos()) - vector(autol.local_pos_target)
        if vector_to_norm != () and vector_to_norm != (0,0):
            self.arm_angle =angle_of_vector(vector_to_norm.normalize())
        else: self.arm_angle=0

        #TODO only rotating when input
        self.arm_pos = self.rect.center + vector(self.arm_lenght,0).rotate(-self.arm_angle)


    def update(self):
        self.x_axis_movement()
        self.y_axis_movement()
        self.arm_handler()
        self.gun.update()

        self.in_air_fps -=1







