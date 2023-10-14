import pygame
from pygame.math import Vector2
import settings

# --------------------------BALL-----------------------------------

class Ball(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        #radius
        self.radius = 20
        self.x, self.y = x,y


        self.rect = pygame.Rect(x - self.radius, y - self.radius,
                                2 * self.radius, 2 * self.radius)
        
        self.image = pygame.Surface((2 * self.radius, 2 * self.radius)
                                    , pygame.SRCALPHA)  # make it transparent
        
        self.image = self.image.convert_alpha()

        pygame.draw.circle(self.image, "black",
            (self.radius, self.radius), self.radius)

        self.speed = Vector2(0, 0)

    def update(self):
        #updating position based on speed
        self.x += self.speed.x
        self.y += self.speed.y
        #slowing down the ball
        self.speed.x /= 1.003
        self.speed.y /= 1.003
        self.checkAndHandleRebound()
        self.setRect()

    
    def setRect(self):
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius,
                                2 * self.radius, 2 * self.radius)


    def checkAndHandleRebound(self):
        if self.x <= 0 or self.x >= settings.WIDTH:
            self.speed.x = -self.speed.x
        if self.y <= 0 or self.y >= settings.HEIGHT:
            self.speed.y = -self.speed.y

