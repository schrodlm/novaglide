import pygame
import utilities
from input_box import InputBox
from button import Button
import sys
from player import Player
class Menu():
    def __init__(self,game):
        self.game = game
        self.run_display = True
        self.mid_x = self.game.WIDTH // 2
        self.mid_y = self.game.HEIGHT //2

    def blit_screen(self):
        self.game.screen.blit(self.game.display,(0,0))
        pygame.display.update()
        self.game.reset_keys()

class LogInMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self,game)
        # log in button
        self.log_in_button = Button(image=None, pos=(self.mid_x, 460),
                text_input="LOG IN", font=utilities.get_font(75), base_color="black", hovering_color="aqua")
        # initializing input boxes for username and password
        self.username_input = InputBox(x = 440, y = 200, w = 400, h = 70, hide = False)
        self.password_input = InputBox(x = 440, y = 300, w = 400, h = 70, hide = True)
        # group same objects
        self.input_boxes = [self.username_input, self.password_input]
        
    def display_menu(self):
        self.username_input.text = ""
        self.password_input.text = ""
        self.run_display = True
        while self.run_display:
            self.game.Check_inputs()
            self.game.display.fill((0,0,0))
            # draw background
            self.game.display.blit(utilities.get_image("background_main"), (0, 0))
            #draw instructions
            utilities.draw_text("Login with your nickname and password", 30, self.mid_x, 150, self.game.display,utilities.BLACK)
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
                    self.run_display = False
                    self.game.curr_menu = self.game.main_menu
                    self.game.user_credentials["name"] = self.username_input.text
                    self.game.user_credentials["password"] = self.password_input.text
            for box in self.input_boxes:
                box.handle_event(event)
        for box in self.input_boxes:
            box.draw_updated(self.game.display)

class MainMenu(Menu):
    def __init__(self,game):
        Menu.__init__(self,game)
        self.buttons = pygame.sprite.Group()
        self.play_1v1_button = Button(image=None, pos=(self.mid_x, 300),
                                    text_input="Play 1v1", font=utilities.get_font(40), base_color="black", hovering_color="aqua")
        self.play_2v2_button = Button(image=None, pos=(self.mid_x, 370),
                                    text_input="Play 2v2", font=utilities.get_font(40), base_color="black", hovering_color="aqua")
        self.match_history_button = Button(image=None, pos=(self.mid_x, 440),
                                    text_input="Match history", font=utilities.get_font(40), base_color="black", hovering_color="aqua")
        self.ranked_button = Button(image=None, pos=(self.mid_x, 510),
                                    text_input="Ranked system", font=utilities.get_font(40), base_color="black", hovering_color="aqua")
        self.back_button = Button(image=utilities.get_image("back_arrow"), pos=(70, 100),
                                    text_input="", font=utilities.get_font(40), base_color=(133, 88, 255), hovering_color="aqua")  
        self.settings_button = Button(image=None, pos=(self.mid_x, 580),
                                    text_input="Settings", font=utilities.get_font(40), base_color="black", hovering_color="aqua")
        self.credits_button = Button(image=None, pos=(self.mid_x, 650),
                                    text_input="Credits", font=utilities.get_font(40), base_color="black", hovering_color="aqua")
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
                    self.game.user_credentials.get("name"), True, ((49, 207, 160)))
        self.logged_user_rect = self.logged_user_text.get_rect(topleft=(15,15))

        self.main_menu_text = utilities.get_font(100).render(
                    "NOVAGLIDE", True, "black")
        self.main_menu_rect = self.main_menu_text.get_rect(center=(self.mid_x, 150))

    
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            #tick and fill new background
            self.game.Check_inputs()
            self.game.display.fill((0,0,0))
            self.game.display.blit(utilities.get_image("background_main"), (0, 0))
            
            #need to regenerate every time because the name is dynamically changing
            self.logged_user_text = utilities.get_font(40).render(
            self.game.user_credentials.get("name"), True, ((49, 207, 160)))
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
                    self.game.playing = True
                    self.run_display = False
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
                    #TODO: finish 
                    print("ranked selected")
                if self.credits_button.check_for_input(self.game.mpos):
                    self.run_display = False
                    self.game.curr_menu = self.game.credits_menu




