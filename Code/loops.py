import sys
import pygame.draw
from entities import *
from enviroment import *
from dev_room import room
from objects import *
from settings import *
from HUD import HUD

class Loops:
    def __init__(self):
        self.scroll_y = 0


        self.player = Player((200,300))
        autol.player = self.player
        for x in range(14): #14 should be enough
            Card_Blueprint((200,300))
        self.camera = Camera(all_sprites, self.player.rect.center)
        self.hud = HUD(self.player)
        PotatoEnemy((300,300))


        #temporary level #####################################
        for row_num, row in enumerate(room):
            for coll_numn, coll in enumerate(row):
                x = coll_numn * 64
                y = row_num * 64
                if coll == 'x':
                    Block((x,y))
        #temporary level #####################################

    def input_handler(self):
        #main
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        #hud
            self.hud.input()
            if event.type == pygame.MOUSEWHEEL:
                self.scroll_y = event.y

        #in game
        if not self.hud.inventory_hud_active:
            self.player.input()

    def display_handler(self,blit_surface):
        blit_surface.fill((100,100,100))
        autol.local_pos_target= self.camera.mouse_depend_movement(self.player.rect.center,blit_surface)

        self.hud.display(blit_surface)
        pg.display.get_surface().blit(pg.transform.scale(blit_surface, pg.display.get_window_size()),(0,0))



    def update_handler(self):
        if not self.hud.inventory_hud_active:
            all_sprites.update()
        self.hud.update(self.scroll_y)
        self.scroll_y = move_towards(self.scroll_y, 0.1, 0)