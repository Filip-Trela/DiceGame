import time
import pygame
from settings import *
from loops import Loops


#important todos


pygame.init()
screen = pygame.display.set_mode(WINDOWS_SIZE ) #flags= FLAGS
blit_surface = pg.Surface(BLIT_SIZE)
pygame.display.set_caption("Dicey")
clock = pygame.time.Clock()


loops = Loops()



while True:

    loops.input_handler()
    loops.update_handler()
    loops.display_handler(blit_surface)

    pygame.display.flip()
    clock.tick(FPS)




