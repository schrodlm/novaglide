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

        self.clock.tick(60)

        self.main_menu = MainMenu(self)
        self.options_menu = OptionsMenu(self)
        self.credits_menu = CreditsMenu(self)
        self.login_menu = LogInMenu(self)

        self.curr_menu = LogInMenu(self)

    def game_loop(self):
        while self.playing:
        # main game loop
            self.check_events(name = "game")
            self.Tick()
            self.Draw()
            self.reset_keys()

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

    def check_events(self, name: str):
        if name == "credits_menu" or name == "game":
            # the main event loop, detects keypresses
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
        
        if name == "main_menu":
            for event in pygame.event.get():
                # closing the game with mouse
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.main_menu.play_1v1_button.check_for_input(self.mpos):
                        self.playing = True
                        self.main_menu.run_display = False
                    if self.main_menu.play_2v2_button.check_for_input(self.mpos):
                        #TODO: implement multiplayer
                        print("2v2 selected")
                    if self.main_menu.settings_button.check_for_input(self.mpos):
                        self.main_menu.run_display = False
                        self.curr_menu = self.options_menu

                    if self.main_menu.back_button.check_for_input(self.mpos):
                        self.main_menu.run_display = False
                        self.curr_menu = self.login_menu

                    if self.main_menu.ranked_button.check_for_input(self.mpos):
                        #TODO: finish 
                        print("ranked selected")
                    if self.main_menu.credits_button.check_for_input(self.mpos):
                        self.main_menu.run_display = False
                        self.curr_menu = self.credits_menu

                         
        if name == "login_screen":
            for event in pygame.event.get():
                # closing the game with mouse
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.login_menu.log_in_button.check_for_input(self.mpos):
                        self.login_menu.user_credentials.append(self.login_menu.username_input.text)
                        self.login_menu.user_credentials.append(self.login_menu.password_input.text)
                        self.curr_menu.run_display = False
                        self.curr_menu = self.main_menu

                for box in self.login_menu.input_boxes:
                    box.handle_event(event)
            for box in self.login_menu.input_boxes:
                box.draw_updated(self.display)
            
        #TODO: to be created
        if name == "options_menu":
            ...

    
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