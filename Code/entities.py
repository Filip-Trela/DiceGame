import pygame as pg
import pygame.draw
from objects import Gun, Dice
from Code.forHelp import autoload as autol
from pygame.math import Vector2 as vector
from Code.forHelp.helpers import *
from settings import *



class Entity(NewSprite):
    def __init__(self):
        super().__init__()
        self.health_max = 100
        self.health_now = 100
    def update(self):
        pass



class Player(Entity):
    def __init__(self, start_pos):
        super().__init__()
        autol.all_sprites.add(self)
        #important variable
        self.scale = 2


        self.image = pg.Surface((30 * self.scale,36 * self.scale)) #60,72
        self.rect = self.image.get_rect(topleft = start_pos)

        #visualization part for a sprite in him
        self.sprite_img = pg.image.load('../Jpgs/player.png') #need a better jpg, that is in center made
        self.sprite_img.set_colorkey(COLORKEY)
        self.sprite_img = pg.transform.scale(self.sprite_img,
                                        (self.sprite_img.get_width() * self.scale, self.sprite_img.get_height() * self.scale))
        self.offsprite_pos = vector(-6 * self.scale,-10 * self.scale)


        #input variables
        self.input_vec = vector(0,0)
        self.jump_inp = 0
        self.scroll_y = 0

        #movement variables
        self.acceleration = 1.2
        self.max_speed = 9
        self.gravity =0.6
        self.jump_strenght = 18
        self.mov_vec = vector(0,0)
        self.in_air_time = 5
        self.in_air_fps = self.in_air_time #when falling off and still want to jump in run

        #arm variables
        self.arm_pos = vector()
        self.arm_lenght = 30
        self.arm_angle = 0

        #statistics
        self.health_max = autol.player_max_health
        self.health_now = 100

        #gun vars
        self.gun = Gun(self.rect.center, self)

        #cards inventory
        self.card_inventory = [] #max can be only 18
        #self.card_number = 0
        self.ammo_now = None

        #timers
        self.dice_timer = Timer(3000)

    def input(self):
        self.input_vec.x = inputHandler(pg.K_d) - inputHandler(pg.K_a)
        if inputHandler(pg.K_w):
            if self.in_air_fps >0:
                self.mov_vec.y = -self.jump_strenght
                self.in_air_fps =0

        if mouse_input_handler((0,0,1)) and not self.dice_timer.active:
            Dice(self.arm_pos,self.arm_angle)
            self.dice_timer.activate()

        #testing
        if inputHandler(pg.K_o) and self.health_now>1: self.health_now -= 1
        elif inputHandler(pg.K_i) and self.health_now < 100: self.health_now += 1
        #testing end

        if mouse_input_handler((1,0,0)) and self.ammo_now != None:
            shooted = self.gun.shoot(self.ammo_now)
            number = 0
            for num,card in enumerate(self.card_inventory):
                if card is self.ammo_now: number = num
            self.ammo_now = None
            if shooted: self.card_inventory = list(x for num,x in enumerate(self.card_inventory) if num != number)



    def x_axis_movement(self):
        self.mov_vec.x = move_towards(self.mov_vec.x,self.acceleration,self.max_speed * self.input_vec.x)
        self.rect.centerx += int(self.mov_vec.x)
        self.x_axis_collision()
    def x_axis_collision(self):
        for sprite in autol.collision_sprites:
            #TODO change rect into collision rect when colliding with world
            if self.rect.colliderect(sprite.rect):
                if self.mov_vec.x >0: #prawo
                    self.rect.right = sprite.rect.left# + 16* self.scale #TODO add variables for that
                elif self.mov_vec.x <0: #lewo
                    self.rect.left = sprite.rect.right# - 9* self.scale
                self.mov_vec.x = 0
    def y_axis_movement(self):
        #TODO jump depends on holding key
        self.mov_vec.y += self.gravity
        self.rect.centery += int(self.mov_vec.y)
        self.y_axis_collision()
    def y_axis_collision(self):
        for sprite in autol.collision_sprites:
            if self.rect.colliderect(sprite.rect):
                if self.mov_vec.y >0: #dol
                    self.rect.bottom = sprite.rect.top# + 2* self.scale
                    self.mov_vec.y = 0
                    self.in_air_fps = self.in_air_time
                elif self.mov_vec.y <0: #gora
                    self.rect.top = sprite.rect.bottom #- 10* self.scale
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

        self.dice_timer.update()


        print(self.ammo_now)


class PotatoEnemy(Entity):
    def __init__(self, start_pos):
        super().__init__()
        autol.all_sprites.add(self)
        autol.enemies_sprite.add(self)
        # important variable
        self.scale = 2

        self.image = pg.Surface((32 * self.scale, 32 * self.scale))  # 60,72
        self.rect = self.image.get_rect(topleft=start_pos)

        # visualization part for a sprite in him
        self.sprite_img = pg.image.load('../Jpgs/potato.png')  # need a better jpg, that is in center made
        self.sprite_img.set_colorkey(COLORKEY)
        self.sprite_img = pg.transform.scale(self.sprite_img,
                                             (self.sprite_img.get_width() * self.scale,
                                              self.sprite_img.get_height() * self.scale))
        self.offsprite_pos = vector(-6 * self.scale, -10 * self.scale)

