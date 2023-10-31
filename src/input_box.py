import pygame
pygame.init()
COLOR_INACTIVE = pygame.Color((138, 178, 255))
COLOR_ACTIVE = pygame.Color((49, 207, 160))
FONT = pygame.font.Font(None, 32)

class InputBox:
    def __init__(self, x, y, w, h, hide, font = FONT, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = font.render(text, True, self.color)
        self.active = False
        self.hide = hide
        self.font = font

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
            
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                if not self.hide:
                    self.txt_surface = self.font.render(self.text, True, self.color)
                else:
                    stars = "*" * len(self.text)
                    self.txt_surface = self.font.render(stars, True, self.color)


    def update(self):
        # Resize the box if the text is too long.
        width = max(400, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+25))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)
    def draw_updated(self, screen):
        #method that manages the whole screen update
        self.update()
        self.draw(screen)
