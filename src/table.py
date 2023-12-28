"""A Table module, provides simple table for the application.
"""
import pygame
import utilities
from typing import Tuple, List
from configuration_mod import Config
class Table(pygame.sprite.Sprite):
    """
    A class representing a table for displaying data in a Pygame application.
    Inherits from pygame.sprite.Sprite.
    Parameters
    ----------
    config : dict
        Configuration settings object of the client.
    header : str, optional
        The header of the table, by default an empty string.
    row_size : int, optional
        The height of each row in pixels, by default 32.
    top_left_coords : tuple, optional
        The coordinates of the top-left corner of the table, by default (640, 50).
    font_size : int, optional
        The font size for regular table content, by default 16.
    header_font_size : int, optional
        The font size for the table header, by default 25.
    n_rows : int, optional
        The number of rows in the table, by default 10.
    cols_sizes : list, optional
        A list containing the width of each column, by default None.

    Attributes
    ----------
    config : dict
        Configuration settings for the table.
    header : str
        The header of the table.
    row_size : int
        The height of each row in pixels.
    top_left_coords : tuple
        The coordinates of the top-left corner of the table.
    font_size : int
        The font size for regular table content.
    header_font_size : int
        The font size for the table header.
    n_cols : int
        The number of columns in the table.
    cols_sizes : list
        A list containing the width of each column.
    n_rows : int
        The number of rows in the table.
    lines_color : str
        The color of the table lines.
    contents_color : str
        The color of the table contents.
    max_x : int
        The maximum x-coordinate of the table.
    max_y : int
        The maximum y-coordinate of the table.
    text_coords_x : set
        A set containing x-coordinates for text rendering.
    text_coords_y : set
        A set containing y-coordinates for text rendering.
    coordinate_pairs : list
        A list containing coordinate pairs for rendering text.
    create_positions : bool
        Flag indicating whether text positions need to be created.

    Methods
    -------
    update(display)
        Updates the table on the display.
    insert_data(data, display)
        Inserts data into the table and renders it on the display.
    """
    def __init__(self, config: Config,header: str = "", row_size: int = 32,
                top_left_coords: Tuple[int,int]= (640,50),font_size: int = 16, 
                header_font_size: int = 25, n_rows: int = 10, 
                cols_sizes: List[int]= None):
        #config, init sprite
        self.config = config
        super().__init__()
        #all table attributes
        self.header = header
        self.row_size = row_size
        self.top_left_coords = top_left_coords
        self.font_size = font_size
        self.header_font_size = header_font_size
        self.n_cols = len(cols_sizes)
        self.cols_sizes = cols_sizes
        self.n_rows = n_rows
        self.lines_color = self.config["design"]["table_lines_colour"]
        self.contents_color = self.config["design"]["table_contents_colour"]
        self.max_x = self.top_left_coords[0] + sum(cols_sizes)
        self.max_y = self.top_left_coords[1] + n_rows * row_size
        #create middle coordiantes where the text is to be put
        self.text_coords_x = set()
        self.text_coords_y = set()
        for row in range(n_rows):
            self.text_coords_y.add(self.top_left_coords[1] + 
                                (self.row_size//2) + row*self.row_size)
        for column in range(self.n_cols + 1):
            if column != 0:
                self.text_coords_x.add((self.top_left_coords[0] + 
                                        sum(self.cols_sizes[:column])) - 
                                       (self.cols_sizes[column - 1])//2)
        self.coordinate_pairs = []
        self.create_positions = True

    def update(self,display):
        """
        Updates the table on the display.

        Parameters
        ----------
        display : pygame.Surface
            The surface on which the table is rendered.
        """
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
        
    def insert_data(self, data, display):
        """
        Inserts data into the table and renders it on the display.

        Parameters
        ----------
        data : list
            The data to be inserted into the table.
        display : pygame.Surface
            The surface on which the table is rendered.
        """
        if self.create_positions:
            self.coordinate_pairs = [(x,y) for y in sorted(self.text_coords_y) for x in sorted(self.text_coords_x)]
        if len(data) <= self.n_rows * self.n_cols:
            for member,coord in zip(data, self.coordinate_pairs):
                utilities.draw_text(member, self.font_size,
                                coord[0], coord[1],
                                display,color=self.config["colours"]["aqua"])

if __name__ == "__main__":
    raise RuntimeError("This module is designed for import only.")
