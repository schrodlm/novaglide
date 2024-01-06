import pygame
from menu.menu import Menu
from menu_elements.input_box import InputBox
from menu_elements.button import Button
import utilities
import sys


class EndScreenMenu(Menu):
    def __init__(self, game, match_stats):
        Menu.__init__(self,game)

        self.buttons = pygame.sprite.Group()
        self.font = utilities.get_font(40)

        hovering_color = self.game.config["design"]["hovering_colour"]

        # Define buttons
        self.play_again_button = Button(image=None, pos=(self.mid_x+300, 600),
                                    text_input="Play again", font=self.font,
                                    base_color="black", hovering_color=hovering_color)
        self.main_menu_button = Button(image=None, pos=(self.mid_x - 300, 600),
                                    text_input="Main menu", font=self.font,
                                    base_color="black", hovering_color=hovering_color)
        
        self.buttons.add(self.play_again_button)
        self.buttons.add(self.main_menu_button)
        self.stats, self.winner = match_stats

    def display_menu(self):
        self.run_display = True
        header_start_y = 150
        first_column_x = 100
        second_column_x = first_column_x + self.game.display.get_width() // 3
        third_column_x = second_column_x + self.game.display.get_width() // 3
        row_spacing = 40
        font_size = 24
        stat_font = pygame.font.Font(None, font_size)

        while self.run_display:
            self.share_status()
            #tick and fill new background
            self.game.check_inputs()
            self.game.display.fill((0,0,0))
            self.game.display.blit(utilities.get_image("background_main"), (0, 0))                

# Display the winner
            winner_text = ""
            if self.winner is None:
                winner_text = self.font.render(f"Tie!", True, (255, 255, 255))
            else:
                winner_text = self.font.render(f"Winner: {self.winner}", True, (255, 255, 255))
            self.game.display.blit(winner_text, (first_column_x, 100))

            # Display headers
            headers = ["Player", "Touches", "Goals"]
            for i, header in enumerate(headers):
                header_text = stat_font.render(header, True, (255, 255, 255))
                x_pos = [first_column_x, second_column_x, third_column_x][i]
                self.game.display.blit(header_text, (x_pos, header_start_y))

            # Display match stats
            y_offset = header_start_y + row_spacing
            for entity, stats in self.stats.items():
                # Player name
                entity_text = stat_font.render(f"{entity}", True, (255, 255, 255))
                self.game.display.blit(entity_text, (first_column_x, y_offset))

                # Touches
                touches_text = stat_font.render(f"{stats['touches']}", True, (255, 255, 255))
                self.game.display.blit(touches_text, (second_column_x, y_offset))

                # Goals
                goals_text = stat_font.render(f"{stats['goals']}", True, (255, 255, 255))
                self.game.display.blit(goals_text, (third_column_x, y_offset))

                y_offset += row_spacing


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
