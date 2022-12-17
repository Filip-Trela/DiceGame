import random

import pygame as pg
import pygame.image
from pygame.math import Vector2 as vector
from forHelp.helpers import *
from Code.forHelp import autoload as autol
from settings import COLORKEY




class Gun(NewSprite):
    def __init__(self, start_pos,operator):
        #TODO add timer for  reloading, when hud puting card will work
        #TODO add knockback
        super().__init__()
        autol.all_sprites.add(self)

        self.scale =1.5

        self.org_sprite = pygame.image.load('../Jpgs/rewolwer.png')
        self.org_sprite = pg.transform.scale(self.org_sprite,\
                        (self.org_sprite.get_width()*self.scale, self.org_sprite.get_height()* self.scale))
        self.org_sprite.set_colorkey(COLORKEY)
        self.blit_sprite = self.org_sprite

        self.operator = operator

        self.image = pg.Surface((pg.display.get_window_size()[0]*1.5,pg.display.get_window_size()[1]*1.5))
        self.image.fill((255,255,255))
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect(center = start_pos) #basically gun center

        self.muzzle_y = -5
        self.muzzle_pos = vector(15, self.muzzle_y)
        self.muzzle_pos_global = vector(0,0)
        self.muzzle_pos_local = vector(0,0)
        self.raycast_line_global = ((),()) #TODO something ehere
        self.raycast_line_local = ((),())
        self.raycast_lenght = 700

        #rotation variables
        self.rotats = self.operator.arm_angle
        self.rotation_speed = 5

        self.rot_knockback_poss = [80,90,100]

        self.shoot_fps = 5
        self.shooting = 0

        #timers
        self.shoot_timer = Timer(1000)

        #for fixing
        self.sprite_img = self.image
        self.offsprite_pos = vector(0,0)

        #func from card
        self.shooting_visualization = None

    def set_place_image(self):
        self.image = pg.Surface((pg.display.get_window_size()[0]*1.5,pg.display.get_window_size()[1]*1.5))
        self.image.fill((255,255,255))
        self.image.set_colorkey(COLORKEY)

    def rotate_handler(self):
        if 90 < self.operator.arm_angle < 270: #z lewej
            self.muzzle_pos.y = -self.muzzle_y
            self.rotats = move_towards(self.rotats, self.rotation_speed, self.operator.arm_angle)
            self.blit_sprite = pg.transform.rotate(pg.transform.flip(self.org_sprite, 0, 1), self.rotats)
        elif self.operator.arm_angle > 270 and self.rotats < 90:
            self.rotats -= self.rotation_speed
            if self.rotats < 0:
                self.rotats += 360
        elif self.operator.arm_angle < 90 and self.rotats > 270:
            self.rotats += self.rotation_speed
            if self.rotats > 360:
                self.rotats -= 360
        else: #z prawej
            self.muzzle_pos.y = self.muzzle_y
            self.rotats = move_towards(self.rotats, self.rotation_speed, self.operator.arm_angle)
            self.blit_sprite = pg.transform.rotate(self.org_sprite, self.rotats)

    def shoot(self,card):
        if not self.shoot_timer.active:
            card.raycasting(self)
            self.shooting = card.shoot_fps
            self.shooting_visualization = card.shooting_visualization
            self.shoot_timer.activate()

            if 90<self.operator.arm_angle<270:
                self.rotats -= random.choice(self.rot_knockback_poss)
            else: self.rotats += random.choice(self.rot_knockback_poss)
            return True
        else: return False

    #todo possible that raycasting will be in card and visualization
    def muzzle_position_handler(self):
        # for physics
        # setting position of muzzle in global world
        self.muzzle_pos_global = self.rect.center + self.muzzle_pos.rotate(-self.operator.arm_angle)

        # for visualization (done)
        self.muzzle_pos_local = self.muzzle_pos.rotate(-self.operator.arm_angle) + \
                                vector(self.image.get_rect().width / 2, self.image.get_rect().height / 2)

    def update(self):
        self.shoot_timer.update()

        self.set_place_image()
        self.rect.center =self.operator.arm_pos
        self.rotate_handler()
        self.muzzle_position_handler()
        if self.shooting:
            self.shooting_visualization(self)
            self.shooting -= 1

        self.pos = (self.image.get_width() / 2 - self.blit_sprite.get_width() / 2, \
                    self.image.get_height() / 2 - self.blit_sprite.get_height() / 2)
        self.image.blit(self.blit_sprite,self.pos)
        self.sprite_img = self.image




