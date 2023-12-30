import pygame
from menu import Menu
from input_box import InputBox
from button import Button
import utilities
import sys


class EndScreenMenu(Menu):
    def __init__(self, game, winner):
        Menu.__init__(self,game)

        self.buttons = pygame.sprite.Group()
        self.winner = winner
        self.font = pygame.font.Font(None, 36)

        hovering_color = self.game.config["design"]["hovering_colour"]

        # Define buttons
        self.play_again_button = Button(image=None, pos=(self.mid_x, 300),
                                    text_input="Play again", font=utilities.get_font(40),
                                    base_color="black", hovering_color=hovering_color)
        self.main_menu_button = Button(image=None, pos=(self.mid_x, 370),
                                    text_input="Main menu", font=utilities.get_font(40),
                                    base_color="black", hovering_color=hovering_color)
        
        self.buttons.add(self.play_again_button)
        self.buttons.add(self.main_menu_button)

    def display_menu(self):
        self.run_display = True

        while self.run_display:
            #tick and fill new background
            self.game.check_inputs()
            self.game.display.fill((0,0,0))
            self.game.display.blit(utilities.get_image("background_main"), (0, 0))                

            # Display the winner
            winner_text = self.font.render(f"{self.winner}", True, (255, 255, 255))
            self.game.display.blit(winner_text, (100, 100))  # Adjust position as needed

            self.check_events()

            # Draw buttons
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
                if self.play_again_button.check_for_input(self.game.mpos):
                    self.run_display = False
                    self.game.play_match = True

                if self.main_menu_button.check_for_input(self.game.mpos):
                    self.run_display = False
                    self.game.curr_menu = self.game.main_menu
