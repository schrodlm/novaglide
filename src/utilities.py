import pygame
import json
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
            "ranks_frames":"./../resources/icon_ranked_borders.jpg",
            "left_arrow": "./../resources/left-arrow.png",
            "right_arrow": "./../resources/right_arrow.png"}
    return pygame.image.load(paths.get(name)).convert_alpha()

def get_settings():
    with open("./../settings/settings.json", encoding="UTF-8") as json_file:
        data = json.load(json_file)
    return data

def convert_volume(volume):
    vocab = {0: "0 %", 1 : "10 %", 2 : "20 %", 3 : "30 %", 4 : "40 %",
             5 : "50 %", 6 : "60 %", 7 : "70 %", 8 : "80 %", 9 : "90 %", 10: "100 %"}
    return vocab.get(volume)

def get_map_names(map_value):
    vocab = {False : "DEFAULT"}
    return vocab.get(map_value)
def get_map_preview(path):
    try:
        preview = pygame.image.load(path).convert_alpha()
    except:
        preview = False
    return preview