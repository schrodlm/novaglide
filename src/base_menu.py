import pygame
import utilities
from input_box import InputBox
from button import Button
import sys
class Menu():
    def __init__(self,game):
        self.game = game
        self.run_display = True
        #TODO: delete
        self.mid_w, self.mid_h = self.game.WIDTH/2, self.game.HEIGHT/2
        self.cursor_rect = pygame.Rect(0,0,20,20)
        self.cursor_offset = - 100

    def blit_screen(self):
        self.game.screen.blit(self.game.display,(0,0))
        pygame.display.update()
        self.game.reset_keys()

class LogInMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self,game)
        # log in button
        self.log_in_button = Button(image=None, pos=(640, 460),
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
            self.game.Tick()
            self.game.display.fill((0,0,0))
            # draw background
            self.game.display.blit(utilities.get_image("background_main"), (0, 0))
            #draw instructions
            utilities.draw_text("Login with your nickname and password", 30, 640, 150, self.game.display,utilities.BLACK)
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
        self.play_1v1_button = Button(image=None, pos=(640, 300),
                                    text_input="Play 1v1", font=utilities.get_font(40), base_color="black", hovering_color="aqua")
        self.play_2v2_button = Button(image=None, pos=(640, 370),
                                    text_input="Play 2v2", font=utilities.get_font(40), base_color="black", hovering_color="aqua")
        self.match_history_button = Button(image=None, pos=(640, 440),
                                    text_input="Match history", font=utilities.get_font(40), base_color="black", hovering_color="aqua")
        self.ranked_button = Button(image=None, pos=(640, 510),
                                    text_input="Ranked system", font=utilities.get_font(40), base_color="black", hovering_color="aqua")
        self.back_button = Button(image=utilities.get_image("back_arrow"), pos=(70, 100),
                                    text_input="", font=utilities.get_font(40), base_color=(133, 88, 255), hovering_color="aqua")  
        self.settings_button = Button(image=None, pos=(640, 580),
                                    text_input="Settings", font=utilities.get_font(40), base_color="black", hovering_color="aqua")
        self.credits_button = Button(image=None, pos=(640, 650),
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
        self.main_menu_rect = self.main_menu_text.get_rect(center=(640, 150))

    
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            #tick and fill new background
            self.game.Tick()
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
                    self.game.curr_menu = self.game.options_menu

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




class OptionsMenu(Menu):
    def __init__(self,game):
        Menu.__init__(self,game)
        self.state = 'Volume'
        self.volx, self.voly = self.mid_w, self.mid_h + 20
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + 40
        self.cursor_rect.midtop = (self.volx + self.cursor_offset,self.voly)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.check_events()
            self.check_input()
            self.game.display.fill((0,0,0))
            utilities.draw_text('Options', 20, self.game.WIDTH / 2, self.game.HEIGHT/2 - 30, self.game.display)
            utilities.draw_text('Volume', 15, self.volx, self.voly, self.game.display)
            utilities.draw_text('Controls', 15, self.controlsx, self.controlsy, self.game.display)
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        
        elif self.game.UP_KEY or self.game.DOWN_KEY:
            if self.state == 'Volume':
                self.state = 'Controls'
                self.cursor_rect.midtop =( self.controlsx + self.cursor_offset, self.controlsy)
            elif self.state == 'Controls':
                self.state = 'Volume'
                self.cursor_rect.midtop = (self.volx + self.cursor_offset, self.voly)
        elif self.game.START_KEY:
            #TODO: Create a volume menu and controls menu
            pass
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