import pygame
from pygame import Vector2
import utilities
from typing import Dict, Tuple, List, Union
# --------------------------PLAYER-----------------------------------


class Player(pygame.sprite.Sprite):
    """
    A class representing a player in the game.

    Attributes
    ----------
    name : str
        The name of the player.
    x : int
        The x-coordinate of the player's center.
    y : int
        The y-coordinate of the player's center.
    config : Dict
        A dictionary containing configuration settings.
    elo : int
        The Elo rating of the player.
    radius : int
        The radius of the player.
    color : str
        The color of the player.
    server : bool
        A boolean indicating whether the player is controlled by the server.
    game_settings : Dict
        Dictionary containing game settings.
    coord_initial : Vector2
        The initial coordinates of the player.
    hook_coords : Vector2
        The coordinates of the player's hook.
    hook_initial : Vector2
        The initial coordinates of the hook.
    coords_current : Vector2
        The current coordinates of the player.
    dash_started : Vector2
        The starting coordinates of a dash.
    dash_coords : Vector2
        The current coordinates during a dash.
    dash_destination : Vector2
        The destination coordinates of a dash.
    hook_cooldown_started : float
        The time when the hook cooldown started.
    hook_on_cooldown : bool
        A boolean indicating whether the hook is on cooldown.
    dash_cooldown_started : float
        The time when the dash cooldown started.
    dash_on_cooldown : bool
        A boolean indicating whether the dash is on cooldown.
    dashed_already : int
        The number of dashes performed.
    dash_length : int
        The maximum length of a dash.
    hooking : bool
        A boolean indicating whether the player is in the process of hooking.
    end_hook : bool
        A boolean indicating whether the hook has reached the border.
    pull : bool
        A boolean indicating whether the player is being pulled.
    dashing : bool
        A boolean indicating whether the player is in the process of dashing.
    rect : pygame.Rect
        A rectangle representing the position and size of the player.
    image : pygame.Surface
        A surface representing the visual appearance of the player.

    Methods
    -------
    update(dt: float, display: Union[pygame.Surface, None], mouse_pos: Tuple[int, int], time: float, keys: List, controls: str) -> None
        Update the player's state based on input and game logic.
    move(dx: Union[int, float], dy: Union[int, float]) -> None
        Move the player by a specified amount.
    set_rect() -> None
        Set the rectangle representation of the player based on its position and size.
    hook(dt: float, display: Union[pygame.Surface, None]) -> None
        Perform the hook action.
    pull_player(dt: float) -> None
        Pull the player towards the hook.
    intersect_vector_rectangle(point_a: Vector2, point_b: Vector2) -> Vector2
        Find the intersection point between a vector and the game border.
    invariant() -> bool
        Ensure that the player stays inside the game borders.
    hook_invariant() -> bool
        Determine whether the hook is within the game borders.
    dash(dt: float) -> None
        Perform the dash action.
    check_cooldowns(time: float) -> None
        Check and update cooldowns for hook and dash actions.
        
    Raises
    ------
    TypeError   
        If the parameters are of incorrect type.
    """
    def __init__(self, name: str, x: int, y: int, config: Dict, elo: int = 0, 
                radius: int = 40, color: str ="red", server: bool = False):
        pygame.sprite.Sprite.__init__(self)
        
        if not isinstance(name, str) or not isinstance(config, dict):
            raise TypeError("Incorrect type of the parameters.")
        if not isinstance(color, str) or not isinstance(server, bool):
            raise TypeError("Incorrect type of the parameters.")
        for integer in (x, y, elo, radius):
            if not isinstance(integer, int):
                raise TypeError("Incorrect type of the parameters.")
        self.game_settings = utilities.get_settings()
        self.config = config
        # width and height
        self.radius = radius
        self.x, self.y = x, y
        self.coord_initial = Vector2(x, y)
        self.hook_coords = Vector2(x, y)
        self.hook_initial = Vector2(x, y)
        self.coords_current = Vector2(x, y)
        self.dash_started = Vector2(x, y)
        self.dash_coords = Vector2(x, y)
        self.dash_destination = Vector2(x, y)
        self.hook_cooldown_started = 0
        self.hook_on_cooldown = False
        self.dash_cooldown_started = 0
        self.dash_on_cooldown = False

        self.dashed_already = 0
        self.dash_length = 8
        self.hooking = False
        self.end_hook = False
        self.pull = False
        self.dashing = False

        self.elo = elo

        self.rect = pygame.Rect(x - self.radius, y - self.radius,
                                2 * self.radius, 2 * self.radius)

        if not server:
            self.image = pygame.Surface(
                (2 * self.radius, 2 * self.radius), pygame.SRCALPHA)  # make it transparent
            self.image = self.image.convert_alpha()

            pygame.draw.circle(self.image, color,
                               (self.radius, self.radius), self.radius)

        self.name = name

    def update(self, dt: float, display: Union[pygame.Surface, None], mouse_pos: Tuple[int, int], time: float, keys: pygame.key.ScancodeWrapper, controls: str):
        """
        Update the player's state based on input and game logic.

        Parameters
        ----------
        dt : float
            The time step.
        display : pygame.Surface or None
            The display surface. None on the server side.
        mouse_pos : Tuple[int, int]
            The mouse coordinates.
        time : float
            The current time.
        keys : List
            The keys pressed.
        controls : str
            The control scheme ("wsad" or "arrows").
        
        Raises
        ------
        TypeError   
            If the parameters are of incorrect type.
        """
        if not isinstance(dt, float):
            raise TypeError("Incorrect type of the parameters.")
        if not isinstance(mouse_pos, Tuple) or not isinstance(mouse_pos[0], int) or not isinstance(mouse_pos[1], int):
            raise TypeError("Incorrect type of the parameters.")
        if not isinstance(time, float) or not isinstance(keys, pygame.key.ScancodeWrapper) or not isinstance(controls, str):
            raise TypeError("Incorrect type of the parameters.")
        if controls not in ["wsad","arrows"]:
            raise TypeError("Controls must be wsad or arrows")
        # display can be None on the server side
        if controls == "wsad":
            if keys[pygame.K_w] and not self.pull:
                self.move(0, -500*dt)
            if keys[pygame.K_s] and not self.pull:
                self.move(0, 500*dt)
            if keys[pygame.K_a] and not self.pull:
                self.move(-500*dt, 0)
            if keys[pygame.K_d] and not self.pull:
                self.move(500*dt, 0)
        if controls == "arrows":
            if keys[pygame.K_UP] and not self.pull:
                self.move(0, -500*dt)
            if keys[pygame.K_DOWN] and not self.pull:
                self.move(0, 500*dt)
            if keys[pygame.K_LEFT] and not self.pull:
                self.move(-500*dt, 0)
            if keys[pygame.K_RIGHT] and not self.pull:
                self.move(500*dt, 0)

        if (keys[pygame.K_SPACE] and self.hooking is False
                and not self.pull and not self.hook_on_cooldown):
            # runs in the first tick after presing backspace
            self.hook_cooldown_started = time
            self.hook_on_cooldown = True
            self.hooking = True
            self.hook_coords.x = self.x
            self.hook_coords.y = self.y
            self.hook_initial.x = mouse_pos[0]
            self.hook_initial.y = mouse_pos[1]
            hook_wall = self.intersect_vector_rectangle(self.hook_coords,
                                                        self.hook_initial)
            self.hook_initial.x = hook_wall.x
            self.hook_initial.y = hook_wall.y
            self.hook(dt, display)
        if self.end_hook:
            # runs after it reaches boarder
            self.end_hook = False
            self.hooking = False
        if self.hooking:
            # runs after casting until reaching border
            self.hook(dt, display)
        if self.pull:
            self.pull_player(dt)
        if keys[pygame.K_LSHIFT] and not self.dash_on_cooldown:
            self.dash_cooldown_started = time
            self.dash_destination.x = mouse_pos[0]
            self.dash_destination.y = mouse_pos[1]
            self.dash(dt)
        self.check_cooldowns(time)

    def move(self, dx: Union[int, float], dy: Union[int, float]):
        """
        Move the player by a specified amount.

        Parameters
        ----------
        dx : Union[int, float]
            The change in the x-coordinate.
        dy : Union[int, float]
            The change in the y-coordinate.
            
        Raises
        ------
        TypeError 
            If the parameters are of incorrect type.
        
        """
        for d in (dx,dy):
            if not isinstance(d,(int, float)):
                raise TypeError("Dx and dy must be numbers.")
        self.x += dx
        self.y += dy
        if self.x - self.radius < 0:
            self.x = 5 + self.radius
        elif self.x + self.radius > self.config["resolution"]["width"]:
            self.x = self.config["resolution"]["width"] - self.radius - 5
        if self.y - self.radius < 0:
            self.y = 5 + self.radius
        elif self.y + self.radius > self.config["resolution"]["height"]:
            self.y = self.config["resolution"]["height"] - self.radius - 5
        self.setRect()

    def setRect(self):
        """
        Set the rectangle representation of the player based on its position and size.
        """
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius,
                                2 * self.radius, 2 * self.radius)

    def hook(self, dt: float, display: Union[pygame.Surface, None]):
        """
        Perform the hook action.

        Parameters
        ----------
        dt : float
            The time step.
        display : pygame.Surface or None
            The display surface. None on the server side.
        
        """
        if not isinstance(dt, float):
            raise TypeError("Dt must be a float")
        if display is not None and not isinstance(display, pygame.Surface):
            raise TypeError("Display must be pyganme.Surface or None.")
        direction = self.hook_initial - self.hook_coords
        if display is None:
            self.hook_coords += 1200*dt*(direction.normalize())
        if not self.hook_invarint():
            # begin pulling after geting out of boundary
            self.end_hook = True
            self.pull = True
            self.coords_current.x = self.x
            self.coords_current.y = self.y
        else:
            if display is not None:
                pygame.draw.line(display, "orange4", (self.x, self.y),
                                 (self.hook_coords.x, self.hook_coords.y), 3)

    def pull_player(self, dt: float):
        """
        Pull the player towards the hook.

        Parameters
        ----------
        dt : float
            The time step.
        """
        if not isinstance(dt, float):
            raise TypeError("Dt must be a float")
        direction = self.hook_initial - self.coords_current
        self.coords_current += 1200*dt*(direction.normalize())
        self.x = self.coords_current.x
        self.y = self.coords_current.y
        # make a seperate method
        if not self.invariant():
            self.pull = False
        self.setRect()

    def intersect_vector_rectangle(self, point_a: Vector2, point_b: Vector2):
        """
        Find the intersection point between a vector and the game border.

        Parameters
        ----------
        point_a : Vector2
            The starting point of the vector.
        point_b : Vector2
            The ending point of the vector.

        Returns
        -------
        Vector2
            The intersection point.
        """
        if not isinstance(point_a, Vector2) or not isinstance(point_b, Vector2):
            raise TypeError("Both points must be a Vector2.")
        # this method finds the point where vector between two points
        # intersects with the border
        t_1 = (-point_a.x)/(point_b.x - point_a.x)
        t_2 = (1280 - point_a.x)/(point_b.x - point_a.x)
        t_3 = (-point_a.y)/(point_b.y - point_a.y)
        t_4 = (720 - point_a.y)/(point_b.y - point_a.y)
        positive_solution = []
        for t in (t_1, t_2, t_3, t_4):
            if t > 0:
                positive_solution.append(t)
        final_t = min(positive_solution)
        return Vector2(point_a.x + final_t*(point_b.x - point_a.x),
                       point_a.y + final_t*(point_b.y - point_a.y))

    def invariant(self):
        """
        Ensure that the player stays inside the game borders.

        Returns
        -------
        bool
            True if the player is inside the game borders, False otherwise.
        """
        # ensures that the player stays inside the game
        if self.x - self.radius < 0:
            self.x = self.config["match"]["border_width"] + self.radius
            return False
        if self.x + self.radius > self.config["resolution"]["width"]:
            self.x = (self.config["resolution"]["width"]
                      - self.radius - self.config["match"]["border_width"])
            return False
        if self.y - self.radius < 0:
            self.y = self.config["match"]["border_width"] + self.radius
            return False
        if self.y + self.radius > self.config["resolution"]["height"]:
            self.y = (self.config["resolution"]["height"] -
                      self.radius - self.config["match"]["border_width"])
            return False
        return True

    def hook_invarint(self):
        """
        Determine whether the hook is out of bounds.

        Returns
        -------
        bool
            True if the hook is within the game borders, False otherwise.
        """
        # determines whether hook is out of bounds
        if (self.hook_coords.x < 0 or
            self.hook_coords.x > self.config["resolution"]["width"]
            or self.hook_coords.y < 0 or
                self.hook_coords.y > self.config["resolution"]["height"]):
            return False
        return True

    def dash(self, dt: float):
        """
        Perform the dash action.

        Parameters
        ----------
        dt : float
            The time step.
        """
        if not isinstance(dt, float):
            raise TypeError("Dt must be a float")
        if self.dashed_already == 0:
            self.dash_started.x = self.x
            self.dash_started.y = self.y
            self.coords_current.x = self.x
            self.coords_current.y = self.y
        if self.dashed_already < self.dash_length:
            direction = self.dash_destination - self.dash_started
            self.coords_current += 1600*dt*(direction.normalize())
            self.hooking = False
            self.end_hook = False
            self.pull = False
            self.dashing = True
            self.x = self.coords_current.x
            self.y = self.coords_current.y
            # make a seperate method
            if not self.invariant():
                self.dashing = False
            self.setRect()
            self.dashed_already += 1
        if self.dashed_already == self.dash_length:
            self.dashed_already = 0
            self.dash_on_cooldown = True

    def check_cooldowns(self, time: float):
        """
        Check and update cooldowns for hook and dash.

        Parameters
        ----------
        time : float
            The current time.
        """
        if not isinstance(time, float):
            raise TypeError("Time must be a float")
        if time - self.dash_cooldown_started > 10:
            self.dash_on_cooldown = False
        if time - self.hook_cooldown_started > 20:
            self.hook_on_cooldown = False


if __name__ == "__main__":
    raise RuntimeError("This module is designed for import only.")
