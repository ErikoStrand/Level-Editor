import pygame
class Shooter:
    position = pygame.Vector2()
    width = 50
    height = 50
    direction = 0
    hasBullet = True
    def __init__(self):
        self.position.xy = 450 - self.width/2, 800
    def setDirection(self, direction):
        self.direction = direction
    def update(self, dt):
        self.direction = 0
        keys = pygame.key.get_pressed()  #checking pressed keys
        if keys[pygame.K_LEFT]:
            self.direction = -1
        if keys[pygame.K_RIGHT]:
            self.direction = 1
        if (not(self.position.x < 0 and self.direction == -1) and not(self.position.x + self.width > 900 and self.direction == 1)):
            self.position.xy = (self.position.x + self.direction*320*dt, self.position.y) 
    def reset(self):
        self.position.xy = 450 - self.width/2, 800