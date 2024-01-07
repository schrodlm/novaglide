# pylint: disable=C0302
# pylint: disable=duplicate-code
"""
Menu Module
-----------

Module containing the Menu abstract base class and its derived classes, which manage different types of menus in a game environment.
"""


import sys
import json
import datetime
from abc import ABC, abstractmethod
import pygame
import numpy as np

import utilities
from menu_elements.input_box import InputBox
from menu_elements.button import Button
from menu_elements.table import Table
from game_objects.player import Player


class Menu(ABC):
    """
    Abstract base class for game menus.

    Parameters
    ----------
    game : Game
        The main game instance.

    Attributes
    ----------
    game : Game
        The main game instance.
    run_display : bool
        Flag to control the menu display loop.
    mid_x : int
        The x-coordinate of the center of the screen.
    mid_y : int
        The y-coordinate of the center of the screen.

    Methods
    -------
    blit_screen() -> "Menu":
        Blits the screen and updates display.
    display_menu():
        Abstract method to display the menu.
    check_events()
        Abstract method to handle menu-specific events.
    """

    def __init__(self, game) -> None:
        self.game = game
        self.run_display = True
        self.mid_x = self.game.WIDTH // 2
        self.mid_y = self.game.HEIGHT // 2

    def blit_screen(self) -> "Menu":
        """
        Blit the screen and update the display.
        """
        self.game.screen.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()
        return self

    def share_status(self):
        """
        Share the current status of the game, especially in an online context.

        This method sends the current time, sender ID, game status flag, and additional data to the game server and receives a response.

        Returns
        -------
        response : dict or None
            The response from the server, or None if the game is not online.
        """
        response = None
        if self.game.online:
            response = self.game.net.send({"time": datetime.datetime.now(),
                                           "sender": self.game.client_id,
                                           "flag": self.game.status,
                                           "data": ["no_data"]})
        return response
    # ensuring that all menus implement these methods,
    # to make the API consistent

    @abstractmethod
    def display_menu(self):
        """
        Abstract method to display the menu.
        """
    @abstractmethod
    def check_events(self):
        """
        Abstract method to handle menu-specific events.
        """


class LogInMenu(Menu):
    """
    Menu for user login screen.

    Parameters
    ----------
    game : Game
        The main game instance.

    Attributes
    ----------
    log_in_button : Button
        Button for logging in.
    username_input : InputBox
        Input box for the username.
    password_input : InputBox
        Input box for the password.
    input_boxes : list
        List of input boxes.
    error_present : bool
        Flag indicating if login error is present.
    allow : str
        Permission level after login attempt.

    Methods
    -------
    display_menu()
        Display the login menu.
    check_events()
        Handle events in the login menu.
    draw_error(message: str)
        Draw error message on the screen.
    """

    def __init__(self, game):
        # init parent
        super().__init__(game)
        # log in button
        self.log_in_button = Button(image=None, pos=(self.mid_x, 460),
                                    text_input="LOG IN",
                                    font=utilities.get_font(75),
                                    base_color="black",
                                    hovering_color="aqua")
        # initializing input boxes for username and password
        self.username_input = InputBox(x=440, y=200, w=400, h=70,
                                       hide=False, config=self.game.config)
        self.password_input = InputBox(x=440, y=300, w=400, h=70,
                                       hide=True, config=self.game.config)
        # group same objects
        self.input_boxes = [self.username_input, self.password_input]
        self.error_present = False
        self.allow = None

    def display_menu(self) -> "LogInMenu":
        """
        Display the login menu.
        """
        # reset input box text
        self.username_input.text = ""
        self.password_input.text = ""
        # TODO: logout from the server
        self.run_display = True
        while self.run_display:
            self.share_status()
            self.game.check_inputs()
            self.game.display.fill((0, 0, 0))
            # draw background
            self.game.display.blit(utilities.get_image("background_main"),
                                   (0, 0))
            # draw instructions
            utilities.draw_text("Login with your nickname and password",
                                30,
                                self.mid_x,
                                150,
                                self.game.display,
                                self.game.config["colours"]["black"])
            if self.error_present:
                self.draw_error(self.allow)
            self.log_in_button.change_color(self.game.mpos).update(self.game.
                                                                   display)
            self.check_events().blit_screen()

        return self

    def check_events(self) -> "LogInMenu":
        """
        Handle events in the login menu.
        """
        for event in pygame.event.get():
            # closing the game with mouse
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.log_in_button.check_for_input(self.game.mpos):
                    if not self.game.online:
                        self.game.net.connect()
                        self.game.online = True
                        self.game.status = "waiting_for_approval"
                    if self.game.online:
                        self.game.status, self.allow, self.game.client_id = self.game.unpack_login_data(self.game.net.send(self.
                                                                                                                           game.parse_data(
                                                                                                                               "log_in_data",
                                                                                                                               [self.username_input.text, self.password_input.text])))

                    if self.allow in ("known user", "registering new user"):
                        self.error_present = False
                        self.allow = None
                        self.run_display = False
                        self.game.status = "online"
                        self.game.curr_menu = self.game.main_menu
                        self.game.user_credentials["name"] = (self.
                                                              username_input.text)
                        self.game.user_credentials["password"] = (self.
                                                                  password_input.text)
                        break

                    self.error_present = True

            for box in self.input_boxes:
                box.handle_event(event)
        for box in self.input_boxes:
            box.draw_updated(self.game.display)
        return self

    def draw_error(self, message):
        """
        Draw error message on the screen.

        Parameters
        ----------
        message : str
            The error message to be displayed.
        """
        utilities.draw_text(message, 30,
                            self.mid_x, 550, self.game.display,
                            self.game.config["colours"]["black"])


