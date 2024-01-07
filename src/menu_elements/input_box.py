"""Module that stores the input box used in the login screen.

Raises
------
RuntimeError
    When called as the main script and not imported
"""
from typing import Dict
import pygame
pygame.init()
# initializing basic font for the boxes
FONT = pygame.font.Font(None, 32)

# pylint: disable=too-many-instance-attributes
class InputBox:
    """
    A class representing an input box for pygame applications.

    Parameters
    ----------
    x : int
        X-coordinate of the input box.
    y : int
        Y-coordinate of the input box.
    w : int
        Width of the input box.
    h : int
        Height of the input box.
    hide : bool
        Flag indicating whether the text should be hidden/masked.
    config : Dict
        Dictionary containing configuration parameters.
    font : pygame.font.Font, optional
        Font to be used for rendering text, by default default pygame font
        of size 32.
    text : str, optional
        Initial text inside the input box, by default "".

    Attributes
    ----------
    config : Dict
        Dictionary containing configuration parameters.
    rect : pygame.Rect
        Rectangle representing the input box.
    color_inactive : Tuple[int,int,int]
        RGB tuple representing the inactive color of the input box.
    color_active : Tuple[int,int,int]
        RGB tuple representing the active color of the input box.
    color : Tuple[int,int,int]
        Current color of the input box.
    text : str
        Text inside the input box.
    txt_surface : pygame.Surface
        Surface for rendering text.
    active : bool
        Flag indicating whether the input box is active.
    hide : bool
        Flag indicating whether the text should be hidden/masked.
    font : pygame.font.Font
        Font used for rendering text.

    Returns
    -------
    None

    Raises
    ------
    TypeError
        If the types of the constructor do not correspond to the hinted types.
    """

    # pylint: disable=too-many-arguments
    def __init__(self,
                 x: int,
                 y: int,
                 w: int,
                 h: int,
                 hide: bool,
                 config: Dict,
                 font: pygame.font.Font = FONT,
                 text: str = "") -> None:
        for size in (x, y, w, h):
            if not isinstance(size, int):
                raise TypeError("All of x, y, w, h must be integers")
        if not isinstance(hide, bool):
            raise TypeError("Hide has to be True or False")
        if not isinstance(config, dict):
            raise TypeError("Config has to be a dictionary")
        if not isinstance(font, pygame.font.Font):
            raise TypeError("Font has to be pygame.font.Font")
        if not isinstance(text, str):
            raise TypeError("Text has to be passed as a string")

        # accesing configuration
        self.config = config
        # initalizing the rectangle
        self.rect = pygame.Rect(x, y, w, h)
        # loading the colors from config
        r, g, b = self.config["design"]["input_box_inactive_colour"].values()
        self.color_inactive = (r, g, b)
        r, g, b = self.config["design"]["input_box_active_colour"].values()
        self.color_active = (r, g, b)
        # current color
        self.color = self.color_inactive
        self.text = text
        self.font = font
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False
        self.hide = hide

    def handle_event(self, event: pygame.event.Event) -> "InputBox":
        """
        Handle pygame events for the input box.
        Takes care of adding or deleting letters and masking them with stars
        if necessary.

        Parameters
        ----------
        event : pygame.event.Event
            Pygame event to handle.

        Returns
        -------
        InputBox
            The updated InputBox instance.
        """
        if not isinstance(event, pygame.event.Event):
            raise TypeError("Event must be a pygame event")
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = self.color_active if self.active else self.color_inactive

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.text = ""
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
        # Re-render the text with either stars or the text itself.
        if not self.hide:
            self.txt_surface = self.font.render(self.text, True, self.color)
        else:
            stars = "*" * len(self.text)
            self.txt_surface = self.font.render(stars, True, self.color)
        return self

    def update(self) -> "InputBox":
        """
        Update the input box, resizing it if necessary.

        Returns
        -------
        InputBox
            The updated InputBox instance.
        """
        # Resize the box if the text is too long.
        self.rect.w = max(400, self.txt_surface.get_width()+10)
        return self

    def draw(self, screen) -> "InputBox":
        """
        Draw the input box on the screen.

        Parameters
        ----------
        screen
            The pygame screen to draw on.

        Returns
        -------
        InputBox
            The InputBox instance.
        """
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+25))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)
        return self

    def draw_updated(self, screen) -> "InputBox":
        """
        Manage the whole screen update.
        Calls self.update() and self.draw() sequentially.

        Parameters
        ----------
        screen
            The pygame screen to draw on.

        Returns
        -------
        InputBox
            The InputBox instance.

        Raises
        ------
        RuntimeError
            When it fails to do the update.
        """
        # method that manages the whole screen update
        try:
            self.update().draw(screen)
        except:
            raise RuntimeError("Failed to update the input box")
        return self


if __name__ == "__main__":
    raise RuntimeError("This module is designed for import only.")
