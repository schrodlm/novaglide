import pygame

class Menu():
    def __init__(self,game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W/2, self.game.DISPLAY_H/2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0,0,20,20)
        self.cursor_offset = - 100


    def draw_cursor(self):
        