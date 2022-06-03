import pygame, sys
import math

# colors
background_color = (0, 0, 0)
block_color = (255, 255, 255)

# screen
screen = pygame.display.set_mode((1600, 900)) # (x, y)
screen.fill(background_color)
# values


while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    pygame.display.flip()