# pylint: disable=too-many-instance-attributes
class MainMenu(Menu):
    """
    A subclass of Menu for displaying the main menu in a game.

    This menu provides various options like playing different game modes, viewing match history, accessing the ranked system, settings, and credits.

    Attributes
    ----------
    buttons : pygame.sprite.Group
        Group of buttons used in the menu.
    play_1v1_button : Button
        Button to start a 1v1 game.
    play_2v2_button : Button
        Button to start a 2v2 game.
    match_history_button : Button
        Button to view match history.
    ranked_button : Button
        Button to access the ranked system.
    back_button : Button
        Button to go back.
    settings_button : Button
        Button to access settings.
    credits_button : Button
        Button to view credits.
    logged_user_text : pygame.Surface
        Surface containing the rendered text of the logged-in user's name.
    logged_user_rect : pygame.Rect
        Rectangle for positioning the logged user text.
    main_menu_text : pygame.Surface
        Surface containing the rendered text 'NOVAGLIDE'.
    main_menu_rect : pygame.Rect
        Rectangle for positioning the main menu text.

    Parameters
    ----------
    game : Game
        The main game instance.
    """
    def __init__(self, game):
        super().__init__(game)
        self.buttons = pygame.sprite.Group()
        hovering_color = self.game.config["design"]["hovering_colour"]
        self.play_1v1_button = Button(image=None, pos=(self.mid_x, 300),
                                      text_input="Play 1v1", font=utilities.get_font(40),
                                      base_color="black", hovering_color=hovering_color)
        self.play_2v2_button = Button(image=None, pos=(self.mid_x, 370),
                                      text_input="Play 2v2", font=utilities.get_font(40),
                                      base_color="black", hovering_color=hovering_color)
        self.match_history_button = Button(image=None, pos=(self.mid_x, 440),
                                           text_input="Match history", font=utilities.get_font(40),
                                           base_color="black", hovering_color=hovering_color)
        self.ranked_button = Button(image=None, pos=(self.mid_x, 510),
                                    text_input="Ranked system", font=utilities.get_font(40),
                                    base_color="black", hovering_color=hovering_color)
        self.back_button = Button(image=utilities.get_image("back_arrow"), pos=(70, 100),
                                  text_input="", font=utilities.get_font(40),
                                  base_color=(133, 88, 255), hovering_color=hovering_color)
        self.settings_button = Button(image=None, pos=(self.mid_x, 580),
                                      text_input="Settings", font=utilities.get_font(40),
                                      base_color="black", hovering_color=hovering_color)
        self.credits_button = Button(image=None, pos=(self.mid_x, 650),
                                     text_input="Credits", font=utilities.get_font(40),
                                     base_color="black", hovering_color=hovering_color)
        # Grouping buttons
        self.buttons.add(self.play_1v1_button)
        self.buttons.add(self.play_2v2_button)
        self.buttons.add(self.match_history_button)
        self.buttons.add(self.ranked_button)
        self.buttons.add(self.back_button)
        self.buttons.add(self.settings_button)
        self.buttons.add(self.credits_button)
        # creating texts and their rectangles
        self.logged_user_text = utilities.get_font(40).render(
            self.game.user_credentials.get("name"), True, self.game.config["colours"]["aqua"])
        self.logged_user_rect = self.logged_user_text.get_rect(
            topleft=(15, 15))

        self.main_menu_text = utilities.get_font(100).render(
            "NOVAGLIDE", True, "black")
        self.main_menu_rect = self.main_menu_text.get_rect(
            center=(self.mid_x, 150))

    def display_menu(self):
        """
        Display menu.
        """
        self.run_display = True
        while self.run_display:
            self.share_status()

            # tick and fill new background
            self.game.check_inputs()
            self.game.display.fill((0, 0, 0))
            self.game.display.blit(
                utilities.get_image("background_main"), (0, 0))
            # need to regenerate every time because the name is dynamically changing
            self.logged_user_text = utilities.get_font(40).render(
                self.game.user_credentials.get("name"), True, self.game.config["colours"]["aqua"])
            self.logged_user_rect = self.logged_user_text.get_rect(
                topleft=(15, 15))
            # draw texts
            self.game.display.blit(self.logged_user_text,
                                   self.logged_user_rect)
            self.game.display.blit(self.main_menu_text, self.main_menu_rect)
            # check all events
            self.check_events()
            # update all buttons
            for button in self.buttons:
                button.change_color(self.game.mpos)
            self.buttons.update(self.game.display)
            self.blit_screen()

    def check_events(self):
        """
        Handles incoming user events.
        """
        for event in pygame.event.get():
            # closing the game with mouse
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.play_1v1_button.check_for_input(self.game.mpos):
                    self.run_display = False
                    self.game.curr_menu = self.game.loading_screen_menu
                    self.game.play_match = True
                    break
                if self.play_2v2_button.check_for_input(self.game.mpos):
                    # TODO: implement multiplayer
                    print("2v2 selected")

                if self.settings_button.check_for_input(self.game.mpos):
                    self.run_display = False
                    self.game.curr_menu = self.game.settings_menu

                if self.back_button.check_for_input(self.game.mpos):
                    self.run_display = False
                    self.game.curr_menu = self.game.login_menu
                    self.game.user_credentials = {"name": "", "password": ""}

                if self.ranked_button.check_for_input(self.game.mpos):
                    self.run_display = False
                    self.game.curr_menu = self.game.ranked_menu
                if self.match_history_button.check_for_input(self.game.mpos):
                    self.run_display = False
                    self.game.curr_menu = self.game.match_history_menu

                if self.credits_button.check_for_input(self.game.mpos):
                    self.run_display = False
                    self.game.curr_menu = self.game.credits_menu

