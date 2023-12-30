"""Module containing the Game object which acts as a top-level 
game menu switch.
Raises
------
RuntimeError
    When called as the main script and not imported
"""

import sys
import pygame
import pygame.locals
from database_query import DBQuery
from player import Player, Bot
from menu import MainMenu, SettingsMenu, CreditsMenu, LogInMenu, RankedMenu, MatchHistoryMenu
from match import Match1v1
from ball import Ball
from endscreen import EndScreenMenu

class Game():
    def __init__(self, config):
        pygame.init()
        pygame.display.set_caption('Novaglide')
        self.config = config
        self.running, self.playing = True,False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.WIDTH, self.HEIGHT = self.config["resolution"]["width"], self.config["resolution"]["height"]

        self.mpos = pygame.mouse.get_pos()

        self.clock = pygame.time.Clock()
        self.dt = 0
        self.last_tick = pygame.time.get_ticks()
        self.screen_res = [self.WIDTH, self.HEIGHT]

        self.display = pygame.Surface(self.screen_res)
        self.screen = pygame.display.set_mode(self.screen_res, pygame.HWSURFACE, 32)
        self.play_match = False



        self.user_credentials = {"name":"", "password":""}
        self.query = DBQuery(self.config)

        self.ttime = self.clock.tick()
        self.keys_pressed = pygame.key.get_pressed()

        self.clock.tick(60)

        self.main_menu = MainMenu(self)
        self.settings_menu = SettingsMenu(self)
        self.credits_menu = CreditsMenu(self)
        self.login_menu = LogInMenu(self)
        self.ranked_menu = RankedMenu(self)
        self.match_history_menu = MatchHistoryMenu(self)
        self.endscreen_menu = EndScreenMenu(self, "test2")

        self.curr_menu = self.login_menu



    def start_match(self):
        
        player = Player(100,100,self.config)
        bot = Bot(100, 100,self.config)
        ball = Ball(400,400,self.config)
    
        curr_match = Match1v1(self.display, player, bot, ball)

        
        while curr_match.playing is True:
            curr_match.match_loop()
            self.Draw()
            self.Tick()
            self.reset_keys()

        self.play_match = False
        self.curr_menu = EndScreenMenu(self, "test")
        
        
    

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
            if event.type == pygame.QUIT:
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
 
    def check_inputs(self):
        #TODO:menu needs to update keyboard and mouse input but should not tick the game clock
        #write different Tick_menu() without self.ttime? idk yet
        self.mpos = pygame.mouse.get_pos()
        self.keys_pressed = pygame.key.get_pressed()

    def Draw(self):   
        self.screen.blit(self.display, (0,0))
        pygame.display.update()

if __name__ == "__main__":
    raise RuntimeError("This module is designed for import only.")