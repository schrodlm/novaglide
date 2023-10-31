import pygame

WHITE = (255,255,255)
BLACK = (0,0,0)

def get_font(size):
    return pygame.font.Font("./../resources/ETHNOCEN.TTF", size)

def draw_text(text,size,x,y, display, color=WHITE):
    font = get_font(size)
    text_surface = font.render(text,True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x,y)
    display.blit(text_surface, text_rect)
    
def get_image(name: str):
    paths = {"back_arrow":"./../resources/arrow-back.png",
            "background_main":"./../resources/background.jpg",
            "background_ranked":"./../resources/ranked_background.jpg",
            "ranks":"./../resources/ranked_trophies_lowres.jpg",
            "ranks_frames":"./../resources/icon_ranked_borders.jpg"}
    return pygame.image.load(paths.get(name))