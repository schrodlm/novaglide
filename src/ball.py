import pygame
from pygame.math import Vector2
import settings

# --------------------------BALL-----------------------------------

class Ball:
    def __init__(self, x, y):
        self.position = Vector2(x, y)
        self.speed = Vector2(0, 0)
        self.size = 20
        print(self.position.x)
        print(self.position.y)

    def move(self):
        self.position += self.speed

    def draw(self):
        pygame.draw.circle(settings.SCREEN, "blue", self.position, self.size)

    def checkAndHandleRebound(self):
        if self.position.x <= 0 or self.position.x >= settings.WIDTH:
            self.speed.x = -self.speed.x
        if self.position.y <= 0 or self.position.y >= settings.HEIGHT:
            self.speed.y = -self.speed.y

