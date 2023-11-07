import pygame 
import utilities
class Table(pygame.sprite.Sprite):
    def __init__(self, header = "", row_size = 32,
                top_left_coords = (640,50),font_size = 16, header_font_size = 25, n_rows = 10, cols_sizes = [50,350,100,120],
                lines_color = "white",contents_colors = "aqua"):
        pygame.sprite.Sprite.__init__(self)
        self.header = header
        self.row_size = row_size
        self.top_left_coords = top_left_coords
        self.font_size = font_size
        self.header_font_size = header_font_size
        self.n_cols = len(cols_sizes)
        self.cols_sizes = cols_sizes
        self.n_rows = n_rows
        self.lines_color = lines_color
        self.contents_color = contents_colors
        self.max_x = self.top_left_coords[0] + sum(cols_sizes)
        self.max_y = self.top_left_coords[1] + n_rows * row_size
        self.text_coords_x = set()
        self.text_coords_y = set()
        for row in range(n_rows):
            self.text_coords_y.add(self.top_left_coords[1] + (self.row_size//2) + row*self.row_size)
        self.coordinate_pairs = []
        self.create_positions = True
    def update(self,display):
        if display is not None:
            utilities.draw_text(self.header, self.header_font_size,
                                int(((self.max_x - self.top_left_coords[0]) // 2)
                                + self.top_left_coords[0]), self.top_left_coords[1] - 20,
                                display,color="aqua")
            for row in range(self.n_rows + 1):
                pygame.draw.line(display, "white",
                                (self.top_left_coords[0],
                                self.top_left_coords[1] + row * self.row_size),
                                (self.max_x, self.top_left_coords[1] + row * self.row_size))
            for column in range(self.n_cols + 1):
                if column == 0:
                    pygame.draw.line(display, "white",
                                     (self.top_left_coords[0], self.top_left_coords[1]),
                                    (self.top_left_coords[0], self.max_y))
                else:
                    pygame.draw.line(display, "white",
                                    (self.top_left_coords[0] + sum(self.cols_sizes[:column]),
                                    self.top_left_coords[1]),
                                    (self.top_left_coords[0] + sum(self.cols_sizes[:column]),
                                     self.max_y))
                    self.text_coords_x.add((self.top_left_coords[0] + sum(self.cols_sizes[:column])) - (self.cols_sizes[column - 1])//2)
        
    def insert_data(self, data, display):
        if self.create_positions:
            self.coordinate_pairs = [(x,y) for x in sorted(self.text_coords_x) for y in sorted(self.text_coords_y)]
        if len(data) <= self.n_rows * self.n_cols:
            for member,coord in zip(data, self.coordinate_pairs):
                utilities.draw_text(member, self.font_size,
                                coord[0], coord[1],
                                display,color="aqua")
        