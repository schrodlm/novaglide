"""_summary_

Returns:
    _type_: _description_
"""
import sys
import json
import pygame
import utilities
from abc import ABC, abstractmethod
from input_box import InputBox
from button import Button
from table import Table
from player import Player

class Menu(ABC):
    def __init__(self,game):
        self.game = game
        self.run_display = True
        self.mid_x = self.game.WIDTH // 2
        self.mid_y = self.game.HEIGHT // 2

    def blit_screen(self):
        self.game.screen.blit(self.game.display,(0,0))
        pygame.display.update()
        self.game.reset_keys()
    
    #ensuring that all menus implement these methods,
    #to make the API consistent
    @abstractmethod
    def display_menu(self):
        pass
    @abstractmethod
    def check_events(self):
        pass


class LogInMenu(Menu):
    def __init__(self, game):
        super().__init__(game)
        # log in button
        self.log_in_button = Button(image=None, pos=(self.mid_x, 460),
                                text_input="LOG IN", font=utilities.get_font(75),
                                base_color="black", hovering_color="aqua")
        # initializing input boxes for username and password
        self.username_input = InputBox(x = 440, y = 200, w = 400, h = 70, hide = False, config=self.game.config)
        self.password_input = InputBox(x = 440, y = 300, w = 400, h = 70, hide = True, config=self.game.config)
        # group same objects
        self.input_boxes = [self.username_input, self.password_input]
        self.error_present = False
        self.allow = None
        self.ignore_check_event = False
        
    def display_menu(self):
        self.username_input.text = ""
        self.password_input.text = ""
        self.run_display = True
        while self.run_display:
            self.game.check_inputs()
            self.game.display.fill((0,0,0))
            # draw background
            self.game.display.blit(utilities.get_image("background_main"), (0, 0))
            #draw instructions
            utilities.draw_text("Login with your nickname and password", 30,
                                self.mid_x, 150, self.game.display,self.game.config["colours"]["black"])
            if self.allow is not None and self.error_present:
                self.draw_error(self.allow)
            
            self.log_in_button.change_color(self.game.mpos)
            self.log_in_button.update(self.game.display)
            self.check_events()
            # draw input boxes on the screen
            self.blit_screen()

    def check_events(self):
        for event in pygame.event.get():
            # closing the game with mouse
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.log_in_button.check_for_input(self.game.mpos):
                    allowed = self.game.query.allow_user_credentials(self.username_input.text,self.password_input.text)
                    if allowed is not None:
                        self.allow = allowed
                    match self.allow:
                        case "known user" | "registering new user":
                            self.error_present = False
                            self.allow = None
                            self.run_display = False
                            self.game.curr_menu = self.game.main_menu
                            self.game.user_credentials["name"] = self.username_input.text
                            self.game.user_credentials["password"] = self.password_input.text
                            break
                        case "Make sure to fill both name and password" | "Incorrect password for this username":
                            self.error_present = True
            for box in self.input_boxes:
                box.handle_event(event)
        for box in self.input_boxes:
            box.draw_updated(self.game.display)
    def draw_error(self, message):
            utilities.draw_text(message, 30,
                    self.mid_x, 550, self.game.display, self.game.config["colours"]["black"])
