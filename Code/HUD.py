import pygame as pg
from forHelp import autoload as autol
from settings import *
from pygame.math import Vector2 as vector


class HUD:
    def __init__(self,player):

        self.player = player

        #healthbar part
        self.scale_health = 2
        self.healthbar_img = pg.image.load('../Jpgs/bar.png')
        self.healthbar_img = pg.transform.scale(self.healthbar_img,(self.healthbar_img.get_width()* self.scale_health,\
                                                                    self.healthbar_img.get_height()* self.scale_health))
        self.healthbar_img.set_colorkey(COLORKEY)
        self.healthbar_pos = vector(BLIT_SIZE[0]/30,BLIT_SIZE[1]/30)

        self.health_img = pg.image.load('../Jpgs/health.png')
        self.h_line_max = self.healthbar_img.get_width()
        self.h_line_one = self.h_line_max / autol.player_max_health
        self.h_line_now = self.h_line_one
        self.health_img = pg.transform.scale(self.health_img, (self.h_line_now,self.healthbar_img.get_height()))








    def display(self,blit_surface):
        self.health_img = pg.transform.scale(self.health_img, (self.h_line_now, self.healthbar_img.get_height()))
        blit_surface.blit(self.health_img, self.healthbar_pos)
        blit_surface.blit(self.healthbar_img, self.healthbar_pos)

    def update(self):
        self.h_line_now = self.h_line_one * self.player.health_now


