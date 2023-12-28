import pygame
from pygame.math import Vector2
from configuration_mod import Config
# --------------------------BALL-----------------------------------

class Ball(pygame.sprite.Sprite):

    def __init__(self, x: float, y: float, config: Config):
        pygame.sprite.Sprite.__init__(self)
        self.config = config
        #radius
        self.radius = 20

        #ball should spawn in a middle of a field
        self.x, self.y = self.config["resolution"]["width"]/2, self.config["resolution"]["height"]/2
        self.speed = (x, y)
        

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
        if self.x <= 0 or self.x >= self.config["resolution"]["width"]:
            self.speed.x = -self.speed.x
        if self.y <= 0 or self.y >= self.config["resolution"]["height"]:
            self.speed.y = -self.speed.y

if __name__ == "__main__":
    raise RuntimeError("This module is designed for import only.")
