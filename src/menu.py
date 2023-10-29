from input_box import InputBox
from button import Button
import pygame
import sys
import os
import settings

class Menu():
    
    def __init__(self): 
        pygame.init() # TODO: this will not be there
        os.chdir(os.path.dirname(os.path.abspath(__file__))) # what is this for
        self.background = pygame.image.load("./../resources/background.jpg")
        self.button_image = pygame.image.load("./../resources/buttton_image.png")
        self.user_login = []
        print("Here")

    def get_font(self,size):
        return pygame.font.Font("./../resources/Lato-Medium.ttf", size)


    def log_in_screen(self):
        pygame.display.set_caption("Log in")
        running = True

        # log in button
        LOG_IN_BUTTON = Button(image=None, pos=(640, 460),
                            text_input="LOG IN", font=self.get_font(75), base_color="black", hovering_color="aqua")

        # initializing input boxes for username and password
        USERNAME_BUTTON = InputBox(440, 200, 400, 70, False)
        PASSWORD_BUTTON = InputBox(440, 300, 400, 70, True)
        input_boxes = [USERNAME_BUTTON, PASSWORD_BUTTON]
        clock = pygame.time.Clock()

        while running:
            # get mouse position
            MOUSE_POS = pygame.mouse.get_pos()
            # draw background
            settings.SCREEN.blit(self.background, (0, 0))

            # draw log in text
            LOG_IN_TEXT = self.get_font(45).render(
                "Login with your nickname and password", True, "black")
            LOG_IN_RECT = LOG_IN_TEXT.get_rect(center=(640, 150))
            settings.SCREEN.blit(LOG_IN_TEXT, LOG_IN_RECT)

            LOG_IN_BUTTON.changeColor(MOUSE_POS)
            LOG_IN_BUTTON.update(settings.SCREEN)

            for event in pygame.event.get():
                # closing the game with mouse
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if LOG_IN_BUTTON.checkForInput(MOUSE_POS):
                        self.user_login.append(USERNAME_BUTTON.text)
                        self.user_login.append(PASSWORD_BUTTON.text)

                        self.main_menu()

                for box in input_boxes:
                    box.handle_event(event)

            # draw input boxes on the screen
            for box in input_boxes:
                box.update()
            for box in input_boxes:
                box.draw(settings.SCREEN)

            pygame.display.flip()
            clock.tick(60)


    def main_menu(self):
        pygame.display.set_caption("Main menu")

        running = True
        PLAY_1V1_BUTTON = Button(image=self.button_image, pos=(640, 300),
                                text_input="PLAY 1v1", font=self.get_font(50), base_color="black", hovering_color="aqua")
        PLAY_2V2_BUTTON = Button(image=self.button_image, pos=(640, 450),
                                text_input="PLAY 2v2", font=self.get_font(50), base_color="black", hovering_color="aqua")
        SETTINGS_BUTTON = Button(image=self.button_image, pos=(640, 600),
                                text_input="SETTINGS", font=self.get_font(50), base_color="black", hovering_color="aqua")
        
        while running:
            settings.SCREEN.fill("black")
            settings.SCREEN.blit(self.background, (0, 0))
            MOUSE_POS = pygame.mouse.get_pos()
            LOGGED_USER_TEXT = self.get_font(40).render(
                self.user_login[0], True, "green") 
            LOGGED_USER_RECT = LOGGED_USER_TEXT.get_rect(center=(100, 50))

            MAIN_MENU_TEXT = self.get_font(100).render(
                "Main menu", True, "black")
            LOG_IN_RECT = MAIN_MENU_TEXT.get_rect(center=(640, 150))
            settings.SCREEN.blit(LOGGED_USER_TEXT, LOGGED_USER_RECT)
            settings.SCREEN.blit(MAIN_MENU_TEXT, LOG_IN_RECT)
            PLAY_1V1_BUTTON.changeColor(MOUSE_POS)
            PLAY_1V1_BUTTON.update(settings.SCREEN)
            PLAY_2V2_BUTTON.changeColor(MOUSE_POS)
            PLAY_2V2_BUTTON.update(settings.SCREEN)
            SETTINGS_BUTTON.changeColor(MOUSE_POS)
            SETTINGS_BUTTON.update(settings.SCREEN)

            for event in pygame.event.get():
                # closing the game with mouse
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_1V1_BUTTON.checkForInput(MOUSE_POS):
                        print("1v1 selected")
                    if PLAY_2V2_BUTTON.checkForInput(MOUSE_POS):
                        print("2v2 selected")
                    if SETTINGS_BUTTON.checkForInput(MOUSE_POS):
                        print("Settings selected")

            pygame.display.flip()


if __name__ == "__main__":
    menu = Menu()
    menu.log_in_screen()
