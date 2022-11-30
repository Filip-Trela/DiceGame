import sys
import pygame.draw
from entities import *
from enviroment import *
from dev_room import room
from objects import *
from settings import *

class Loops:
    def __init__(self):
        self.player = Player((70,-32))
        self.camera = Camera(all_sprites, self.player.rect.center)


        #temporary level #####################################
        for row_num, row in enumerate(room):
            for coll_numn, coll in enumerate(row):
                x = coll_numn * 64
                y = row_num * 64
                if coll == 'x':
                    Block((x,y))
        ######################################################

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

    def display_handler(self,blit_surface):
        blit_surface.fill((255,255,255))
        autol.local_pos_target= self.camera.mouse_depend_movement(self.player.rect.center,blit_surface)

        pg.display.get_surface().blit(pg.transform.scale(blit_surface, pg.display.get_window_size()),(0,0))


    def update_handler(self):
        all_sprites.update()
