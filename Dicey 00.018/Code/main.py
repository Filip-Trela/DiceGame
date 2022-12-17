import time
import pygame
from settings import *
from loops import Loops

"""
Version 00.018
"""

#important todo
#enemy for later, slowing down time when dice thrown
#spadlo do 55 fps'ow, jebac


pygame.init()
screen = pygame.display.set_mode(WINDOWS_SIZE) #flags= FLAGS
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