class MainMenu(Menu):
    def __init__(self,game):
        super().__init__(game)
        self.buttons = pygame.sprite.Group()
        hovering_color = self.game.config["design"]["hovering_colour"]
        self.play_1v1_button = Button(image=None, pos=(self.mid_x, 300),
                                    text_input="Play 1v1", font=utilities.get_font(40),
                                    base_color="black", hovering_color=hovering_color)
        self.play_2v2_button = Button(image=None, pos=(self.mid_x, 370),
                                    text_input="Play 2v2", font=utilities.get_font(40),
                                    base_color="black", hovering_color=hovering_color)
        self.match_history_button = Button(image=None, pos=(self.mid_x, 440),
                                    text_input="Match history", font=utilities.get_font(40),
                                    base_color="black", hovering_color=hovering_color)
        self.ranked_button = Button(image=None, pos=(self.mid_x, 510),
                                    text_input="Ranked system", font=utilities.get_font(40),
                                    base_color="black", hovering_color=hovering_color)
        self.back_button = Button(image=utilities.get_image("back_arrow"), pos=(70, 100),
                                    text_input="", font=utilities.get_font(40),
                                    base_color=(133, 88, 255), hovering_color=hovering_color)
        self.settings_button = Button(image=None, pos=(self.mid_x, 580),
                                    text_input="Settings", font=utilities.get_font(40),
                                    base_color="black", hovering_color=hovering_color)
        self.credits_button = Button(image=None, pos=(self.mid_x, 650),
                                    text_input="Credits", font=utilities.get_font(40),
                                    base_color="black", hovering_color=hovering_color)
        #Grouping buttons
        self.buttons.add(self.play_1v1_button)
        self.buttons.add(self.play_2v2_button)
        self.buttons.add(self.match_history_button)
        self.buttons.add(self.ranked_button)
        self.buttons.add(self.back_button)
        self.buttons.add(self.settings_button)
        self.buttons.add(self.credits_button)
        #creating texts and their rectangles
        self.logged_user_text = utilities.get_font(40).render(
                    self.game.user_credentials.get("name"), True, self.game.config["colours"]["aqua"])
        self.logged_user_rect = self.logged_user_text.get_rect(topleft=(15,15))

        self.main_menu_text = utilities.get_font(100).render(
                    "NOVAGLIDE", True, "black")
        self.main_menu_rect = self.main_menu_text.get_rect(center=(self.mid_x, 150))

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            #tick and fill new background
            self.game.check_inputs()
            self.game.display.fill((0,0,0))
            self.game.display.blit(utilities.get_image("background_main"), (0, 0))
            #need to regenerate every time because the name is dynamically changing
            self.logged_user_text = utilities.get_font(40).render(
            self.game.user_credentials.get("name"), True, self.game.config["colours"]["aqua"])
            self.logged_user_rect = self.logged_user_text.get_rect(topleft=(15,15))
            #draw texts
            self.game.display.blit(self.logged_user_text, self.logged_user_rect)
            self.game.display.blit(self.main_menu_text, self.main_menu_rect)
            #check all events
            self.check_events()
            #update all buttons
            for button in self.buttons:
                button.change_color(self.game.mpos)
            self.buttons.update(self.game.display)
            self.blit_screen()

    def check_events(self):
        for event in pygame.event.get():
            # closing the game with mouse
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.play_1v1_button.check_for_input(self.game.mpos):
                    self.run_display = False
                    self.game.play_match = True
                    print("1v1 selected")


                if self.play_2v2_button.check_for_input(self.game.mpos):
                    #TODO: implement multiplayer
                    print("2v2 selected")

                if self.settings_button.check_for_input(self.game.mpos):
                    self.run_display = False
                    self.game.curr_menu = self.game.settings_menu

                if self.back_button.check_for_input(self.game.mpos):
                    self.run_display = False
                    self.game.curr_menu = self.game.login_menu
                    self.game.user_credentials = {"name":"", "password":""}

                if self.ranked_button.check_for_input(self.game.mpos):
                    self.run_display = False
                    self.game.curr_menu = self.game.ranked_menu
                if self.match_history_button.check_for_input(self.game.mpos):
                    self.run_display = False
                    self.game.curr_menu = self.game.match_history_menu
                
                if self.credits_button.check_for_input(self.game.mpos):
                    self.run_display = False
                    self.game.curr_menu = self.game.credits_menu


