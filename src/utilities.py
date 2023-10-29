import pygame


WHITE = (255,255,255)
BLACK = (0,0,0)

def get_font(size):
    return pygame.font.Font("./../resources/Lato-Medium.ttf", size)

def draw_text(text,size,x,y, display):
    font = get_font(size)
    text_surface = font.render(text,True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.center = (x,y)
    display.blit(text_surface, text_rect)