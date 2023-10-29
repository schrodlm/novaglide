import pygame

from pygame.locals import *
import sys

from player import Player
from ball import Ball
from pygame import Vector2

pygame.init()

class Game():
    def __init__(self):

        pygame.display.set_caption('Novaglide')

        self.clock = pygame.time.Clock()
        self.dt = 0
        self.last_tick = pygame.time.get_ticks()
        self.screen_res = [1280, 720]

        self.screen = pygame.display.set_mode(self.screen_res, pygame.HWSURFACE, 32)

        self.entities = pygame.sprite.Group()
        self.solids = pygame.sprite.Group()

        self.player = Player(20,20)
        self.ball = Ball(100,100)
        
        self.entities.add(self.solids)
        self.entities.add(self.player)
        self.entities.add(self.ball)

        self.clock.tick(60)

        while 1:
            self.Loop()
            
    def Loop(self):
        # main game loop
        self.eventLoop()
        
        self.Tick()
        self.Draw()
        pygame.display.update()


    def eventLoop(self):
        # the main event loop, detects keypresses
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    self.reset()
                    self.maploader.load(2)
                    
                if event.key == K_SPACE:
                    self.player.jump()

    def Tick(self):
        self.ttime = self.clock.tick()
        self.mpos = pygame.mouse.get_pos()
        self.keys_pressed = pygame.key.get_pressed()

    # def reset(self):
    #     self.maploader.layers = []
    #     player = self.maploader.player
    #     self.entities.empty()
    #     self.solids.empty()
    #     self.player = player

    #     self.entities.add(self.player)

    def Draw(self):
        # self.screen.fill((150,150,150))
        self.screen.fill("purple")
        # for l in self.maploader.layers[::-1]:#Update layers (have to reverse list to blit properly)
        #     self.screen.blit(l.image, self.ball.apply_layer(l))                
        
        if pygame.sprite.collide_circle(self.player,self.ball) :
            # 1. Calculate the collision normal
            collision_normal = self.ball.rect.center - Vector2(self.player.rect.center)
            collision_normal.normalize_ip()  # Normalize the vector to have a magnitude of 1
        
            # 2. Determine the new speed of the ball
            speed_magnitude = 20  # You can adjust this value as needed
            self.ball.speed = collision_normal * speed_magnitude
        
        
        self.dt = self.clock.tick(60) / 1000
        self.player.update(self.dt)
        self.ball.update()
        
        for e in self.entities: #update blocks etc.
            self.screen.blit(e.image, e.rect)


Game()