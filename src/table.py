import pygame 
import utilities
class Table(pygame.sprite.Sprite):
    def __init__(self, data = None, header = "", row_size = 40,
                column_size = 90, top_left_coords = (1000,50),font_size = 20, n_rows = 10, n_cols = 3,
                lines_color = "white",contents_colors = "aqua"):
        self.header = header
        self.row_size = row_size
        self.column_size = column_size
        self.top_left_coords = top_left_coords
        self.font_size = font_size
        self.n_cols = n_cols
        self.n_rows = n_rows
        self.data = data
        self.lines_color = lines_color
        self.contents_color = contents_colors
        self.max_x = self.top_left_coords[0] + n_cols * column_size
        self.max_y = self.top_left_coords[1] + n_rows * row_size
    def update(self,display):
        if (self.data is not None) and (display is not None):
            utilities.draw_text(self.header, self.font_size, int(((self.max_x - self.top_left_coords[0]) // 2) + self.top_left_coords[0]), self.top_left_coords[1] - 20, display,color="aqua")
            for row in range(self.n_rows + 1):
                pygame.draw.line(display, "white", (self.top_left_coords[0], self.top_left_coords[1] + row * self.row_size),
                                (self.max_x, self.top_left_coords[1] + row * self.row_size))
            for column in range(self.n_cols + 1):
                pygame.draw.line(display, "white", (self.top_left_coords[0] + column * self.column_size, self.top_left_coords[1]),
                                (self.top_left_coords[0] + column * self.column_size, self.max_y))
    
                
            
    
        

