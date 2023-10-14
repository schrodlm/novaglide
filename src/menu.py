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
BG = pygame.image.load("background.jpg")


def get_font(size):
    return pygame.font.Font("Lato-Medium.ttf", size)


def log_in_screen():
    SCREEN.fill((50, 0, 0))
    pygame.display.set_caption("Log in")
    running = True

    # log in button
    LOG_IN_BUTTON = Button(image=None, pos=(640, 460),
                           text_input="LOG IN", font=get_font(75), base_color="black", hovering_color="aqua")

    # initializing input boxes for username and password
    USERNAME_BUTTON = InputBox(440, 200, 400, 70, False)
    PASSWORD_BUTTON = InputBox(440, 300, 400, 70, True)
    input_boxes = [USERNAME_BUTTON, PASSWORD_BUTTON]
    clock = pygame.time.Clock()
    while running:
        # get mouse position
        MOUSE_POS = pygame.mouse.get_pos()
        # draw background
        SCREEN.blit(BG, (0, 0))

        # draw log in text
        LOG_IN_TEXT = get_font(45).render(
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
                    print(USERNAME_BUTTON.text)
                    print(PASSWORD_BUTTON.text)
                    main_menu()

            for box in input_boxes:
                box.handle_event(event)

        # draw input boxes on the screen
        for box in input_boxes:
            box.update()
        for box in input_boxes:
            box.draw(SCREEN)

        pygame.display.flip()
        clock.tick(60)


def main_menu():
    running = True
    print("jsem tu")
    while running:
        SCREEN.fill("black")
        SCREEN.blit(BG, (0, 0))
        for event in pygame.event.get():
            # closing the game with mouse
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.flip()

if __name__ == "__main__":
    log_in_screen()