# pylint: disable=too-many-instance-attributes

class LoadingScreenMenu(Menu):
    """
    A subclass of Menu for displaying the loading screen in a game.

    This menu shows a waiting message and animated loading points while waiting for opponents in the lobby.

    Attributes
    ----------
    waiting_text : pygame.Surface
        Surface containing the rendered text 'Waiting for opponents'.
    waiting_text_rect : pygame.Rect
        Rectangle for positioning the waiting text.
    leave_text : pygame.Surface
        Surface containing the rendered text 'Do not leave the lobby.'.
    leave_text_rect : pygame.Rect
        Rectangle for positioning the leave text.
    loading_points_x_1, loading_points_y_1 : tuple
        Coordinates for the first set of loading points.
    loading_points_x_2, loading_points_y_2 : tuple
        Coordinates for the second set of loading points.
    loading_points_x_3, loading_points_y_3 : tuple
        Coordinates for the third set of loading points.
    loading_points_x_4, loading_points_y_4 : tuple
        Coordinates for the fourth set of loading points.
    x_generator_1, y_generator_1 : generator
        Generators for the x and y coordinates of the first set of loading points.
    x_generator_2, y_generator_2 : generator
        Generators for the x and y coordinates of the second set of loading points.
    x_generator_3, y_generator_3 : generator
        Generators for the x and y coordinates of the third set of loading points.
    x_generator_4, y_generator_4 : generator
        Generators for the x and y coordinates of the fourth set of loading points.

    Parameters
    ----------
    game : Game
        The main game instance.
    """
    def __init__(self, game) -> None:
        super().__init__(game)
        self.waiting_text = utilities.get_font(40).render(
            "Waiting for opponents", True, "black")
        self.waiting_text_rect = self.waiting_text.get_rect(
            center=(self.mid_x, 120))
        self.leave_text = utilities.get_font(40).render(
            "Do not leave the lobby.", True, "black")
        self.leave_text_rect = self.leave_text.get_rect(
            center=(self.mid_x, 170))
        self.loading_points_x_1, self.loading_points_y_1 = LoadingScreenMenu.generate_circle_coordinates(
            120, ball_start=1)
        self.loading_points_x_2, self.loading_points_y_2 = LoadingScreenMenu.generate_circle_coordinates(
            120, ball_start=2)
        self.loading_points_x_3, self.loading_points_y_3 = LoadingScreenMenu.generate_circle_coordinates(
            120, ball_start=3)
        self.loading_points_x_4, self.loading_points_y_4 = LoadingScreenMenu.generate_circle_coordinates(
            120, ball_start=4)
        self.x_generator_1 = LoadingScreenMenu.circular_list_generator(
            self.loading_points_x_1)
        self.y_generator_1 = LoadingScreenMenu.circular_list_generator(
            self.loading_points_y_1)
        self.x_generator_2 = LoadingScreenMenu.circular_list_generator(
            self.loading_points_x_2)
        self.y_generator_2 = LoadingScreenMenu.circular_list_generator(
            self.loading_points_y_2)
        self.x_generator_3 = LoadingScreenMenu.circular_list_generator(
            self.loading_points_x_3)
        self.y_generator_3 = LoadingScreenMenu.circular_list_generator(
            self.loading_points_y_3)
        self.x_generator_4 = LoadingScreenMenu.circular_list_generator(
            self.loading_points_x_4)
        self.y_generator_4 = LoadingScreenMenu.circular_list_generator(
            self.loading_points_y_4)

    def display_menu(self):
        """
        Display menu.
        """
        self.run_display = True
        while self.run_display:
            self.game.response = self.share_status()
            if self.game.response is not None and self.game.response["flag"] == "game_state_1":
                self.run_display = False
                self.game.play_match = True
            self.game.display.fill((0, 0, 0))
            self.game.display.blit(
                utilities.get_image("background_main"), (0, 0))
            self.game.display.blit(self.waiting_text, self.waiting_text_rect)
            self.game.display.blit(self.leave_text, self.leave_text_rect)
            pygame.draw.circle(self.game.display, (255, 255, 255), (next(
                self.x_generator_1), next(self.y_generator_1)), 7)
            pygame.draw.circle(self.game.display, (255, 255, 255), (next(
                self.x_generator_2), next(self.y_generator_2)), 7)
            pygame.draw.circle(self.game.display, (255, 255, 255), (next(
                self.x_generator_3), next(self.y_generator_3)), 7)
            pygame.draw.circle(self.game.display, (255, 255, 255), (next(
                self.x_generator_4), next(self.y_generator_4)), 7)
            self.check_events()
            self.blit_screen()

    def check_events(self):
        """
        Handles pygame events.
        """

        for event in pygame.event.get():
            # closing the game with mouse
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    @staticmethod
    def generate_circle_coordinates(radius, num_points=30, ball_start=1):
        """
        Generates circle coordinates.
        """
        starts = {1: np.linspace(0, 2*np.pi, num_points),
                  2: np.linspace(0.5*np.pi, 2.5*np.pi, num_points),
                  3: np.linspace(np.pi, 3*np.pi, num_points),
                  4: np.linspace(1.5*np.pi, 3.5*np.pi, num_points)}

        theta_repeated = np.repeat(starts.get(ball_start), 4)
        x = 640 + radius * np.cos(theta_repeated)
        y = 360 + radius * np.sin(theta_repeated)
        return (list(x), list(y))

    @staticmethod
    def circular_list_generator(my_list):
        """
        Generator of list
        """
        index = 0
        while True:
            yield my_list[index]
            index = (index + 1) % len(my_list)


