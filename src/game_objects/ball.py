"""
Ball Module
--------------

A pygame module for the Ball class, handling the dynamics and graphics of a ball in a game environment.
"""
from typing import Dict

import pygame
from pygame.math import Vector2
# --------------------------BALL-----------------------------------


class Ball(pygame.sprite.Sprite):
    """
    A class representing a ball in a game.

    Attributes
    ----------
    config : Dict
        A configuration of the game.
    server : bool, optional
        A boolean indicating whether the ball is handled by the server. Defaults to False.
    radius : int
        The radius of the ball.
    x : float
        The x-coordinate of the ball's center.
    y : float
        The y-coordinate of the ball's center.
    rect : pygame.Rect
        A rectangle representing the position and size of the ball.
    image : pygame.Surface
        A surface representing the visual appearance of the ball.
    speed : Vector2
        A vector representing the speed of the ball.

    Methods
    -------
    update(borders: pygame.Rect)
        Update the position and speed of the ball.
    set_rect()
        Set the rectangle representation of the ball based on its position and size.
    check_and_handle_rebound(playfield_border: pygame.Rect)
        Check and handle rebound when the ball collides with the playfield borders.
    """
    def __init__(self, config: Dict, server=False):
        pygame.sprite.Sprite.__init__(self)
        self.config = config
        # radius
        self.radius = 20

        # ball should spawn in a middle of a field
        self.x, self.y = self.config["resolution"]["width"] / \
            2, self.config["resolution"]["height"]/2

        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius,
                                2 * self.radius, 2 * self.radius)

        if not server:
            self.image = pygame.Surface(
                (2 * self.radius, 2 * self.radius), pygame.SRCALPHA)  # make it transparent
            self.image = self.image.convert_alpha()
            pygame.draw.circle(self.image, "black",
                               (self.radius, self.radius), self.radius)

        self.speed = Vector2(0, 0)

    def update(self, borders: pygame.Rect):
        """
        Update the position and speed of the ball.

        Parameters
        ----------
        borders : pygame.Rect
            A rectangle representing the borders of the playfield.
        """
        # updating position based on speed
        self.x += self.speed.x
        self.y += self.speed.y
        # slowing down the ball
        self.speed.x /= 1.003
        self.speed.y /= 1.003
        self.checkAndHandleRebound(borders)
        self.setRect()

    def setRect(self):
        """Set the rectangle representation of the ball based on its position and size."""
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius,
                                2 * self.radius, 2 * self.radius)

    def checkAndHandleRebound(self, playfield_border: pygame.Rect):
        """
        Check and handle rebound when the ball collides with the playfield borders.

        Parameters
        ----------
        playfield_border : pygame.Rect
            A rectangle representing the borders of the playfield.
        """
     # Check collision with the left or right border
        if self.x - self.radius <= playfield_border.left:
            self.speed.x = -self.speed.x
            # Adjust position to the border edge
            self.x = playfield_border.left + self.radius
        elif self.x + self.radius >= playfield_border.right:
            self.speed.x = -self.speed.x
            # Adjust position to the border edge
            self.x = playfield_border.right - self.radius

        # Check collision with the top or bottom border
        if self.y - self.radius <= playfield_border.top:
            self.speed.y = -self.speed.y
            # Adjust position to the border edge
            self.y = playfield_border.top + self.radius
        elif self.y + self.radius >= playfield_border.bottom:
            self.speed.y = -self.speed.y
            # Adjust position to the border edge
            self.y = playfield_border.bottom - self.radius


if __name__ == "__main__":
    raise RuntimeError("This module is designed for import only.")
