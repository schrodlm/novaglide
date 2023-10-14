import pygame
from pygame import Vector2
import settings

# --------------------------PLAYER-----------------------------------
class Player:
    def __init__(self, x, y):
        self.position = Vector2(x, y)
        self.size = 40
        self.future_position = Vector2(x, y)

    def move(self, dx, dy):
        self.future_position += dx,dy
        if self.future_position.x > 0 and self.future_position.x < settings.WIDTH and self.future_position.y > 0 and self.future_position.y < settings.HEIGHT:
            self.position += dx,dy
            
        self.future_position = self.position.copy()
            
    def draw(self):
        pygame.draw.circle(settings.SCREEN, "red", self.position, self.size)

    def update(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.move(0, -300*dt)
        if keys[pygame.K_s]:
            self.move(0, 300*dt)
        if keys[pygame.K_a]:
            self.move(-300*dt, 0)
        if keys[pygame.K_d]:
            self.move(300*dt, 0)