class SettingsMenu(Menu):
    def __init__(self,game):
        Menu.__init__(self,game)
        self.loaded_settings = utilities.get_settings()
        self.music = self.loaded_settings["Music"]
        self.volume = self.loaded_settings["Volume"]
        self.next_volume = self.volume
        
        self.map = utilities.get_map_preview(self.loaded_settings["Map"])
        self.profile_picture = self.loaded_settings["ProfilePicture"]
        self.controls = self.loaded_settings["Controls"]
        
        self.default_player = Player(200,self.mid_y,100)
        
        self.buttons = pygame.sprite.Group()
        self.volume_button_left_arrow = Button(image=utilities.get_image("left_arrow"), pos=(self.mid_x - 100, 170),
                                    text_input="", font=utilities.get_font(40), base_color="black", hovering_color="aqua")
        self.volume_button_right_arrow = Button(image=utilities.get_image("right_arrow"), pos=(self.mid_x + 100, 170),
                                    text_input="", font=utilities.get_font(40), base_color="black", hovering_color="aqua")
        self.change_profile_picture_button = Button(image=None, pos=(self.mid_x, 170),
                                    text_input="Change profile picture", font=utilities.get_font(40), base_color="black", hovering_color="aqua")
        
        #Grouping buttons
        self.buttons.add(self.volume_button_left_arrow)
        self.buttons.add(self.volume_button_right_arrow)
        self.buttons.add(self.change_profile_picture_button)





    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.Check_inputs()
            self.check_events()
            self.game.display.fill((0,0,0))
            self.game.display.blit(utilities.get_image("background_main"), (0, 0))
            #Music settings
            utilities.draw_text("Music", 40, self.mid_x, 100, self.game.display,utilities.BLACK)
            
            if self.music:
                utilities.draw_text("ON", 30, self.mid_x, 170, self.game.display)
            else:
                utilities.draw_text("OFF", 30, self.mid_x, 170, self.game.display)
            #Volume settings    
            utilities.draw_text("Volume", 40, self.mid_x, 230, self.game.display,utilities.BLACK)
            utilities.draw_text(utilities.convert_volume(self.volume), 30, self.mid_x, 300, self.game.display)
            #Map choice
            utilities.draw_text("Map", 40, self.mid_x, 370, self.game.display,utilities.BLACK)
            
            utilities.draw_text(utilities.get_map_names(self.map), 30, self.mid_x, 440, self.game.display)
            
            #bliting player skin
            try:
                raise Exception
            except:
                self.game.display.blit(self.default_player.image, self.default_player.rect)
            
            utilities.draw_text("Controls", 40, self.mid_x, 510, self.game.display,utilities.BLACK)
            if self.controls == "wsad":
                utilities.draw_text("W S A D", 30, self.mid_x, 580, self.game.display)
            if self.controls == "arrows":
                utilities.draw_text("Arrows", 30, self.mid_x, 580, self.game.display)
                
            #update all buttons
            for button in self.buttons:
                button.change_color(self.game.mpos)
            #update all buttons
            self.buttons.update(self.game.display)
            self.blit_screen()


    def check_events(self):
        #TODO: to be changed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.game.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.game.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.game.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.game.UP_KEY = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.volume_button_right_arrow.check_for_input(self.game.mpos):
                    self.next_volume = self.volume + 1
                    print(self.next_volume)
                    if self.next_volume <= 10 and self.next_volume >= 0:
                        self.volume = self.next_volume
                        print(self.volume)
                if self.volume_button_left_arrow.check_for_input(self.game.mpos):
                    self.next_volume = self.volume - 1
                    print(self.next_volume)
                    if self.next_volume <= 10 and self.next_volume >= 0:
                        self.volume = self.next_volume
                        print(self.volume)
                    

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
            self.game.display.fill(utilities.BLACK)
            utilities.draw_text('Press Backspace to exit', 15, 170, 30, self.game.display)
            utilities.draw_text('Credits', 20, self.game.WIDTH / 2, self.game.HEIGHT/2 - 20, self.game.display)
            utilities.draw_text('TOM B & MAT S', 15, self.game.WIDTH / 2, self.game.HEIGHT/2 + 10, self.game.display)
            self.blit_screen()
            
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.game.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.game.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.game.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.game.UP_KEY = True