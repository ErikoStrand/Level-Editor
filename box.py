import pygame
class Box:
    width = 10
    height = 10
    def __init__(self, x, y):
        self.position = pygame.Vector2()
        self.position.xy = x, y
        self.direction = 1
    def update(self, dt):
        self.position.xy = (self.position.x, self.position.y + self.direction*5*60*dt) 
    def setDirection(self, direction):
        self.direction = direction