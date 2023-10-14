import pygame
from pygame import Vector2
from player import Player
from ball import Ball
import settings

# Initialize game
pygame.init()




def checkCollision(p, b):
    return p.position.distance_to(b.position) < max(b.size,p.size)


#setup
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
dt = 0
player = Player(settings.WIDTH // 2, settings.HEIGHT // 2)
ball = Ball(100, 100)


#main loop
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("purple")
    player.draw()
    ball.draw()
    
    if checkCollision(player, ball):
        ball.speed = Vector2(8, 8)

    ball.checkAndHandleRebound()
    # moving the ball
    ball.move()
    # moving the player
    pygame.display.flip()
    dt = clock.tick(60) / 1000
    player.update(dt)    

pygame.quit()
