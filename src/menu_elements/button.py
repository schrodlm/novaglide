"""Module that stores buttons for the menu that change color on mouse hovering.

Raises
------
RuntimeError
    When called as the main script and not imported
"""
from typing import Tuple, Union
import pygame
import utilities

 # pylint: disable=too-many-instance-attributes
class Button(pygame.sprite.Sprite):
    """
    A class representing a button for the menu
    that changes color on mouse hovering.

    Parameters
    ----------
    image : pygame.Surface or None
        The image surface for the button.
        If None, the button will use text only.
    pos : Tuple[int, int]
        The position (x, y) of the button.
    text_input : str
        The text of the button.
    font : pygame.font.Font
        The font used for rendering the text.
    base_color : str or Tuple[int, int, int]
        The base color of the button when not hovered.
        Pygame color string representation or a Tuple of int from 0-255
    hovering_color : str or Tuple[int, int, int]
        The color of the button when hovered.
        Pygame color string representation or a Tuple of int from 0-255

    Attributes
    ----------
    image : pygame.Surface
        The image surface for the button.
    x_pos : int
        The x-coordinate of the button's position.
    y_pos : int
        The y-coordinate of the button's position.
    font : pygame.font.Font
        The font used for rendering the text.
    base_color : str or Tuple[int, int, int]
        The base color of the button when not hovered.
    hovering_color : str or Tuple[int, int, int]
        The color of the button when hovered.
    text_input : str
        The text of the button.
    text : pygame.Surface
        The rendered text surface for the button.
    rect : pygame.Rect
        The rectangular area occupied by the button.
    text_rect : pygame.Rect
        The rectangular area occupied by the text of the button.

    Methods
    -------
    update(screen: pygame.Surface) -> "Button":
        Updates the button on the given Pygame screen.
    check_for_input(position: Tuple[int, int]) -> bool:
        Checks whether the mouse is hovering over the button.
    change_color(position: Tuple[int, int]) -> "Button":
        Changes the color of the button based on mouse hovering.

    Raises
    ------
    TypeError
        If the provided types do not correspond to the hinted types
    ValueError
        If the length of the tuple is different from 2
    OutOfBoundsError
        If the pos exceeds the size of the screen or the colors are not in
        0-255 range
    InvalidColorString
        If the name of the color is not recognized in pygame

    Notes
    -----
    Inherits from pygame.sprite.Sprite.
    """
    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-branches
    def __init__(self, image: Union[pygame.Surface, None],
                 pos: Tuple[int, int],
                 text_input: str,
                 font: pygame.font.Font,
                 base_color: Union[str, Tuple[int, int, int]],
                 hovering_color: Union[str, Tuple[int, int, int]]) -> None:
        # sprite init
        super().__init__()
        # test arguments
        if (not isinstance(image, pygame.Surface)) and (image is not None):
            raise TypeError("Image has to be a pygame.Surface object or None")
        if not isinstance(pos, tuple):
            raise TypeError("Pos has to be a tuple")
        if len(pos) != 2:
            raise ValueError("The tuple must contain exactly two values")

        for coordinate in pos:
            if not isinstance(coordinate, int):
                raise TypeError("All coordinates need to be integers")

        if not isinstance(text_input, str):
            raise TypeError("Text_input needs to be passed as a string")
        if not isinstance(font, pygame.font.Font):
            raise TypeError("Font has to be pygame.font.Font object")
        for color in (base_color, hovering_color):
            if not isinstance(color, (str, tuple)):
                raise TypeError("The colours need to be string or tuple")
            if isinstance(color, tuple):
                if len(color) != 3:
                    raise ValueError(
                        "The tuples for the color parameter must be of length 3")

                # raises OutOfBoundsError
                utilities.check_color_values(r=color[0], g=color[1],
                                             b=color[2])
            else:
                # raises InvalidColorString
                utilities.check_string_color_posibility(color=color)
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen: pygame.Surface) -> "Button":
        """
        Updates the button on the given Pygame screen.

        Parameters
        ----------
        screen : pygame.Surface
            The Pygame surface on which the button is rendered.

        Returns
        -------
        None

        Raises
        ------
        TypeError
            If screen is not pygame.Surface
        """
        if not isinstance(screen, pygame.Surface):
            raise TypeError("Screen needs to be pygame.Surface")

        # blit the button texture or just the text of the button
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)
        return self

    def check_for_input(self, position: Tuple[int, int]) -> bool:
        """
        Checks whether the mouse is hovering over the button.

        Parameters
        ----------
        position : Tuple[int, int]
            The current mouse position.

        Returns
        -------
        bool
            True if the mouse is hovering over the button, False otherwise

        Raises
        ------
        TypeError
            When position is not a tuple or some coordinates in the tuple
            are not integers
        ValueError
            When the length of the tuple is different from 2
        CoordinatesOutOfBoundsError
            When the coordinates are outside the window screen bounds
        """
        if not isinstance(position, tuple):
            raise TypeError("Position has to be a tuple")
        if len(position) != 2:
            raise ValueError("The tuple must contain exactly two values")

        for coordinate in position:
            if not isinstance(coordinate, int):
                raise TypeError("All coordinates must be integers")

        # check whether mouse is hovering over the rectangle of the button
        if (position[0] in range(self.rect.left, self.rect.right) and
                position[1] in range(self.rect.top, self.rect.bottom)):
            return True
        return False

    def change_color(self, position: Tuple[int, int]) -> "Button":
        """
        Changes the color of the button based on mouse hovering.

        Parameters
        ----------
        position : Tuple[int, int]
            The current mouse position.

        Returns
        -------
        Button
            The updated Button instance with the color change.

        Raises
        ------
        TypeError
            When position is not a tuple or some coordinates in the tuple
            are not integers
        ValueError
            When the length of the tuple is different from 2
        CoordinatesOutOfBoundsError
            When the coordinates are outside the window screen bounds
        """
        # the error handling is done by the check_for_input()
        if self.check_for_input(position=position):
            self.text = self.font.render(self.text_input, True,
                                         self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True,
                                         self.base_color)
        return self


if __name__ == "__main__":
    raise RuntimeError("This module is designed for import only.")
