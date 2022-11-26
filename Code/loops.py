import sys
import pygame.draw
from entities import *
from enviroment import *
from dev_room import room
from objects import *

class Loops:
    def __init__(self):

        self.player = Player((70,-32))
        self.camera = Camera(all_sprites, self.player.rect.center)




        #temporary level
        for row_num, row in enumerate(room):
            for coll_numn, coll in enumerate(row):
                x = coll_numn * 64
                y = row_num * 64
                if coll == 'x':
                    Block((x,y))

    def input_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            self.player.input()

    def display_handler(self):
        pygame.display.get_surface().fill((255,255,255))
        self.camera.mouse_depend_movement(self.player.rect.center)

    def update_handler(self,dt):
        all_sprites.update(dt)
