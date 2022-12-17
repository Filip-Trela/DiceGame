import pygame



#sprite autoloads
all_sprites = pygame.sprite.Group()
collision_sprites = pygame.sprite.Group()
dice_sprite = pygame.sprite.GroupSingle()
enemies_sprite = pygame.sprite.Group()

#image autoloads
all_images = []

local_pos_target = (0,0)

player_max_health = 100
player = None

scroll_y = 0


