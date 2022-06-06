from json import load
from tracemalloc import start
import pygame, sys
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
text_color = (110, 110, 100)
display = pygame.display.set_mode((width, height))
pygame.display.set_caption(("FANTASTIC GAME NAME"))
running = False
loading_screen = True
upgrades = False
score = 0
last_score = 0
dots = 0
size = 50
size_cost = 100
small_font =  pygame.font.Font("Pokemon GB.ttf", 20)
middle_font = pygame.font.Font("Pokemon GB.ttf", 80)
home_font = pygame.font.Font("Pokemon GB.ttf", 40)

SCORE_UPDATE = pygame.USEREVENT + 1
BOX_DROP = pygame.USEREVENT
box_limit = 10
box_amount = 1

class button:
    def __init__(self, text, font_size, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.heigth = height
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font_size = font_size
        while 1:
            font =  pygame.font.Font("Pokemon GB.ttf", self.font_size)
            x, y = pygame.font.Font.size(font, self.text)
            if x > self.width:
                self.font_size -= 1
            if x <= self.width:
                break

    def draw_button(self):
        font = pygame.font.Font("Pokemon GB.ttf", self.font_size)
        draw = font.render(self.text, False, text_color)
        pygame.draw.rect(display, self.color, self.rect)
        display.blit(draw, (self.x + 3, self.y + self.heigth/2.7))        

    def update(self):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                pygame.draw.rect(display, active, self.rect)
                pygame.display.flip()
                pygame.time.wait(200)
                return True


start_button = button("Start", 30, 300, 300, 150, 50, deactive)
upgrade_button = button("Upgrades", 30, 300, 375, 150, 50, deactive)
back_button = button("Back", 30, 100, 100, 150, 50, deactive)

pygame.time.set_timer(SCORE_UPDATE, 500, 0)
pygame.time.set_timer(BOX_DROP, 500, 0)
def reset():
    global boxes, score, box_amount, box_limit
    boxes = []
    score = 0
    box_limit = 10
    box_amount = 1

def draw_text(x, y, middle, text, value, font_size):
    font = pygame.font.Font("Pokemon GB.ttf", font_size)
    a, b = pygame.font.Font.size(font, str(text) + str(value))
    draw = font.render(str(text) + str(value), False, (100, 100, 100))
    if middle:
        display.blit(draw, (x - a/2, y))
    if not middle:
        display.blit(draw, (x, y))

shooter = Shooter()

while loading_screen:
    dt = clock.tick(120) / 1000
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    if start_button.update():
        loading_screen = False
        running = True
    if upgrade_button.update():
        loading_screen = False
        upgrades = True

    display.fill(background)      
    # draw
    draw_text(200, 500, False, "Last Score: ", last_score, 30)
    upgrade_button.draw_button()
    start_button.draw_button()
    
    # game name
    a, b = pygame.font.Font.size(home_font, "FANTASTIC GAME NAME")
    draw = home_font.render("FANTASTIC GAME NAME", False, (150, 150, 150))
    display.blit(draw, (450 - a/2, 100))

    reset()
    pygame.display.flip()

    while upgrades:
        size_upgrade = button("Size:" + " -5 " + "Cost: " + str(size_cost), 30, 100, 175, 300, 50, deactive)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if back_button.update():
                upgrades = False
                loading_screen = True

            if size_upgrade.update():
                if dots >= size_cost:
                    if size >= 15:
                        dots -= size_cost
                        size -= 5
                        size_cost *= 2

                else:
                    pygame.draw.rect(display, background, size_upgrade)
                    draw_text(size_upgrade.x, size_upgrade.y + 10, False, "Insufficient Dots", "", 18)
                    pygame.display.flip()
                    pygame.time.wait(200)

        display.fill(background)
        draw_text(50, 50, False, "Dots: ", str(dots), 20)
        back_button.draw_button()
        size_upgrade.draw_button()
        pygame.display.flip()
    while running:
        if box_limit == score:
            box_limit += 5
            box_amount += 1

        player = pygame.Rect(shooter.position.x + shooter.width/2 - 50/2 , shooter.position.y - 6, size, size)
        # calculate deltatime
        dt = clock.tick(120) / 1000
        shooter.setDirection(0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.quit()

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
                dots += 1
                
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
        display.blit(draw, (450 - a/2, 50))
        # money
        a, b = pygame.font.Font.size(small_font, "Dots" + " " + str(dots))
        draw = small_font.render("Dots:" + " " + str(dots), False, (150, 150, 150))
        display.blit(draw, (25, 50))
            
        pygame.draw.rect(display, (200, 200, 200), player) # shooter
            
        for box in boxes:
            pygame.draw.rect(display, (50, 50, 50), (box.position.x, box.position.y - 30, 10, 10)) # boxes
            

        pygame.display.flip()

