"""Module containing the Game object which acts as a top-level 
game menu switch.
Raises
------
RuntimeError
    When called as the main script and not imported
"""

import sys
import datetime
import json
import pygame
import pygame.locals
from networking.network import Network
from database.database_query import DBQuery
from game_objects.player import Player, Bot
from menu.menu import MainMenu, SettingsMenu, CreditsMenu, LogInMenu, RankedMenu, MatchHistoryMenu
from match.match import Match1v1
from game_objects.ball import Ball
from menu.endscreen import EndScreenMenu

class Game():
    def __init__(self, config):
        pygame.init()
        pygame.display.set_caption("Novaglide")
        #config file
        self.config = config
        self.net = Network()
        #client receives his id on startup
        self.client_id = "uknown"
        #flag indicating whether client is connected to
        #the server(whether connection is active)
        self.online = False
        #offline/waiting_for_approval/online(in menu)/queued/ingame
        self.status = "offline"
        
        
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

        self.curr_menu = self.login_menu



    def start_match(self):
        
        player = Player(self.user_credentials["name"], 100,100,self.config)
        bot = Bot(100, 100,self.config)
        ball = Ball(400,400,self.config)
    
        curr_match = Match1v1(self.display, player, bot, ball)

        
        while curr_match.playing is True:
            curr_match.match_loop()
            self.Draw()
            self.Tick()
            self.reset_keys()

        match_stats = curr_match.get_match_stats()
        self.play_match = False
        self.curr_menu = EndScreenMenu(self, match_stats)
        print(match_stats.stats.get(player))
        
        
    

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

    def parse_data(self, flag, data):
        data = {"time":datetime.datetime.now(),
                "sender":self.client_id, 
                "flag":flag,
                "data":data}
        return data
    def unpack_login_data(self, data):
        return (data["data"][0], data["data"][1], data["data"][2])
    def unpack_elo_data(self, data):
        return (data["data"][0], data["data"][1])
    def unpack_winrate_data(self, data):
        return data["data"][0]
    def unpack_challenger_data(self, data):
        return data["data"]
if __name__ == "__main__":
    raise RuntimeError("This module is designed for import only.")