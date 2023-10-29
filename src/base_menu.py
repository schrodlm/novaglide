import pygame
import utilities
from game import Game

class Menu():
    def __init__(self,game: Game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W/2, self.game.DISPLAY_H/2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0,0,20,20)
        self.cursor_offset = - 100


    def draw_cursor(self):
        utilities.draw_text('*', 15, self.cursor_rect.x, self.cursor_rect.y,)

    def blit_screen(self):
        self.game.screen.blit(self.game.display,(0,0))
        pygame.display.update()


class MainMenu(Menu):
    def __init__(self,game):
        Menu.__init__(self,game)
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h + 30
        self.optionx, self.optiony = self.mid_w, self.mid_h + 50
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 70
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.display.fill(utilities.BLACK)
            utilities.draw_text('Main Menu', 20, self.game)

    