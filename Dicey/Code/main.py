import time
import pygame
from settings import *
from loops import Loops




pygame.init()
screen = pygame.display.set_mode(WINDOWS_SIZE)
pygame.display.set_caption("Dicey")
clock = pygame.time.Clock()

loops = Loops()
next_time = time.time()
dt = 0



while True:
    dt = time.time() - next_time
    dt*=60
    next_time = time.time()

    loops.input_handler()
    loops.update_handler(dt)
    loops.display_handler()

    pygame.display.flip()
    clock.tick(FPS)


