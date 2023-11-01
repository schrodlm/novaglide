import pygame

from pygame.locals import *
import sys

from player import Player
from ball import Ball
from pygame import Vector2
from base_menu import MainMenu, OptionsMenu, CreditsMenu, LogInMenu

class Game():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Novaglide')

        self.running, self.playing = True,False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.WIDTH, self.HEIGHT = 1280, 720

        self.mpos = pygame.mouse.get_pos()
        
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.last_tick = pygame.time.get_ticks()
        self.screen_res = [self.WIDTH, self.HEIGHT]

        self.display = pygame.Surface(self.screen_res)
        self.screen = pygame.display.set_mode(self.screen_res, pygame.HWSURFACE, 32)

        self.entities = pygame.sprite.Group()
        self.solids = pygame.sprite.Group()

        self.player = Player(20,20)
        self.ball = Ball(100,100)
        
        self.entities.add(self.solids)
        self.entities.add(self.player)
        self.entities.add(self.ball)
        
        self.user_credentials = {"name":"", "password":""}

        self.clock.tick(60)

        self.main_menu = MainMenu(self)
        self.options_menu = OptionsMenu(self)
        self.credits_menu = CreditsMenu(self)
        self.login_menu = LogInMenu(self)

        self.curr_menu = LogInMenu(self)

    def game_loop(self):
        while self.playing:
        # main game loop
            self.check_events()
            self.Tick()
            self.Draw()
            self.reset_keys()

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

    def check_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
    
    
    def Tick(self):
        self.ttime = self.clock.tick()
        self.mpos = pygame.mouse.get_pos()
        self.keys_pressed = pygame.key.get_pressed()

    def Draw(self):
        self.display.fill((150,150,150))
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
            self.display.blit(e.image, e.rect)

        self.screen.blit(self.display, (0,0))
        pygame.display.update()