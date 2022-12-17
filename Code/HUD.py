import pygame as pg
from forHelp import autoload as autol
from settings import *
from pygame.math import Vector2 as vector
from Code.forHelp.helpers import *


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



    #hud inventory part
        self.inventoryHUD_img = pg.Surface((BLIT_SIZE[0], BLIT_SIZE[1]/2))
        self.inventoryHUD_img.fill((255,255,255))
        self.inventoryHUD_img.set_colorkey((COLORKEY))

        self.cards_scale = 4 #for now 4 is enough
        self.rotated_mouse = 0
        self.scroll_speed = 3
        self.inventory_hud_active = 0
        self.center = (BLIT_SIZE[0]/2, BLIT_SIZE[1]/2)
        self.inv_move_max = 100
        self.inventory_move_y = self.inv_move_max   # 100
        self.inv_move_target = self.inv_move_max
        self.inventory_move_speed= 4

        self.choosen_card_mov_speed = 10
        self.choose_card_mov = 0
        self.choosen_card_is = False


    def set_hud_img(self):
        self.inventoryHUD_img = pg.Surface((BLIT_SIZE[0], BLIT_SIZE[1]/2))
        self.inventoryHUD_img.fill((255,255,255))
        self.inventoryHUD_img.set_colorkey((COLORKEY))

    def input(self):
        if inputHandler(pg.K_1): #TODO change into one key, probably tab, once pressed
            self.inv_move_target = 0
            self.choose_card_mov = 0
            self.choosen_card_is = False
        elif inputHandler(pg.K_0):
            self.inv_move_target = self.inv_move_max

    def update(self, scroll_y):
        self.h_line_now = self.h_line_one * self.player.health_now
        self.inventory_move_y = move_towards(self.inventory_move_y,self.inventory_move_speed, self.inv_move_target)
        self.inventory_hud_active = self.inventory_move_y != self.inv_move_max

        if self.inventory_move_y != self.inv_move_max:
            self.shuffle_cards()
            if self.inv_move_target == 0:
                self.rotated_mouse += scroll_y * self.scroll_speed


    def display(self,blit_surface):
        self.health_img = pg.transform.scale(self.health_img, (self.h_line_now, self.healthbar_img.get_height()))
        blit_surface.blit(self.health_img, self.healthbar_pos)
        blit_surface.blit(self.healthbar_img, self.healthbar_pos)

        #todo when not active, hide on the bottom and then dont blit
        if self.inventory_move_y != self.inv_move_max:
            self.set_hud_img()
            if len(self.all_cards) != 0:
                self.show_shuffle_cards()
            blit_surface.blit(self.inventoryHUD_img, (0, BLIT_SIZE[1] / 2 + self.inventory_move_y))



    def shuffle_cards(self):
        self.all_cards = self.player.card_inventory
        self.num_cards = len(self.all_cards)


        self.degree_for_one = 360/self.num_cards if self.num_cards !=0 else 0
        self.from_center = vector(BLIT_SIZE[0]/3, 0)

    def show_shuffle_cards(self):
        card_choose_list = []
        card_half_size = None

        # pozycja local kart
        for card_number,card in enumerate(self.all_cards):
            card_half_size = vector(card.image.get_width() * self.cards_scale / 2, card.image.get_height() * self.cards_scale / 2)
            #TODO can be once used only ^
            #positions
            rotated_vec = self.from_center.rotate(self.degree_for_one * (card_number+1)+ self.rotated_mouse)
            card.z_hud_pos = rotated_vec

        #sortowanie kart na podstawie polozenia y w talii obracanej
        self.all_cards.sort(key= lambda x: x.z_hud_pos[1])


        #blitowansko
        #todo optimalize and put some shit into update function
        for card_number,card in enumerate(self.all_cards):
            if card_number ==0:
                card.image.set_alpha(255)
                self.inventoryHUD_img.blit(pg.transform.scale(card.image, \
                        (card.image.get_width() * self.cards_scale,card.image.get_height() * self.cards_scale)), \
                        # image and its size handling
                        vector(self.center) + vector(card.z_hud_pos[0],
                        card.z_hud_pos[1] / 10 - (100/ len(self.all_cards)) +self.choose_card_mov) - card_half_size)
            else:
                card.image.set_alpha(210)
                self.inventoryHUD_img.blit(pg.transform.scale(card.image, \
                                                              (card.image.get_width() * self.cards_scale,
                                                               card.image.get_height() * self.cards_scale)), \
                                           # image and its size handling
                                           vector(self.center) + vector(card.z_hud_pos[0],
                                                                        card.z_hud_pos[1] / 8) - card_half_size)


        #wrzucanie karty do magazynku
        if mouse_input_handler((1,0,0)):
            self.player.ammo_now = self.all_cards[0]
            self.inv_move_target = self.inv_move_max
            self.choosen_card_is = True
        if self.choosen_card_is:
            self.choose_card_mov += self.choosen_card_mov_speed