class SettingsMenu(Menu):
    """
    A subclass of Menu for displaying and managing the settings screen in a game.

    This menu allows players to view and modify game settings such as music, volume, map selection, profile picture, and controls.

    Attributes
    ----------
    loaded_settings : dict
        The current settings loaded from a JSON file.
    music : bool
        Flag indicating if music is enabled.
    volume : int
        Current volume level.
    next_volume : int
        The next volume level to be set.
    max_map_indx : int
        Maximum index for map selection.
    map_indx : int
        Current index of the selected map.
    next_map_indx : int
        The next index of the map to be selected.
    maps_ordered : list
        An ordered list of available maps.
    map : str
        The currently selected map.
    profile_picture : str
        The file path of the current profile picture.
    controls : dict
        The current control settings.
    player : Player
        A Player object for displaying skin preview.
    buttons : pygame.sprite.Group
        A group containing all buttons in the settings menu.

    Parameters
    ----------
    game : Game
        The main game instance.
    """
    def __init__(self, game):
        super().__init__(game)
        # load settings JSON
        self.loaded_settings = utilities.get_settings()
        self.music = self.loaded_settings["Music"]

        self.volume = self.loaded_settings["Volume"]
        self.next_volume = self.volume

        self.max_map_indx = 2
        self.map_indx = int(self.loaded_settings["Map"][-5]) - 1
        self.next_map_indx = 0
        self.maps_ordered = utilities.get_ordered_maps()
        self.map = self.maps_ordered[self.map_indx]

        self.profile_picture = self.loaded_settings["ProfilePicture"]

        self.controls = self.loaded_settings["Controls"]
        # using player to plot skin preview
        self.player = Player("", 200, self.mid_y + 100, self.game.config, 100)
        # group of all buttons
        self.buttons = pygame.sprite.Group()

        # music arrows
        self.music_button_left_arrow = Button(image=utilities.get_image("left_arrow"),
                                              pos=(self.mid_x - 100, 170),
                                              text_input="", font=utilities.get_font(40),
                                              base_color="black", hovering_color="aqua")
        self.music_button_right_arrow = Button(image=utilities.get_image("right_arrow"),
                                               pos=(self.mid_x + 100, 170),
                                               text_input="", font=utilities.get_font(40),
                                               base_color="black", hovering_color="aqua")
        # volume arrows
        self.volume_button_left_arrow = Button(image=utilities.get_image("left_arrow"),
                                               pos=(self.mid_x - 100, 310),
                                               text_input="", font=utilities.get_font(40),
                                               base_color="black", hovering_color="aqua")
        self.volume_button_right_arrow = Button(image=utilities.get_image("right_arrow"),
                                                pos=(self.mid_x + 100, 310),
                                                text_input="", font=utilities.get_font(40),
                                                base_color="black", hovering_color="aqua")
        # controls arrows
        self.controls_button_left_arrow = Button(image=utilities.get_image("left_arrow"),
                                                 pos=(self.mid_x - 120, 450),
                                                 text_input="", font=utilities.get_font(40),
                                                 base_color="black", hovering_color="aqua")
        self.controls_button_right_arrow = Button(image=utilities.get_image("right_arrow"),
                                                  pos=(self.mid_x + 120, 450),
                                                  text_input="", font=utilities.get_font(40),
                                                  base_color="black", hovering_color="aqua")
        # map arrows
        self.map_button_left_arrow = Button(image=utilities.get_image("left_arrow"),
                                            pos=(980 - 120, 150),
                                            text_input="", font=utilities.get_font(40),
                                            base_color="black", hovering_color="aqua")
        self.map_button_right_arrow = Button(image=utilities.get_image("right_arrow"),
                                             pos=(980 + 120, 150),
                                             text_input="", font=utilities.get_font(40),
                                             base_color="black", hovering_color="aqua")
        # exit_button
        self.exit_button = Button(image=utilities.get_image("back_arrow"), pos=(70, 50),
                                  text_input="", font=utilities.get_font(40),
                                  base_color=(133, 88, 255), hovering_color="aqua")
        # Grouping buttons
        self.buttons.add(self.volume_button_left_arrow)
        self.buttons.add(self.volume_button_right_arrow)
        self.buttons.add(self.music_button_left_arrow)
        self.buttons.add(self.music_button_right_arrow)
        self.buttons.add(self.controls_button_left_arrow)
        self.buttons.add(self.controls_button_right_arrow)
        self.buttons.add(self.map_button_left_arrow)
        self.buttons.add(self.map_button_right_arrow)
        self.buttons.add(self.exit_button)

    def display_menu(self):
        """
        Displays the menu on screen.
        """
        self.run_display = True
        while self.run_display:
            self.share_status()
            self.game.check_inputs()
            self.check_events()
            self.game.display.fill((0, 0, 0))
            self.game.display.blit(
                utilities.get_image("background_main"), (0, 0))
            # Music settings
            utilities.draw_text("Music", 40, self.mid_x, 100,
                                self.game.display, self.game.config["colours"]["black"])
            # music settings
            if self.music:
                utilities.draw_text("ON", 30, self.mid_x,
                                    170, self.game.display)
            else:
                utilities.draw_text("OFF", 30, self.mid_x,
                                    170, self.game.display)
            # Volume settings
            utilities.draw_text("Volume", 40, self.mid_x, 240,
                                self.game.display, self.game.config["colours"]["black"])
            utilities.draw_text(utilities.convert_volume(self.volume), 30,
                                self.mid_x, 310, self.game.display)
            # Map choice
            utilities.draw_text(
                "Map", 40, 980, 100, self.game.display, self.game.config["colours"]["black"])
            utilities.draw_text(utilities.get_map_names(
                self.map), 30, 980, 150, self.game.display)
            # map preview
            self.game.display.blit(
                pygame.transform.rotate(pygame.image.load(
                    self.map).convert_alpha(), 90),
                (840, 170))
            # skin preview
            utilities.draw_text("Your skin", 30, 200, 200, self.game.display)
            # bliting player skin
            # TODO: make more skins that will be circular in class player
            self.game.display.blit(self.player.image, self.player.rect)
            # controls settings
            utilities.draw_text("Controls", 40, self.mid_x, 380,
                                self.game.display, self.game.config["colours"]["black"])
            if self.controls == "wsad":
                utilities.draw_text(
                    "W S A D", 30, self.mid_x, 450, self.game.display)
            if self.controls == "arrows":
                utilities.draw_text("Arrows", 30, self.mid_x,
                                    450, self.game.display)
            # update/draw all buttons
            for button in self.buttons:
                button.change_color(self.game.mpos)
            self.buttons.update(self.game.display)
            self.blit_screen()

    # pylint: disable=too-many-branches
    def check_events(self):
        """
        Hadnles pygame and user inputs.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # music button revert
                if (self.music_button_right_arrow.check_for_input(self.game.mpos) or
                        self.music_button_left_arrow.check_for_input(self.game.mpos)):
                    self.music = not self.music

                # volume changing
                if self.volume_button_right_arrow.check_for_input(self.game.mpos):
                    self.next_volume = self.volume + 1
                    if self.next_volume <= 10 and self.next_volume >= 0:
                        self.volume = self.next_volume
                if self.volume_button_left_arrow.check_for_input(self.game.mpos):
                    self.next_volume = self.volume - 1
                    if self.next_volume <= 10 and self.next_volume >= 0:
                        self.volume = self.next_volume

                # controls changing
                if (self.controls_button_right_arrow.check_for_input(self.game.mpos) or
                        self.controls_button_left_arrow.check_for_input(self.game.mpos)):
                    if self.controls == "wsad":
                        self.controls = "arrows"
                    else:
                        self.controls = "wsad"
                # change map
                if self.map_button_right_arrow.check_for_input(self.game.mpos):
                    self.next_map_indx = self.map_indx + 1
                    if self.next_map_indx <= self.max_map_indx and self.next_map_indx >= 0:
                        self.map_indx = self.next_map_indx
                if self.map_button_left_arrow.check_for_input(self.game.mpos):
                    self.next_map_indx = self.map_indx - 1
                    if self.next_map_indx <= self.max_map_indx and self.next_map_indx >= 0:
                        self.map_indx = self.next_map_indx
                # change it immediately so it gets saved
                self.map = self.maps_ordered[self.map_indx]
                # save new settings to json
                self.save_settings()
                # return to main menu
                if self.exit_button.check_for_input(self.game.mpos):
                    self.run_display = False
                    self.game.curr_menu = self.game.main_menu

    def save_settings(self):
        """
        Saves settings.
        """
        new_settings = {}
        new_settings["Music"] = self.music
        new_settings["Volume"] = self.volume
        new_settings["Map"] = self.map
        new_settings["ProfilePicture"] = self.profile_picture
        new_settings["Controls"] = self.controls
        with open("./../settings/settings.json", 'w', encoding="UTF-8") as stgs:
            json.dump(new_settings, stgs)

# pylint: disable=too-many-instance-attributes
class RankedMenu(Menu):
    """
    A subclass of Menu for displaying the ranked menu in a game.

    This menu shows the player's rank, division, win rate, and a leaderboard of top players.

    Attributes
    ----------
    elements : pygame.sprite.Group
        Group of elements used in the menu, including buttons and tables.
    back_button_rm : Button
        Button to go back to the previous menu.
    elo : str
        The player's Elo rating.
    division : str
        The player's division.
    player_preview : Player
        Player object for previewing player stats.
    winrate : str
        The player's win rate.
    preview_page : int
        Current page number of the challenger leaderboard.
    next_preview_page : int
        The next page number to be displayed in the leaderboard.
    challenger_table : Table
        Table to display the top players' leaderboard.
    challenger_table_left_arrow : Button
        Button to navigate to the previous page of the leaderboard.
    challenger_table_right_arrow : Button
        Button to navigate to the next page of the leaderboard.

    Parameters
    ----------
    game : Game
        The main game instance.
    """
    def __init__(self, game):
        super().__init__(game)
        self.elements = pygame.sprite.Group()
        self.back_button_rm = Button(image=utilities.get_image("back_arrow"), pos=(70, 50),
                                     text_input="", font=utilities.get_font(40),
                                     base_color=(133, 88, 255), hovering_color=self.game.config["colours"]["aqua"])
        self.elo, self.division = "unknown", "unknown"
        self.player_preview = Player("", 170, 250, self.game.config, 0, 70)
        self.winrate = "unknown"
        self.preview_page = 1
        self.next_preview_page = 2
        self.challenger_table = Table(
            self.game.config, header="CHALLENGERS", cols_sizes=[50, 350, 100, 120])
        # challenger table buttons
        # will change the preview (1-10,11-20,... up to 100)
        self.challenger_table_left_arrow = Button(image=utilities.get_image("left_arrow"),
                                                  pos=(int((((self.challenger_table.max_x -
                                                              self.challenger_table.top_left_coords[0]) // 2)
                                                            + self.challenger_table.top_left_coords[0]) - 150),
                                                       self.challenger_table.top_left_coords[1] - 20),
                                                  text_input="", font=utilities.get_font(40),
                                                  base_color=self.game.config["colours"]["black"], hovering_color=self.game.config["design"]["hovering_colour"])
        self.challenger_table_right_arrow = Button(image=utilities.get_image("right_arrow"),
                                                   pos=(int((((self.challenger_table.max_x -
                                                               self.challenger_table.top_left_coords[0]) // 2)
                                                             + self.challenger_table.top_left_coords[0]) + 150),
                                                        self.challenger_table.top_left_coords[1] - 20),
                                                   text_input="", font=utilities.get_font(40),
                                                   base_color=self.game.config["colours"]["black"], hovering_color=self.game.config["design"]["hovering_colour"])
        self.elements.add(self.back_button_rm)
        self.elements.add(self.challenger_table_left_arrow)
        self.elements.add(self.challenger_table_right_arrow)
        self.elements.add(self.challenger_table)

    def draw_ranked_names(self, names):
        """
        Draws names of players in ranked
        """
        xs = [120, 280, 455, 660, 900, 1113]
        ys = [465, 460, 420, 421, 420, 415]
        intervals = ["<1000", "<2000", "<4000", "<6000", ">= 6000", "TOP 100"]
        for name, interval, x, y in zip(names, intervals, xs, ys):
            utilities.draw_text(name, 25, x, y,
                                self.game.display,
                                color=self.game.config["colours"]["aqua"])
            utilities.draw_text(interval, 15, x, y + 20,
                                self.game.display,
                                color=self.game.config["colours"]["aqua"])

    def display_menu(self):
        """
        Draws names of players in ranked
        """
        self.elo, self.division = self.get_my_elo()
        self.winrate = self.get_winrate()
        challengers_data = self.get_challengers()
        self.run_display = True
        while self.run_display:
            self.share_status()
            self.game.check_inputs()
            self.check_events()
            # draw background
            r, g, b = (self.game.config["design"]
                       ["ranked_background_colour"].values())
            self.game.display.fill((r, g, b))
            # draw trophies on the screen
            border = pygame.transform.scale_by(
                utilities.get_image(self.division), 0.4)
            self.game.display.blit(utilities.get_image("ranks"), (0, 400))
            # draw player and his stats
            utilities.draw_text("Your stats", 35, 470, 130,
                                self.game.display,
                                color=self.game.config["colours"]["aqua"])
            utilities.draw_text(f"ELO:   {self.elo}", 35, 470, 200,
                                self.game.display,
                                color=self.game.config["colours"]["aqua"])
            utilities.draw_text(self.division, 35, 470, 270,
                                self.game.display,
                                color=self.game.config["colours"]["aqua"])
            utilities.draw_text(str(self.winrate) + "%", 35, 470, 340,
                                self.game.display,
                                color=self.game.config["colours"]["aqua"])
            self.game.display.blit(
                self.player_preview.image, self.player_preview.rect)
            # draw names
            self.draw_ranked_names(
                ["WOODEN", "IRON", "BRONZE", "SILVER", "GOLD", "CHALLENGER"])
            self.elements.update(self.game.display)
            # hardcoded coordinates because of different sizes of the pictures
            border_coordinates = {"WOODEN": 80, "IRON": 95, "BRONZE": 95,
                                  "SILVER": 105, "GOLD": 120, "CHALLENGER": 130}
            self.game.display.blit(border,
                                   (self.player_preview.x - border_coordinates[self.division] + 3,
                                    self.player_preview.y-border_coordinates[self.division]))

            self.challenger_table.insert_data(data=challengers_data[(
                (self.preview_page - 1)*40):((self.preview_page - 1)*40) + 40], display=self.game.display)
            self.challenger_table.create_positions = False
            self.blit_screen()

    def check_events(self):
        """
        Handles pygame and user inputs.
        """
        for event in pygame.event.get():
            # closing the game with mouse
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.back_button_rm.check_for_input(self.game.mpos):
                    self.run_display = False
                    self.game.curr_menu = self.game.main_menu
                if self.challenger_table_right_arrow.check_for_input(self.game.mpos):
                    self.next_preview_page = self.preview_page + 1
                    if self.next_preview_page <= 10 and self.next_preview_page >= 1:
                        self.preview_page = self.next_preview_page
                if self.challenger_table_left_arrow.check_for_input(self.game.mpos):
                    self.next_preview_page = self.preview_page - 1
                    if self.next_preview_page <= 10 and self.next_preview_page >= 1:
                        self.preview_page = self.next_preview_page

    def get_my_elo(self):
        """
        Retrieve the player's Elo rating and determine their division based on the rating.

        This method requests the player's Elo rating and the Elo ratings of the top 100 players, then categorizes the player into a division based on their rating.

        Returns
        -------
        tuple
            A tuple containing the player's Elo rating and their division as a string.
        """
        elo, elo_of_top_100 = self.game.unpack_elo_data(self.game.net.send(self.game.parse_data("get_elo", [
            self.game.user_credentials["name"]
        ])))

        elo_of_top = max(elo_of_top_100[0][0], elo_of_top_100[1][0]) if len(elo_of_top_100) > 1 else elo_of_top_100[0][0]



        division = "WOODEN"
        if elo >= 1000:
            division = "IRON"
        if elo >= 2000:
            division = "BRONZE"
        if elo >= 4000:
            division = "SILVER"
        if elo >= 6000:
            division = "GOLD"
        if elo >= elo_of_top:
            division = "CHALLENGER"
        return (elo, division)

    def get_challengers(self):
        """
        Gets best 100 player in the world.
        """
        # TODO: query top 100 players ordered by elo
        challenger_data = self.game.unpack_challenger_data(
            self.game.net.send(self.game.parse_data("get_challengers", ["no_data"])))
        final_data = []
        for row in zip(range(1, 101), challenger_data):
            final_data += [str(row[0]), str(row[1][0]),
                           str(row[1][1]) + "%", str(row[1][2])]
        if len(challenger_data) < 100:
            for rest in range(len(challenger_data) + 1, 101):
                final_data += [str(rest), "NA", "NA", "NA"]
        return final_data

    def get_winrate(self):
        """
        Gets clients winrate.
        """
        return self.game.unpack_winrate_data(self.game.net.send(self.game.parse_data("get_winrate", [self.game.user_credentials["name"]])))


class MatchHistoryMenu(Menu):
    """
    A subclass of Menu for displaying the match history in a game.

    This menu shows the player's match history, including separate tables for solo and duo games.

    Attributes
    ----------
    elements : pygame.sprite.Group
        Group of elements used in the menu, including buttons and tables.
    back_button_hm : Button
        Button to go back to the previous menu.
    match_history_table : Table
        Table to display match history for solo games.
    draw_solo : bool
        Flag to indicate whether to draw the solo games table.

    Parameters
    ----------
    game : Game
        The main game instance.
    """
    def __init__(self, game):
        super().__init__(game)
        self.elements = pygame.sprite.Group()
        self.back_button_hm = Button(image=utilities.get_image("back_arrow"), pos=(70, 50),
                                     text_input="", font=utilities.get_font(40),
                                     base_color=(133, 88, 255), hovering_color=self.game.config["colours"]["aqua"])
        # seperate table for solo games and duo games
        self.match_history_table = Table(self.game.config, header="MATCH HISTORY SOLO", row_size=60, top_left_coords=(100, 80),
                                         header_font_size=50, cols_sizes=[230, 230, 70, 70, 230, 230])
        self.elements.add(self.match_history_table)
        self.elements.add(self.back_button_hm)
        self.draw_solo = True

    def display_menu(self):
        """
        Gets best 100 player in the world.
        """
        self.run_display = True
        data_solo, data_duo = self.get_match_history()
        while self.run_display:
            self.share_status()
            self.game.check_inputs()
            self.check_events()
            self.game.display.fill((0, 0, 0))
            if self.draw_solo:
                utilities.draw_text("Press arrows to change to duo match history",
                                    18, 640, 700, self.game.display)
                self.match_history_table.header = "MATCH HISTORY SOLO"
            else:
                utilities.draw_text("Press arrows to change to solo match history",
                                    18, 640, 700, self.game.display)
                self.match_history_table.header = "MATCH HISTORY DUO"
            self.elements.update(self.game.display)
            if self.draw_solo:
                self.match_history_table.insert_data(
                    data=data_solo, display=self.game.display)
            else:
                self.match_history_table.insert_data(
                    data=data_duo, display=self.game.display)
            self.match_history_table.create_positions = False
            self.blit_screen()

    def get_match_history(self):
        """
        Gets players match history.
        """
        data_solo, data_duo = self.game.unpack_match_history_data(self.game.net.send(
            self.game.parse_data("get_match_history", [self.game.user_credentials["name"]])))
        final_data_solo = []
        final_data_duo = []
        for row in data_solo:
            final_data_solo += [str(row[1]), str(row[3]),
                                str(row[5]), str(row[6]), str(row[4]), str(row[2])]
        if len(data_solo) < 10:
            for _ in range(len(data_solo) + 1, 11):
                final_data_solo += ["NA", "NA", "NA", "NA", "NA", "NA"]
        for row in data_duo:
            final_data_duo += [str(row[1]) + "-" + str(row[2]), str(row[5]) + "-" + str(row[6]), str(
                row[9]), str(row[10]), str(row[7]) + "-" + str(row[8]), str(row[3]) + "-" + str(row[4])]
        if len(data_duo) < 10:
            for _ in range(len(data_duo) + 1, 11):
                final_data_duo += ["NA", "NA", "NA", "NA", "NA", "NA"]
        return (final_data_solo, final_data_duo)

    def check_events(self):
        """
        Gets players match history.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.back_button_hm.check_for_input(self.game.mpos):
                    self.run_display = False
                    self.game.curr_menu = self.game.main_menu
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    self.draw_solo = not self.draw_solo


class CreditsMenu(Menu):
    """
    A subclass of Menu for displaying the credits screen in a game.

    This menu shows the credits information related to the game.

    Attributes
    ----------
    Inherits all attributes from the Menu class.

    Parameters
    ----------
    game : Game
        The main game instance.
    """
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        """
        Displays user menu
        """
        self.run_display = True
        while self.run_display:
            self.share_status()
            self.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.fill(self.game.config["colours"]["black"])
            utilities.draw_text('Press Backspace to exit',
                                15, 170, 30, self.game.display)
            utilities.draw_text('Credits',
                                20, self.game.WIDTH // 2, self.game.HEIGHT // 2 - 20, self.game.display)
            utilities.draw_text('TOM B & MAT S',
                                15, self.game.WIDTH // 2, self.game.HEIGHT // 2 + 10, self.game.display)
            self.blit_screen()

    def check_events(self):
        """
        Checks events.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.game.BACK_KEY = True


if __name__ == "__main__":
    raise RuntimeError("This module is designed for import only.")
