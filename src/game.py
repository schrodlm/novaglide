import sys
import pygame
import pygame.locals
from pygame import Vector2
from database_query import DBQuery
from player import Player, Bot
from ball import Ball
from menu import MainMenu, SettingsMenu, CreditsMenu, LogInMenu, RankedMenu, MatchHistoryMenu
from match import Match1v1

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
        self.play_match = False



        self.user_credentials = {"name":"", "password":""}
        self.query = DBQuery()

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

        self.player = Player(20,20)
        self.bot = Bot(100, 100)
        self.curr_match = Match1v1(self, self.player, self.bot)

    def start_match(self):
        if(self.play_match == True):
            self.curr_match.match_loop()
    

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
        #TODO: přidano i do init? pylint to nefeeluje mimo něj
        self.ttime = self.clock.tick()
        self.mpos = pygame.mouse.get_pos()
        self.keys_pressed = pygame.key.get_pressed()
 
    def Check_inputs(self):
        #TODO:menu needs to update keyboard and mouse input but should not tick the game clock
        #write different Tick_menu() without self.ttime? idk yet
        self.mpos = pygame.mouse.get_pos()
        self.keys_pressed = pygame.key.get_pressed()

    def Draw(self):   
        self.screen.blit(self.display, (0,0))
        pygame.display.update()
