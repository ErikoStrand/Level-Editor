import pygame
import math
import time
import numpy as np
from shooter import Shooter
from box import Box
projectiles = []
boxes = []

clock = pygame.time.Clock()
pygame.init()
pygame.font.init
background = (255,255,255)
(width, height) = (900, 900)
deactive = (160, 160, 160)
active = (100, 100, 100)
display = pygame.display.set_mode((width, height))
pygame.display.set_caption(("FANTASTIC GAME NAME"))
running = False
loading_screen = True
score = 0
last_score = 0
middle_font = pygame.font.Font("Pokemon GB.ttf", 80)
home_font = pygame.font.Font("Pokemon GB.ttf", 40)
start_button = pygame.Rect(300, 300, 150, 50)
SCORE_UPDATE = pygame.USEREVENT + 1
BOX_DROP = pygame.USEREVENT
box_limit = 10
box_amount = 1

pygame.time.set_timer(SCORE_UPDATE, 500, 0)
pygame.time.set_timer(BOX_DROP, 500, 0)
def reset():
    global boxes, score, box_amount, box_limit
    boxes = []
    score = 0
    box_limit = 10
    box_amount = 1


shooter = Shooter()

while loading_screen:
    dt = clock.tick(120) / 1000
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loading_screen = False

    if event.type == pygame.MOUSEBUTTONDOWN:
        if start_button.collidepoint(event.pos):
            pygame.draw.rect(display, active, start_button)
            pygame.display.flip()
            pygame.time.wait(500)
            loading_screen = False
            running = True

    display.fill(background)      
    # draw
    a, b = pygame.font.Font.size(middle_font, str(last_score))
    draw = middle_font.render(str(last_score), False, (150, 150, 150))
    display.blit(draw, (450 - a/2, 450))
    pygame.draw.rect(display, deactive, start_button)
    a, b = pygame.font.Font.size(home_font, "FANTASTIC GAME NAME")
    draw = home_font.render("FANTASTIC GAME NAME", False, (150, 150, 150))
    display.blit(draw, (450 - a/2, 100))

    reset()
    pygame.display.flip()
    while running:
        if box_limit == score:
            box_limit += 5
            box_amount += 1

        player = pygame.Rect(shooter.position.x + shooter.width/2 - 50/2 , shooter.position.y - 6, 50, 50)
        # calculate deltatime
        dt = clock.tick(120) / 1000
        shooter.setDirection(0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == SCORE_UPDATE:
                score += 1

            if event.type == BOX_DROP:
                for x in range(box_amount):
                    y = np.random.randint(0, 100, 1)
                    boxes.append(Box(np.random.randint(0, 900), y))

        for box in boxes:
            box.update(dt)
            if box.position.y + box.height < 0 or box.position.y > 910:
                boxes.remove(box)

        shooter.update(dt)

            
        for box in boxes:
            if player.collidepoint(box.position.x, box.position.y - 20):
                last_score = 0
                last_score = score
                running = False
                loading_screen = True

        # draw
        display.fill(background)
        # score
        a, b = pygame.font.Font.size(middle_font, str(score))
        draw = middle_font.render(str(score), False, (150, 150, 150))
        display.blit(draw, (450 - a/2, 100))
        
            
        pygame.draw.rect(display, (200, 200, 200), player) # shooter
            
        for box in boxes:
            pygame.draw.rect(display, (50, 50, 50), (box.position.x, box.position.y - 30, 10, 10)) # boxes
            

        pygame.display.flip()

