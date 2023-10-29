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

    def get_font(self,size):
        return pygame.font.Font("./../resources/Lato-Medium.ttf", size)


    def log_in_screen(self):
        pygame.display.set_caption("Log in")
        running = True

        # log in button
        log_in_btn = Button(image=None, pos=(640, 460),
                            text_input="LOG IN", font=self.get_font(75), base_color="black", hovering_color="aqua")

        # initializing input boxes for username and password
        username_btn = InputBox(440, 200, 400, 70, False)
        password_btn = InputBox(440, 300, 400, 70, True)
        input_boxes = [username_btn, password_btn]
        clock = pygame.time.Clock()

        while running:
            # get mouse position
            mouse_pos = pygame.mouse.get_pos()
            # draw background
            settings.SCREEN.blit(self.background, (0, 0))

            # draw log in text
            login_txt = self.get_font(45).render(
                "Login with your nickname and password", True, "black")
            login_rect = login_txt.get_rect(center=(640, 150))
            settings.SCREEN.blit(login_txt, login_rect)

            log_in_btn.changeColor(mouse_pos)
            log_in_btn.update(settings.SCREEN)

            for event in pygame.event.get():
                # closing the game with mouse
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if log_in_btn.checkForInput(mouse_pos):
                        self.user_login.append(username_btn.text)
                        self.user_login.append(password_btn.text)

                        self.loop()

                for box in input_boxes:
                    box.handle_event(event)

            # draw input boxes on the screen
            for box in input_boxes:
                box.update()
            for box in input_boxes:
                box.draw(settings.SCREEN)

            pygame.display.flip()
            clock.tick(60)


    def loop(self):
        pygame.display.set_caption("Main menu")

        running = True
        one_vs_one_btn = Button(image=self.button_image, pos=(640, 300),
                                text_input="PLAY 1v1", font=self.get_font(50), base_color="black", hovering_color="aqua")
        two_vs_two_btn = Button(image=self.button_image, pos=(640, 450),
                                text_input="PLAY 2v2", font=self.get_font(50), base_color="black", hovering_color="aqua")
        settings_btn = Button(image=self.button_image, pos=(640, 600),
                                text_input="SETTINGS", font=self.get_font(50), base_color="black", hovering_color="aqua")
        
        while running:
            settings.SCREEN.fill("black")
            settings.SCREEN.blit(self.background, (0, 0))
            mouse_pos = pygame.mouse.get_pos()
            logged_user_txt = self.get_font(40).render(
                self.user_login[0], True, "green") 
            logged_usr_rect = logged_user_txt.get_rect(center=(100, 50))

            main_menu_txt = self.get_font(100).render(
                "Main menu", True, "black")
            login_rect = main_menu_txt.get_rect(center=(640, 150))
            settings.SCREEN.blit(logged_user_txt, logged_usr_rect)
            settings.SCREEN.blit(main_menu_txt, login_rect)
            one_vs_one_btn.changeColor(mouse_pos)
            one_vs_one_btn.update(settings.SCREEN)
            two_vs_two_btn.changeColor(mouse_pos)
            two_vs_two_btn.update(settings.SCREEN)
            settings_btn.changeColor(mouse_pos)
            settings_btn.update(settings.SCREEN)

            for event in pygame.event.get():
                # closing the game with mouse
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if one_vs_one_btn.checkForInput(mouse_pos):
                        print("1v1 selected")
                    if two_vs_two_btn.checkForInput(mouse_pos):
                        print("2v2 selected")
                    if settings_btn.checkForInput(mouse_pos):
                        print("Settings selected")

            pygame.display.flip()


if __name__ == "__main__":
    menu = Menu()
    menu.log_in_screen()
