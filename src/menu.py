from input_box import InputBox
from button import Button
import pygame
import sys
import os
# Initialize menu
pygame.init()
os.chdir(os.path.dirname(os.path.abspath(__file__)))
WIDTH, HEIGHT = 1280, 720
# Set up display
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
BG = pygame.image.load("./../resources/background_new.jpg")
BACK_BUTTON_IMAGE = pygame.image.load("./../resources/arrow-back.png")
user_login = []

def get_font(size):
    return pygame.font.Font("./../resources/ETHNOCEN.TTF", size)


def log_in_screen():
    pygame.display.set_caption("Log in")
    running = True

    # log in button
    LOG_IN_BUTTON = Button(image=None, pos=(640, 460),
                           text_input="LOG IN", font=get_font(75), base_color="black", hovering_color="aqua")

    # initializing input boxes for username and password
    USERNAME_BUTTON = InputBox(x = 440, y = 200, w = 400, h = 70, hide = False,font = get_font(20))
    PASSWORD_BUTTON = InputBox(x = 440, y = 300, w = 400, h = 70, hide = True,font = get_font(20))
    input_boxes = [USERNAME_BUTTON, PASSWORD_BUTTON]
    clock = pygame.time.Clock()

    while running:
        # get mouse position
        MOUSE_POS = pygame.mouse.get_pos()
        # draw background
        SCREEN.blit(BG, (0, 0))

        # draw log in text
        LOG_IN_TEXT = get_font(30).render(
            "Login with your nickname and password", True, "black")
        LOG_IN_RECT = LOG_IN_TEXT.get_rect(center=(640, 150))
        SCREEN.blit(LOG_IN_TEXT, LOG_IN_RECT)

        LOG_IN_BUTTON.changeColor(MOUSE_POS)
        LOG_IN_BUTTON.update(SCREEN)

        for event in pygame.event.get():
            # closing the game with mouse
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if LOG_IN_BUTTON.checkForInput(MOUSE_POS):
                    user_login.append(USERNAME_BUTTON.text)
                    user_login.append(PASSWORD_BUTTON.text)

                    main_menu()

            for box in input_boxes:
                box.handle_event(event)

        # draw input boxes on the screen
        for box in input_boxes:
            box.draw_updated(SCREEN)

        pygame.display.flip()
        clock.tick(60)


def main_menu():
    pygame.display.set_caption("Main menu")

    
    
    PLAY_1V1_BUTTON = Button(image=None, pos=(640, 300),
                             text_input="Play 1v1", font=get_font(40), base_color="black", hovering_color="aqua")
    PLAY_2V2_BUTTON = Button(image=None, pos=(640, 370),
                             text_input="Play 2v2", font=get_font(40), base_color="black", hovering_color="aqua")
    MATCH_HISTORY_BUTTON = Button(image=None, pos=(640, 440),
                             text_input="Match history", font=get_font(40), base_color="black", hovering_color="aqua")
    RANKED_BUTTON = Button(image=None, pos=(640, 510),
                             text_input="Ranked system", font=get_font(40), base_color="black", hovering_color="aqua")
    BACK_BUTTON = Button(image=BACK_BUTTON_IMAGE, pos=(70, 50),
                             text_input="", font=get_font(40), base_color=(133, 88, 255), hovering_color="aqua")    
    SETTINGS_BUTTON = Button(image=None, pos=(640, 580),
                             text_input="Settings", font=get_font(40), base_color="black", hovering_color="aqua")
    
    running = True
    while running:
        SCREEN.fill("black")
        SCREEN.blit(BG, (0, 0))
        MOUSE_POS = pygame.mouse.get_pos()
        
        
        LOGGED_USER_TEXT = get_font(40).render(
            user_login[0], True, ((49, 207, 160)))

        MAIN_MENU_TEXT = get_font(100).render(
            "NOVAGLIDE", True, "black")
        LOG_IN_RECT = MAIN_MENU_TEXT.get_rect(center=(640, 150))
        
        SCREEN.blit(LOGGED_USER_TEXT, (15,15))
        SCREEN.blit(MAIN_MENU_TEXT, LOG_IN_RECT)
        
        #updating buttons of menu
        PLAY_1V1_BUTTON.changeColor(MOUSE_POS)
        PLAY_1V1_BUTTON.update(SCREEN)
        PLAY_2V2_BUTTON.changeColor(MOUSE_POS)
        PLAY_2V2_BUTTON.update(SCREEN)
        MATCH_HISTORY_BUTTON.changeColor(MOUSE_POS)
        MATCH_HISTORY_BUTTON.update(SCREEN)
        RANKED_BUTTON.changeColor(MOUSE_POS)
        RANKED_BUTTON.update(SCREEN)
        SETTINGS_BUTTON.changeColor(MOUSE_POS)
        SETTINGS_BUTTON.update(SCREEN)
        BACK_BUTTON.changeColor(MOUSE_POS)
        BACK_BUTTON.update(SCREEN)


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
                if BACK_BUTTON.checkForInput(MOUSE_POS):
                    log_in_screen()

        pygame.display.flip()


if __name__ == "__main__":
    log_in_screen()