class SettingsMenu(Menu):
    def __init__(self,game):
        super().__init__(game)
        #load settings JSON
        self.loaded_settings = utilities.get_settings()
        self.music = self.loaded_settings["Music"]

        self.volume = self.loaded_settings["Volume"]
        self.next_volume = self.volume

        self.max_map_indx = 2
        self.map_indx = int(self.loaded_settings["Map"][-5]) - 1
        self.next_map_indx = 0
        self.maps_ordered = utilities.get_ordered_maps()
        self.map = self.maps_ordered[self.map_indx]

        self.profile_picture = self.loaded_settings["ProfilePicture"]

        self.controls = self.loaded_settings["Controls"]
        #using player to plot skin preview
        self.player = Player(200,self.mid_y + 100, self.game.config, 100)
        #group of all buttons
        self.buttons = pygame.sprite.Group()

        #music arrows
        self.music_button_left_arrow = Button(image=utilities.get_image("left_arrow"),
                                    pos=(self.mid_x - 100, 170),
                                    text_input="", font=utilities.get_font(40),
                                    base_color="black", hovering_color="aqua")
        self.music_button_right_arrow = Button(image=utilities.get_image("right_arrow"),
                                    pos=(self.mid_x + 100, 170),
                                    text_input="", font=utilities.get_font(40),
                                    base_color="black", hovering_color="aqua")
        #volume arrows
        self.volume_button_left_arrow = Button(image=utilities.get_image("left_arrow"),
                                    pos=(self.mid_x - 100, 310),
                                    text_input="", font=utilities.get_font(40),
                                    base_color="black", hovering_color="aqua")
        self.volume_button_right_arrow = Button(image=utilities.get_image("right_arrow"),
                                    pos=(self.mid_x + 100, 310),
                                    text_input="", font=utilities.get_font(40),
                                    base_color="black", hovering_color="aqua")
        #controls arrows
        self.controls_button_left_arrow = Button(image=utilities.get_image("left_arrow"),
                                    pos=(self.mid_x - 120, 450),
                                    text_input="", font=utilities.get_font(40),
                                    base_color="black", hovering_color="aqua")
        self.controls_button_right_arrow = Button(image=utilities.get_image("right_arrow"),
                                    pos=(self.mid_x + 120, 450),
                                    text_input="", font=utilities.get_font(40),
                                    base_color="black", hovering_color="aqua")
        #map arrows
        self.map_button_left_arrow = Button(image=utilities.get_image("left_arrow"),
                                    pos=(980 - 120, 150),
                                    text_input="", font=utilities.get_font(40),
                                    base_color="black", hovering_color="aqua")
        self.map_button_right_arrow = Button(image=utilities.get_image("right_arrow"),
                                    pos=(980 + 120, 150),
                                    text_input="", font=utilities.get_font(40),
                                    base_color="black", hovering_color="aqua")
        #exit_button
        self.exit_button = Button(image=utilities.get_image("back_arrow"), pos=(70, 50),
                                    text_input="", font=utilities.get_font(40),
                                    base_color=(133, 88, 255), hovering_color="aqua")
        #Grouping buttons
        self.buttons.add(self.volume_button_left_arrow)
        self.buttons.add(self.volume_button_right_arrow)
        self.buttons.add(self.music_button_left_arrow)
        self.buttons.add(self.music_button_right_arrow)
        self.buttons.add(self.controls_button_left_arrow)
        self.buttons.add(self.controls_button_right_arrow)
        self.buttons.add(self.map_button_left_arrow)
        self.buttons.add(self.map_button_right_arrow)
        self.buttons.add(self.exit_button)


    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_inputs()
            self.check_events()
            self.game.display.fill((0,0,0))
            self.game.display.blit(utilities.get_image("background_main"), (0, 0))
            #Music settings
            utilities.draw_text("Music", 40, self.mid_x, 100, self.game.display, self.game.config["colours"]["black"])
            #music settings
            if self.music:
                utilities.draw_text("ON", 30, self.mid_x, 170, self.game.display)
            else:
                utilities.draw_text("OFF", 30, self.mid_x, 170, self.game.display)
            #Volume settings
            utilities.draw_text("Volume", 40, self.mid_x, 240, self.game.display, self.game.config["colours"]["black"])
            utilities.draw_text(utilities.convert_volume(self.volume), 30,
            self.mid_x, 310, self.game.display)
            #Map choice
            utilities.draw_text("Map", 40, 980, 100, self.game.display, self.game.config["colours"]["black"])
            utilities.draw_text(utilities.get_map_names(self.map), 30, 980, 150, self.game.display)
            #map preview
            self.game.display.blit(
            pygame.transform.rotate(pygame.image.load(self.map).convert_alpha(), 90),
            (840, 170))
            #skin preview
            utilities.draw_text("Your skin", 30, 200, 200, self.game.display)
            #bliting player skin
            #TODO: make more skins that will be circular in class player
            self.game.display.blit(self.player.image, self.player.rect)
            #controls settings
            utilities.draw_text("Controls", 40, self.mid_x, 380, self.game.display, self.game.config["colours"]["black"])
            if self.controls == "wsad":
                utilities.draw_text("W S A D", 30, self.mid_x, 450, self.game.display)
            if self.controls == "arrows":
                utilities.draw_text("Arrows", 30, self.mid_x, 450, self.game.display)
            #update/draw all buttons
            for button in self.buttons:
                button.change_color(self.game.mpos)
            self.buttons.update(self.game.display)
            self.blit_screen()


    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                #music button revert
                if (self.music_button_right_arrow.check_for_input(self.game.mpos) or
                    self.music_button_left_arrow.check_for_input(self.game.mpos)):
                    self.music = not self.music

                #volume changing
                if self.volume_button_right_arrow.check_for_input(self.game.mpos):
                    self.next_volume = self.volume + 1
                    if self.next_volume <= 10 and self.next_volume >= 0:
                        self.volume = self.next_volume
                if self.volume_button_left_arrow.check_for_input(self.game.mpos):
                    self.next_volume = self.volume - 1
                    if self.next_volume <= 10 and self.next_volume >= 0:
                        self.volume = self.next_volume

                #controls changing
                if (self.controls_button_right_arrow.check_for_input(self.game.mpos) or
                    self.controls_button_left_arrow.check_for_input(self.game.mpos)):
                    if self.controls == "wsad":
                        self.controls = "arrows"
                    else:
                        self.controls = "wsad"
                #change map
                if self.map_button_right_arrow.check_for_input(self.game.mpos):
                    self.next_map_indx = self.map_indx + 1
                    if self.next_map_indx <= self.max_map_indx and self.next_map_indx >= 0:
                        self.map_indx = self.next_map_indx
                if self.map_button_left_arrow.check_for_input(self.game.mpos):
                    self.next_map_indx = self.map_indx - 1
                    if self.next_map_indx <= self.max_map_indx and self.next_map_indx >= 0:
                        self.map_indx = self.next_map_indx
                #change it immediately so it gets saved
                self.map = self.maps_ordered[self.map_indx]
                #save new settings to json
                self.save_settings()
                #return to main menu
                if self.exit_button.check_for_input(self.game.mpos):
                    self.run_display = False
                    self.game.curr_menu = self.game.main_menu
    def save_settings(self):
        #TODO:open settings only as seperate window so it can be changed ingame
        #+ notify game that settings changed?
        new_settings = {}
        new_settings["Music"] = self.music
        new_settings["Volume"] = self.volume
        new_settings["Map"] = self.map
        new_settings["ProfilePicture"] = self.profile_picture
        new_settings["Controls"] = self.controls
        with open("./../settings/settings.json", 'w',encoding="UTF-8") as stgs:
            json.dump(new_settings, stgs)

