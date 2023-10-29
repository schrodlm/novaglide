import pygame
import utilities

class Menu():
    def __init__(self,game):
        self.game = game
        self.mid_w, self.mid_h = self.game.WIDTH/2, self.game.HEIGHT/2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0,0,20,20)
        self.cursor_offset = - 100


    def draw_cursor(self):
        utilities.draw_text('*', 15, self.cursor_rect.x, self.cursor_rect.y, self.game.display)

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
        self.cursor_rect.midtop = (self.startx + self.cursor_offset, self.starty)

    
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(utilities.BLACK)
            utilities.draw_text('Main Menu', 20, self.game.WIDTH / 2, self.game.HEIGHT/2 - 20, self.game.display)
            utilities.draw_text("Start Game", 20, self.startx, self.starty, self.game.display)
            utilities.draw_text("Options", 20, self.optionx, self.optiony, self.game.display)
            utilities.draw_text("Credits", 20, self.creditsx, self.creditsy, self.game.display)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.optionsx + self.cursor_offset, self.optiony)
                self.state = 'Options'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.creditsx + self.cursor_offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.startx + self.cursor_offset, self.starty)
                self.state = 'Start'

        elif self.game.UP_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.creditsx + self.cursor_offset, self.creditsy)
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.startx + self.cursor_offset, self.starty)
                self.state = 'Start'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.optionx + self.cursor_offset, self.optionsy)

    
    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Start':
                self.game.playing = True
            elif self.state == 'Options':
                pass
            elif self.state == 'Credits':
                pass
        self.run_display = False