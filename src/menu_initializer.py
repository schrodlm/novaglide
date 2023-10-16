#imports
from input_box import InputBox
from button import Button
import pygame
import sys
import os

# main class with all features that the menu has
class GameInitializer:
    """initalizing of the buttons, input boxesx etc.
    Will be performed directly in the methods for each coresponding screen 
    """
    def __init__(self, width = 1280, height = 720):
        pygame.init()
        self.SCREEN = pygame.display.set_mode((width, height))
        self.user_credentials = []
        self.ranking_initialized = False
        self.main_menu_initialized = False
        self.log_in_initialized = False
    #font loader
    @staticmethod    
    def get_font(size):
        return pygame.font.Font("./../resources/ETHNOCEN.TTF", size)
    #loading images
    def load_resources(self):
        self.BG = pygame.image.load("./../resources/background_new.jpg")
        self.BG_RANKED = pygame.image.load("./../resources/ranked_background.jpg")
        self.BACK_BUTTON_IMAGE = pygame.image.load("./../resources/arrow-back.png")
        self.TROPHIES = pygame.image.load("./../resources/ranked_trophies_lowres.jpg")
    #initializing ranking objects
    def init_ranking(self):
        self.ranking_initialized = True
        pygame.display.set_caption("Ranking system")  
        self.clock = pygame.time.Clock()
        self.BACK_BUTTON = Button(image=self.BACK_BUTTON_IMAGE, pos=(70, 50),
                             text_input="", font=self.get_font(40), base_color=(133, 88, 255), hovering_color="aqua")      
        self.running = True
    def run_ranking(self):
        if self.ranking_initialized:
            while self.running:
                #get mouse position
                MOUSE_POS = pygame.mouse.get_pos()
                # draw background
                self.SCREEN.fill((30, 15, 72))
                #draw trophies on the screen
                self.TROPHIES.get_rect()
                self.SCREEN.blit(self.TROPHIES, (0,400))
                #draw button on the screen
                self.BACK_BUTTON.change_color(MOUSE_POS)
                self.BACK_BUTTON.update(self.SCREEN)

                for event in pygame.event.get():
                    # closing the game with mouse
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.BACK_BUTTON.check_for_input(MOUSE_POS):
                            self.init_main_menu()
                            self.run_main_menu()
                        
                pygame.display.flip()
                self.clock.tick(60)
            
    def init_log_in(self):
        self.log_in_initialized = True
        pygame.display.set_caption("Log in")
        self.running = True
        # log in button
        self.LOG_IN_BUTTON = Button(image=None, pos=(640, 460),
                                text_input="LOG IN", font=self.get_font(75), base_color="black", hovering_color="aqua")

        # initializing input boxes for username and password
        self.USERNAME_BUTTON = InputBox(x = 440, y = 200, w = 400, h = 70, hide = False,font = self.get_font(20))
        self.PASSWORD_BUTTON = InputBox(x = 440, y = 300, w = 400, h = 70, hide = True,font = self.get_font(20))
        self.input_boxes = [self.USERNAME_BUTTON, self.PASSWORD_BUTTON]
        self.clock = pygame.time.Clock()
    
    def run_log_in(self):
        if self.log_in_initialized:
            while self.running:
                # get mouse position
                MOUSE_POS = pygame.mouse.get_pos()
                # draw background
                self.SCREEN.blit(self.BG, (0, 0))

                # draw log in text
                LOG_IN_TEXT = self.get_font(30).render(
                    "Login with your nickname and password", True, "black")
                LOG_IN_RECT = LOG_IN_TEXT.get_rect(center=(640, 150))
                self.SCREEN.blit(LOG_IN_TEXT, LOG_IN_RECT)

                self.LOG_IN_BUTTON.change_color(MOUSE_POS)
                self.LOG_IN_BUTTON.update(self.SCREEN)

                for event in pygame.event.get():
                    # closing the game with mouse
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.LOG_IN_BUTTON.check_for_input(MOUSE_POS):
                            self.user_credentials.append(self.USERNAME_BUTTON.text)
                            self.user_credentials.append(self.PASSWORD_BUTTON.text)
                            self.init_main_menu()
                            self.run_main_menu()

                    for box in self.input_boxes:
                        box.handle_event(event)

                # draw input boxes on the screen
                for box in self.input_boxes:
                    box.draw_updated(self.SCREEN)

                pygame.display.flip()
                self.clock.tick(60)      
    def init_main_menu(self):
        self.main_menu_initialized = True
        pygame.display.set_caption("Main menu")

        self.PLAY_1V1_BUTTON = Button(image=None, pos=(640, 300),
                                    text_input="Play 1v1", font=self.get_font(40), base_color="black", hovering_color="aqua")
        self.PLAY_2V2_BUTTON = Button(image=None, pos=(640, 370),
                                    text_input="Play 2v2", font=self.get_font(40), base_color="black", hovering_color="aqua")
        self.MATCH_HISTORY_BUTTON = Button(image=None, pos=(640, 440),
                                    text_input="Match history", font=self.get_font(40), base_color="black", hovering_color="aqua")
        self.RANKED_BUTTON = Button(image=None, pos=(640, 510),
                                    text_input="Ranked system", font=self.get_font(40), base_color="black", hovering_color="aqua")
        self.BACK_BUTTON = Button(image=self.BACK_BUTTON_IMAGE, pos=(70, 100),
                                    text_input="", font=self.get_font(40), base_color=(133, 88, 255), hovering_color="aqua")    
        self.SETTINGS_BUTTON = Button(image=None, pos=(640, 580),
                                    text_input="Settings", font=self.get_font(40), base_color="black", hovering_color="aqua")

        self.running = True
    #updating all buttons at once
    def update_menu_buttons(self, buttons = [], mouse_pos = None):
        for button in buttons:
            button.change_color(mouse_pos)
            button.update(self.SCREEN)
            
    def run_main_menu(self):
        if self.main_menu_initialized:
            while self.running:
                self.SCREEN.fill("black")
                self.SCREEN.blit(self.BG, (0, 0))
                MOUSE_POS = pygame.mouse.get_pos()
                

                LOGGED_USER_TEXT = self.get_font(40).render(
                    self.user_credentials[0], True, ((49, 207, 160)))

                MAIN_MENU_TEXT = self.get_font(100).render(
                    "NOVAGLIDE", True, "black")
                LOG_IN_RECT = MAIN_MENU_TEXT.get_rect(center=(640, 150))
                
                self.SCREEN.blit(LOGGED_USER_TEXT, (15,15))
                self.SCREEN.blit(MAIN_MENU_TEXT, LOG_IN_RECT)

                #update all buttons
                self.update_menu_buttons(buttons = [self.PLAY_1V1_BUTTON, self.PLAY_2V2_BUTTON, 
                    self.MATCH_HISTORY_BUTTON, self.RANKED_BUTTON,
                    self.BACK_BUTTON, self.SETTINGS_BUTTON], mouse_pos= MOUSE_POS)
                
                for event in pygame.event.get():
                    # closing the game with mouse
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.PLAY_1V1_BUTTON.check_for_input(MOUSE_POS):
                            print("1v1 selected")
                        if self.PLAY_2V2_BUTTON.check_for_input(MOUSE_POS):
                            print("2v2 selected")
                        if self.SETTINGS_BUTTON.check_for_input(MOUSE_POS):
                            print("Settings selected")
                        if self.BACK_BUTTON.check_for_input(MOUSE_POS):
                            self.init_log_in()
                            self.run_log_in()
                        if self.RANKED_BUTTON.check_for_input(MOUSE_POS):
                            self.init_ranking()
                            self.run_ranking()

                pygame.display.flip()
    def start_app(self):
        self.load_resources
        self.init_log_in()
        self.run_log_in()