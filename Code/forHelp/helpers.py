import pygame as pg
import math

import pygame.math

import Code.forHelp.autoload


def clamp(value, min_value, max_value):
    return max(min_value,min(value,max_value))

def inputHandler(key):
    keys = pg.key.get_pressed()
    if keys[key]:
        return True
    else:
        return False

def mouse_input_handler(mouse_key):
    real_mouse_keys = pg.mouse.get_pressed()
    if mouse_key == real_mouse_keys: return True

def move_towards(value, byHowMuch, theEnd):
    if value > theEnd:
        value -= byHowMuch
        if value < theEnd:
            value = theEnd
    elif value < theEnd:
        value += byHowMuch
        if value > theEnd:
            value = theEnd
    return value

def mouse_local_center_pos():
    return (pygame.mouse.get_pos()[0] -pygame.display.get_window_size()[0]/2,\
            pygame.mouse.get_pos()[1] -pygame.display.get_window_size()[1]/2)

#for spliting <Dice Sprite (in 1 group)> into Dice Sprite
def split_sprite_name(name):
    sprite = str(name)
    sprite = sprite.split('(')[0]
    sprite = sprite[1:]
    return sprite

#idk why it doesn't work
#def angle_of_vectors(vec1,vec2): #need to be modified
#    a,b = vec1
#    c,d = vec2
#
#    dotProduct = a * c + b * d
#    # for three dimensional simply add dotProduct = a*c + b*d  + e*f
#    modOfVector1 = math.sqrt(a * a + b * b) * math.sqrt(c * c + d * d)
#    # for three dimensional simply add modOfVector = math.sqrt( a*a + b*b + e*e)*math.sqrt(c*c + d*d +f*f)
#    if modOfVector1 == 0: modOfVector1 = 1
#    angle = dotProduct / modOfVector1
#    return math.degrees(math.acos(angle))

def angle_of_vector(vec2):
    a,b = 1,0
    c,d = vec2

    dotProduct = a * c + b * d
    # for three dimensional simply add dotProduct = a*c + b*d  + e*f
    modOfVector1 = math.sqrt(a * a + b * b) * math.sqrt(c * c + d * d)
    # for three dimensional simply add modOfVector = math.sqrt( a*a + b*b + e*e)*math.sqrt(c*c + d*d +f*f)
    if modOfVector1 ==0: modOfVector1 =1
    angle = dotProduct / modOfVector1
    if d >0:
        return 360-math.degrees(math.acos(angle))
    else:
        return math.degrees(math.acos(angle))


#hard to decide if they should have be in group and updated in loops or in their own objects
class Timer():
    def __init__(self, duration, func = None):
        self.duration = duration
        self.func = func
        self.start_time = 0
        self.active = False


    def activate(self):
        self.active = True
        self.start_time = pg.time.get_ticks()

    def deactivate(self):
        self.active = False
        self.start_time = 0

    #when timer runned out of time keep using func
    def update(self):
        current_time = pg.time.get_ticks()
        if current_time - self.start_time >= self.duration:
            self.deactivate()
            if self.func:
                self.func()

    #when timer runned out, use func once and deactive
    def once_func_update(self):
        current_time = pg.time.get_ticks()
        if current_time - self.start_time >= self.duration:
            if self.func and self.active:
                self.func()
            self.deactivate()


class Camera:
    '''
    Basic layout of how cameras will work
    '''
    #TODO new following target camera movement, layer camera, layer following camera
    #TODO more smooth movement
    def __init__(self,sprite_group, start_target):
        self.camera_sprites = sprite_group #only for pygame sprites
        self.offset = pygame.math.Vector2()
        self.win_size = pygame.display.get_window_size()
        self.step = self.win_size[0]/100

        self.x, self.y = start_target
        self.x= self.x - self.win_size[0]/2
        self.y =self.y - self.win_size[1]/2

        self.max_dis_mouse = 1.3

    def clipped_movement(self,target_position):
        self.x, self.y = target_position
        target_local_pos = (target_position[0] - self.x + pygame.display.get_window_size()[0]/2,\
                            target_position[1] - self.y + pygame.display.get_window_size()[1]/2)

        self.x= self.x - self.win_size[0]/2
        self.y =self.y - self.win_size[1]/2

        for sprite in self.camera_sprites:
            pygame.display.get_surface().blit(sprite.image, sprite.rect.topleft - pygame.math.Vector2(self.x, self.y))


        return target_local_pos


    def mouse_depend_movement(self,target_position):
        self.x, self.y = target_position
        self.x = int(self.x - self.win_size[0] + pygame.mouse.get_pos()[0] - mouse_local_center_pos()[0]/self.max_dis_mouse)
        self.y = int(self.y - self.win_size[1] + pygame.mouse.get_pos()[1] - mouse_local_center_pos()[1]/self.max_dis_mouse)


        #it is not perfect calculation, but thanks to ignoring .0 nums,
        # we can be sure that to win size 4000,3000 it will work good
        target_local_pos = (int(target_position[0] - self.x + pygame.display.get_window_size()[0] / 100000), \
                            int(target_position[1] - self.y + pygame.display.get_window_size()[1] / 100000))

        for sprite in self.camera_sprites:
            pygame.display.get_surface().blit(sprite.image, sprite.rect.topleft - pygame.math.Vector2(self.x, self.y))
        return target_local_pos

