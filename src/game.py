"""Module containing the Game object which acts as a top-level 
game menu switch.
Raises
------
RuntimeError
    When called as the main script and not imported
"""

import sys
import datetime
import pygame
import pygame.locals
import utilities
from networking.network import Network
from database.database_query import DBQuery
from game_objects.player import Player
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
        self.screen_res = [self.WIDTH, self.HEIGHT]

        self.display = pygame.Surface(self.screen_res)
        self.screen = pygame.display.set_mode(self.screen_res, pygame.HWSURFACE, 32)
        #indicating whether player is ready to play
        self.play_match = False

        self.user_credentials = {"name":"", "password":""}

        self.keys_pressed = pygame.key.get_pressed()

        self.main_menu = MainMenu(self)
        self.settings_menu = SettingsMenu(self)
        self.credits_menu = CreditsMenu(self)
        self.login_menu = LogInMenu(self)
        self.ranked_menu = RankedMenu(self)
        self.match_history_menu = MatchHistoryMenu(self)
        #start on the login screen
        self.curr_menu = self.login_menu
        #game elements that will be ploted to the screen
        self.bg = pygame.image.load("./../resources/rink_" + str(self.settings_menu.map_indx + 1)+ ".jpg").convert_alpha()
        self.player_1 = Player("unknown", 100,360,self.config, color = "green")
        self.player_2 = Player("unknown", 1180,360,self.config, color = "blue")
        self.ball = Ball(self.config)
        
        goal_height = self.config["match"]["goal_height"]
        goal_width = self.config["match"]["goal_width"]
        self.goal_1 = pygame.Rect(0, (self.display.get_height() - goal_height) // 2, goal_width, goal_height)
        self.goal_2 = pygame.Rect(self.display.get_width() - goal_width, (self.display.get_height() - goal_height) // 2, goal_width, goal_height)
        self.border_width = self.config["match"]["border_width"]
        self.border = self.display.get_rect()
        
    def start_match(self, match_data):
        """{"time":"datetime.datetime.now()",
        "sender":"server", "flag":"1v1_game",
        "data":[your_side,game_time,goals_1,goals_2, p_1_name,p_2_name
        ,p1_pos_x, p_1_pos_y,p1_mouse_pos_x, 
        p_1_mouse_pos_y, p_1_dash_cooldown,p_1_hook_cooldown,p_1_hooking,
        p_2_pos_x, p2_pos_y,p_2_mouse_pos_x, 
        p_2_mouse_pos_y, p_2_dash_cooldown,p_2_hook_cooldown,p_2_hooking,ball_x,ball_y]}
        """
        #self.player_1.name = match_data["data"][4]
        #self.player_1.name = match_data["data"][5]
        #curr_match = Match1v1(self.display, player, bot, ball)

        while self.status == "ingame":
            self.Draw(match_data)
            self.check_inputs()
            self.share_inputs()
        #match_stats = curr_match.get_match_stats()
        self.play_match = False
        #self.curr_menu = EndScreenMenu(self, match_stats)
        
    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

    def share_inputs(self):
        self.parse_data("ingame",[self.keys_pressed, self.mpos])
    
    def check_inputs(self):
        self.mpos = pygame.mouse.get_pos()
        self.keys_pressed = pygame.key.get_pressed()
        if self.status == "ingame":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
    def Draw(self, match_data):
        #draw background
        self.screen.blit(self.display, (0,0))
        self.display.fill((150,150,150))
        self.display.blit(self.bg,(0,0))
        #draw border
        pygame.draw.rect(self.display, "red", self.goal_1)  # White goal
        pygame.draw.rect(self.display, "red", self.goal_2)  # White goal
        pygame.draw.rect(self.display, (255, 255, 255), self.border, self.border_width)

        #update all positions according to the server
        
        self.player_1.setRect()
        self.player_2.setRect()
        self.ball.setRect()
        for e in (self.player_1, self.player_2, self.ball): #update blocks etc.
            self.display.blit(e.image, e.rect)
        
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

    def unpack_match_history_data(self, data):
        return (data["data"][0],data["data"][1])

if __name__ == "__main__":
    raise RuntimeError("This module is designed for import only.")