class Card_Blueprint(NewSprite):
    def __init__(self, start_pos):
        super().__init__()
        autol.all_sprites.add(self)
        self.sprite = pg.image.load('../Jpgs/card.png')
        self.sprite.set_colorkey(COLORKEY)

        self.image = self.sprite
        self.rect = self.image.get_rect(center = start_pos)

        self.mov_vec = vector(0,1)

        self.raycast_line_global = vector(0,0)
        self.raycast_line_local  = vector(0,0)
        self.start_ray_vis = ()
        self.end_ray_vis = ()

        self.lenght_raycast = 700

        self.z_hud_pos =vector(0,0)

        self.sprite_img = self.image
        self.offsprite_pos = vector(0,0)

        self.shoot_fps = 5

    def when_hits(self, hitted_object):
        if hitted_object.__class__.__name__ == "Dice":
            self.hits_dice(hitted_object)
        else:
            self.hits_other()

    def raycasting(self, gun):
        #todo later add hurtboxs and others
        self.raycast_line_handler(gun)

        collisions = autol.collision_sprites.sprites()
        dices = autol.dice_sprite.sprites()
        enemies = autol.enemies_sprite.sprites()

        all_to_collide = dices + collisions + enemies#all these sprites

        lowest_dist = [None, 10000, (0,0)]
        self.start_ray_vis = ()
        self.end_ray_vis = ()

        for collid in all_to_collide :
            clipped = collid.rect.clipline(self.raycast_line_global)
            if clipped != ():
                distance = vector(clipped[0]).distance_to(self.raycast_line_global[0])
                if distance < lowest_dist[1]:
                    lowest_dist[0] = collid
                    lowest_dist[1] = distance
                    lowest_dist[2] = clipped

        self.start_ray_vis = vector(self.raycast_line_local[0])
        if lowest_dist[0] != None:
            self.end_ray_vis = lowest_dist[2][0] - vector(self.raycast_line_global[0]) + vector(gun.muzzle_pos_local)
            self.when_hits(lowest_dist[0])
        else:
            self.end_ray_vis = vector(self.raycast_line_local[1])

    def raycast_line_handler(self,gun):
        # settings start and end of line
        self.raycast_line_global = (gun.muzzle_pos_global, \
                                    gun.muzzle_pos_global + vector(self.lenght_raycast, 0).rotate(
                                        -gun.operator.arm_angle))
        # settings start and end of line but on a local
        self.raycast_line_local = (gun.muzzle_pos_local, \
                                   gun.muzzle_pos_local + vector(self.lenght_raycast, 0).rotate(-gun.operator.arm_angle))

    def shooting_visualization(self,gun):
        pg.draw.line(gun.image, (150, 80, 40), self.start_ray_vis, self.end_ray_vis, 5)
        pg.draw.line(gun.image, (200, 200, 200), self.start_ray_vis, self.end_ray_vis, 2)

    def hits_dice(self,dice):
        pass

    def hits_other(self):
        pass

    def collide_handler(self):
        #collision with player
        if self.rect.colliderect(autol.player.rect):
            autol.player.card_inventory.append(self)
            self.kill()
        #TODO collision with world floor

    def update(self):
        self.collide_handler()
        self.sprite_img = self.image




class Dice(NewSprite):
    def __init__(self, start_pos, direction):
        super().__init__()
        autol.all_sprites.add(self)
        autol.dice_sprite.add(self)

        self.sprite_org = pg.image.load('../Jpgs/dice.png')
        self.sprite_org.set_colorkey(COLORKEY)
        self.sprite = self.sprite_org

        self.alpha = 130

        self.image = pg.Surface((20,20))
        self.image.fill(COLORKEY)
        self.image.set_colorkey(COLORKEY)
        self.image.set_alpha(self.alpha)
        self.rect = self.image.get_rect(center = start_pos)


        #move variable
        self.force = 12
        self.mov_var = vector(self.force,0)
        self.mov_var = self.mov_var.rotate(-direction)
        self.gravity = 0.2
        self.angle = 0
        if 90 < direction < 270:
            self.direction = direction /16
        elif 90> direction:
            self.direction = (direction-90)/5
        else:
            self.direction = (direction - 360)/4

        self.sprite_img = self.image
        self.offsprite_pos = vector(0, 0)

    def set_image(self):
        self.image = pg.Surface((20, 20))
        self.image.fill(COLORKEY)
        self.image.set_colorkey(COLORKEY)
        self.image.set_alpha(self.alpha)

    def collide_handler(self):
        for collider in autol.collision_sprites:
            if collider.rect.colliderect(self.rect):
                self.kill() #TODO for later, change into collide rect

    def rotate(self):
        self.set_image()
        self.sprite = pg.transform.rotate(self.sprite_org, self.angle)
        self.image.blit(self.sprite, (self.image.get_size()[0]/2 - self.sprite.get_size()[0]/2,\
                                      self.image.get_size()[1]/2 - self.sprite.get_size()[1]/2))
        self.angle +=self.direction

    def update(self):
        self.rotate()
        self.collide_handler()

        self.rect.x += self.mov_var.x
        self.mov_var.y += self.gravity
        self.rect.y += self.mov_var.y
        self.sprite_img = self.image