class RankedMenu(Menu):
    def __init__(self,game):
        super().__init__(game)
        self.elements = pygame.sprite.Group()
        self.back_button_rm = Button(image=utilities.get_image("back_arrow"), pos=(70, 50),
                            text_input="", font=utilities.get_font(40),
                            base_color=(133, 88, 255), hovering_color=self.game.config["colours"]["aqua"])
        self.elo, self.division = self.get_my_elo()
        self.player_preview = Player(170,250, self.game.config,100)
        self.winrate = self.get_winrate()
        self.challenger_table = Table(self.game.config,header="CHALLENGERS",cols_sizes=[50,350,100,120])
        #challenger table buttons
        #will change the preview (1-10,11-20,... up to 100)
        self.challenger_table_button_left_arrow = Button(image=utilities.get_image("left_arrow"),
                                    pos=(int((((self.challenger_table.max_x -
                                    self.challenger_table.top_left_coords[0]) // 2)
                                    + self.challenger_table.top_left_coords[0]) - 150),
                                    self.challenger_table.top_left_coords[1] - 20),
                                    text_input="", font=utilities.get_font(40),
                                    base_color=self.game.config["colours"]["black"], hovering_color=self.game.config["design"]["hovering_colour"])
        self.challenger_table_right_arrow = Button(image=utilities.get_image("right_arrow"),
                                    pos=(int((((self.challenger_table.max_x -
                                    self.challenger_table.top_left_coords[0]) // 2)
                                    + self.challenger_table.top_left_coords[0]) + 150),
                                    self.challenger_table.top_left_coords[1] - 20),
                                    text_input="", font=utilities.get_font(40),
                                    base_color=self.game.config["colours"]["black"], hovering_color=self.game.config["design"]["hovering_colour"])
        self.elements.add(self.back_button_rm)
        self.elements.add(self.challenger_table_button_left_arrow)
        self.elements.add(self.challenger_table_right_arrow)
        self.elements.add(self.challenger_table)
    def draw_ranked_names(self,names):
        xs = [120,280,455,660,900,1113]
        ys = [465,460,420,421,420,415]
        intervals = ["<1000","<2000","<4000","<6000",">= 8000","TOP 100"]
        for name, interval, x, y in zip(names, intervals, xs, ys):
            utilities.draw_text(name, 25, x, y,
                                self.game.display,
                                color=self.game.config["colours"]["aqua"])
            utilities.draw_text(interval, 15, x, y + 20,
                                self.game.display,
                                color=self.game.config["colours"]["aqua"])
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_inputs()
            self.check_events()
            # draw background
            r, g, b = (self.game.config["design"]
                    ["ranked_background_colour"].values())
            self.game.display.fill((r, g, b))
            #draw trophies on the screen
            self.game.display.blit(utilities.get_image("ranks"), (0,400))
            #draw player and his stats
            utilities.draw_text("Your stats", 35, 470, 130, 
                                self.game.display,
                                color=self.game.config["colours"]["aqua"])
            utilities.draw_text(f"ELO:   {self.elo}", 35, 470, 200, 
                                self.game.display,
                                color=self.game.config["colours"]["aqua"])
            utilities.draw_text(self.division, 35, 470, 270,
                            self.game.display,
                            color=self.game.config["colours"]["aqua"])
            utilities.draw_text(self.winrate, 35, 470, 340,
                            self.game.display,
                            color=self.game.config["colours"]["aqua"])
            self.game.display.blit(self.player_preview.image, self.player_preview.rect)
            #draw names
            self.draw_ranked_names(["WOODEN", "IRON", "BRONZE", "SILVER", "GOLD", "CHALLENGER"])
            self.elements.update(self.game.display)
            #TODO: to be changed to real data from database, just for testing now
            self.challenger_table.insert_data(data = self.get_challengers(), display=self.game.display)
            self.challenger_table.create_positions = False
            self.blit_screen()


    def check_events(self):
        for event in pygame.event.get():
            # closing the game with mouse
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.back_button_rm.check_for_input(self.game.mpos):
                    self.run_display = False
                    self.game.curr_menu = self.game.main_menu
    #TODO: all these methods will send request to the server and plot the data
    #that the server returns (now they are just blueprints)
    def get_my_elo(self):
        #TODO: database query for my current elo
        #will return pair (elo,division)
        #TODO: Temporary, to be deleted
        elo = 13000
        division = "CHALLENGER"
        return (elo,division)
    def get_challengers(self):
        #TODO: query top 100 players ordered by elo
        challengers = (["1","Brambora","50%","3570","2","Brambora","50%","3570",
                        "3","Brambora","50%","3570",
                        "4","Brambora","50%","3570",
                        "5","Brambora","50%","3570",
                        "6","Brambora","50%","3570",
                        "7","Brambora","50%","3570",
                        "8","Brambora","50%","3570",
                        "9","Brambora","50%","3570",
                        "10","Brambora","50%","3570"])
        return challengers
    def get_winrate(self):
        #TODO: Calculating winrate (wins/gp)
        #TODO: Temporary, to be deleted
        winrate = "80%"
        return winrate




class MatchHistoryMenu(Menu):
    def __init__(self,game):
        super().__init__(game)
        self.elements = pygame.sprite.Group()
        self.back_button_hm = Button(image=utilities.get_image("back_arrow"), pos=(70, 50),
                            text_input="", font=utilities.get_font(40),
                            base_color=(133, 88, 255), hovering_color=self.game.config["colours"]["aqua"])
        #seperate table for solo games and duo games
        self.match_history_table = Table(self.game.config,header="MATCH HISTORY SOLO", row_size= 60,top_left_coords=(100,80),
                                header_font_size=50 ,cols_sizes=[230,230,70,70,230,230])
        self.elements.add(self.match_history_table)
        self.elements.add(self.back_button_hm)
        self.draw_solo = True
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_inputs()
            self.check_events()
            self.game.display.fill((0,0,0))
            if self.draw_solo:
                utilities.draw_text("Press arrows to change to duo match history",
                            18, 640, 700, self.game.display)
                self.match_history_table.header = "MATCH HISTORY SOLO"
            else:
                utilities.draw_text("Press arrows to change to solo match history",
                            18, 640, 700, self.game.display)
                self.match_history_table.header = "MATCH HISTORY DUO"
            self.elements.update(self.game.display)
            if self.draw_solo:
                #TODO: to be connected to real database data returned by the server
                self.match_history_table.insert_data(data = ["autobus","1220","3","5","1220","autobus",
                                                             "autobus","1220","3","5","1220","autobus",
                                                             "autobus","1220","3","5","1220","autobus",
                                                             "autobus","1220","3","5","1220","autobus",
                                                             "autobus","1220","3","5","1220","autobus",
                                                             "autobus","1220","3","5","1220","autobus",
                                                             "autobus","1220","3","5","1220","autobus",
                                                             "autobus","1220","3","5","1220","autobus",
                                                             "autobus","1220","3","5","1220","autobus",
                                                             "autobus","1220","3","5","1220","autobus",], display=self.game.display)
            else:
                self.match_history_table.insert_data(data = ["auto-brambor","1220-800","8","6","300-1220","auto-vcela",
                                                             "auto-brambor","1220-800","8","6","300-1220","auto-vcela",
                                                             "auto-brambor","1220-800","8","6","300-1220","auto-vcela",
                                                             "auto-brambor","1220-800","8","6","300-1220","auto-vcela",
                                                             "auto-brambor","1220-800","8","6","300-1220","auto-vcela",
                                                             "auto-brambor","1220-800","8","6","300-1220","auto-vcela",
                                                             "auto-brambor","1220-800","8","6","300-1220","auto-vcela",
                                                             "auto-brambor","1220-800","8","6","300-1220","auto-vcela",
                                                             "auto-brambor","1220-800","8","6","300-1220","auto-vcela",
                                                             "auto-brambor","1220-800","8","6","300-1220","auto-vcela",], display=self.game.display)
            self.match_history_table.create_positions = False
            self.blit_screen()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.back_button_hm.check_for_input(self.game.mpos):
                    self.run_display = False
                    self.game.curr_menu = self.game.main_menu
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    self.draw_solo = not self.draw_solo



class CreditsMenu(Menu):
    def __init__(self,game):
        Menu.__init__(self,game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.fill(self.game.config["colours"]["black"])
            utilities.draw_text('Press Backspace to exit',
                            15, 170, 30, self.game.display)
            utilities.draw_text('Credits',
                            20, self.game.WIDTH / 2, self.game.HEIGHT/2 - 20, self.game.display)
            utilities.draw_text('TOM B & MAT S',
                            15, self.game.WIDTH / 2, self.game.HEIGHT/2 + 10, self.game.display)
            self.blit_screen()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.game.BACK_KEY = True
