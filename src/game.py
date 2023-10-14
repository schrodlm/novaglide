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


player = Player(20,20)
ball = Ball(100,100)

#main loop
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("purple")

    dt = clock.tick(60) / 1000
    player.update(dt)
    ball.update()

    if pygame.sprite.collide_circle(player,ball) :
        # 1. Calculate the collision normal
        collision_normal = ball.rect.center - Vector2(player.rect.center)
        collision_normal.normalize_ip()  # Normalize the vector to have a magnitude of 1
    
        # 2. Determine the new speed of the ball
        speed_magnitude = 20  # You can adjust this value as needed
        ball.speed = collision_normal * speed_magnitude

    #drawing sprites on screen    
    screen.blit(player.image,player.rect)
    screen.blit(ball.image, ball.rect)



    pygame.display.flip()
      

pygame.quit()
