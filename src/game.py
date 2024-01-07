"""Module containing the Game object which acts as a top-level
game menu switch.
Raises
------
RuntimeError
    When called as the main script and not imported
"""

import datetime
import pygame
import pygame.locals
import utilities
from networking.network import Network

from game_objects.player import Player
from game_objects.ball import Ball

from menu.menu import (
    MainMenu,
    SettingsMenu,
    CreditsMenu,
    LogInMenu,
    RankedMenu,
    MatchHistoryMenu,
    LoadingScreenMenu
)
from menu.endscreen import EndScreenMenu

# pylint: disable=too-many-instance-attributes
class Game():
    """
    Main class for managing the game state, including network interactions, game menus, and gameplay elements.

    Attributes
    ----------
    config : dict
        Configuration settings for the game.
    net : Network
        Network object for handling online interactions.
    client_id : str
        Identifier for the client.
    online : bool
        Flag indicating whether the client is connected online.
    status : str
        Current status of the game (e.g., offline, online, ingame).
    response : dict or None
        Latest response received from the server.
    running, playing : bool
        Flags controlling the game loop.
    WIDTH, HEIGHT : int
        Dimensions of the game window.
    mpos : tuple
        Current mouse position.
    screen_res : list
        Screen resolution settings.
    display, screen : pygame.Surface
        Pygame surfaces for display.
    play_match : bool
        Flag indicating readiness to play a match.
    user_credentials : dict
        User credentials information.
    keys_pressed : tuple
        Current state of pressed keys.
    main_menu, settings_menu, etc. : Menu
        Different menu instances for the game.
    bg : pygame.Surface
        Background image for the game.
    player_1, player_2 : Player
        Player objects for the game.
    ball : Ball
        Ball object for the game.
    goal_1, goal_2 : pygame.Rect
        Goal areas in the game.
    border_width : int
        Width of the game border.
    border : pygame.Rect
        Rect object representing the game border.

    Parameters
    ----------
    config : dict
        Configuration settings for the game.
    """
    def __init__(self, config):
        pygame.init()
        pygame.display.set_caption("Novaglide")
        # config file
        self.config = config
        self.net = Network()
        # client receives his id on startup
        self.client_id = "uknown"
        # flag indicating whether client is connected to
        # the server(whether connection is active)
        self.online = False
        # offline/waiting_for_approval/online(in menu)/queued/ingame
        self.status = "offline"
        self.response = None
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False # pylint: disable=invalid-name
        self.WIDTH = self.config["resolution"]["width"] # pylint: disable=invalid-name
        self.HEIGHT = self.config["resolution"]["height"] # pylint: disable=invalid-name

        self.mpos = pygame.mouse.get_pos()
        self.screen_res = [self.WIDTH, self.HEIGHT]

        self.display = pygame.Surface(self.screen_res)
        self.screen = pygame.display.set_mode(
            self.screen_res, pygame.HWSURFACE, 32)
        # indicating whether player is ready to play
        self.play_match = False

        self.user_credentials = {"name": "", "password": ""}

        self.keys_pressed = pygame.key.get_pressed()

        self.main_menu = MainMenu(self)
        self.settings_menu = SettingsMenu(self)
        self.credits_menu = CreditsMenu(self)
        self.login_menu = LogInMenu(self)
        self.ranked_menu = RankedMenu(self)
        self.match_history_menu = MatchHistoryMenu(self)
        self.loading_screen_menu = LoadingScreenMenu(self)
        # start on the login screen
        self.curr_menu = self.login_menu
        # game elements that will be ploted to the screen
        self.bg = pygame.image.load(  # pylint: disable=invalid-name
            "./../resources/rink_" + str(self.settings_menu.map_indx + 1) + ".jpg").convert_alpha()
        self.player_1 = Player("unknown", 100, 360, self.config, color="green")
        self.player_2 = Player("unknown", 1180, 360, self.config, color="blue")
        self.ball = Ball(self.config)
        self.font = utilities.get_font(32)
        goal_height = self.config["match"]["goal_height"]
        goal_width = self.config["match"]["goal_width"]
        self.goal_1 = pygame.Rect(
            0, (self.display.get_height() - goal_height) // 2, goal_width, goal_height)
        self.goal_2 = pygame.Rect(self.display.get_width(
        ) - goal_width, (self.display.get_height() - goal_height) // 2, goal_width, goal_height)
        self.border_width = self.config["match"]["border_width"]
        self.border = self.display.get_rect()

    def start_match(self, match_data):
        """{"time":"datetime.datetime.now()",
        "sender":"server", "flag":"1v1_game",
        "data":[your_side,game_time,goals_1,goals_2, p_1_name,p_2_name
        ,p1_pos_x, p_1_pos_y,p1_mouse_pos_x,
        p_1_mouse_pos_y, p_1_dash_cooldown,p_1_hook_cooldown,p_1_hooking,
        p_2_pos_x, p2_pos_y,p_2_mouse_pos_x,
        p_2_mouse_pos_y, p_2_dash_cooldown,p_2_hook_cooldown,p_2_hooking,ball_x,ball_y]}
        """

        while self.status == "ingame":

            self.draw(match_data)
            self.check_inputs()

            self.response = self.share_inputs()

            if self.response["flag"] == "game_state_1":
                match_data = self.response["data"]

            elif self.response["flag"] == "end_game_state_1":
                self.status = "online"
                self.play_match = False
                self.curr_menu = EndScreenMenu(self, self.response["data"])

        self.play_match = False

    def reset_keys(self):
        """
        Reset the state of control keys.
        """
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

    def share_inputs(self):
        """
        Send the current input states to the server and receive a response.
        """
        parsed_data = self.parse_data(
            "ingame",
            [self.mpos, self.keys_pressed, self.settings_menu.controls]
        )
        return self.net.send(parsed_data)

    def check_inputs(self):
        """
        Update mouse position and key states, and handle game quit event.
        """
        self.mpos = pygame.mouse.get_pos()
        self.keys_pressed = pygame.key.get_pressed()
        if self.status == "ingame":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

    def draw(self, match_data):
        """
        Draw the game elements based on the current match data.
        """
        # draw background
        self.screen.blit(self.display, (0, 0))
        self.display.fill((150, 150, 150))
        self.display.blit(self.bg, (0, 0))

        # draw goals and border
        pygame.draw.rect(self.display, "red", self.goal_1)  # White goal
        pygame.draw.rect(self.display, "red", self.goal_2)  # White goal
        pygame.draw.rect(self.display, (255, 255, 255),
                         self.border, self.border_width)

        # draw scoreboard
        score_text = f"{match_data[2]} - {match_data[3]}"
        score_surface = self.font.render(
            score_text, True, (255, 255, 255))  # White text
        score_x = self.display.get_width() // 2 - score_surface.get_width() // 2
        score_y = 10  # 10 pixels from the top
        self.display.blit(score_surface, (score_x, score_y))

        # update all positions according to the server
        self.player_1.x, self.player_1.y = match_data[6], match_data[7]
        self.player_2.x, self.player_2.y = match_data[8], match_data[9]
        self.player_1.hook_coords.x, self.player_1.hook_coords.y = match_data[
            10], match_data[11]
        self.player_2.hook_coords.x, self.player_2.hook_coords.y = match_data[
            12], match_data[13]
        self.ball.x, self.ball.y = match_data[18], match_data[19]

        # display timer
        remaining_time = match_data[1]
        if not match_data[22]:
            timer_surface = self.font.render(
                f"Time Left: {int(remaining_time)}s", True, (255, 255, 255))
        else:
            timer_surface = self.font.render(
                f"Tiebreak", True, (255, 255, 255))
        self.display.blit(timer_surface, (10, 10))

        # if the player is hooking draw the hook
        if match_data[20]:
            self.player_1.hook(0, self.display)
        if match_data[21]:
            self.player_2.hook(0, self.display)

        # draw cooldowns indicating your side
        if match_data[0] == 1:
            cooldown_surace_dash_1 = self.font.render(
                f"Dash: {int(match_data[14])}s", True, (0, 221, 85))
            cooldown_surace_hook_1 = self.font.render(
                f"Hook: {int(match_data[15])}s", True, (0, 221, 85))
            cooldown_surace_dash_2 = self.font.render(
                f"Dash: {int(match_data[16])}s", True, (255, 255, 255))
            cooldown_surace_hook_2 = self.font.render(
                f"Hook: {int(match_data[17])}s", True, (255, 255, 255))
        else:
            cooldown_surace_dash_1 = self.font.render(
                f"Dash: {int(match_data[14])}s", True, (255, 255, 255))
            cooldown_surace_hook_1 = self.font.render(
                f"Hook: {int(match_data[15])}s", True, (255, 255, 255))
            cooldown_surace_dash_2 = self.font.render(
                f"Dash: {int(match_data[16])}s", True, (0, 221, 85))
            cooldown_surace_hook_2 = self.font.render(
                f"Hook: {int(match_data[17])}s", True, (0, 221, 85))
        self.display.blit(cooldown_surace_dash_1, (50, 630))
        self.display.blit(cooldown_surace_hook_1, (50, 680))
        self.display.blit(cooldown_surace_dash_2, (1000, 630))
        self.display.blit(cooldown_surace_hook_2, (1000, 680))

        self.player_1.setRect()
        self.player_2.setRect()
        self.ball.setRect()
        # update blocks etc.
        for entity in (self.player_1, self.player_2, self.ball):
            self.display.blit(entity.image, entity.rect)

        pygame.display.update()

    def parse_data(self, flag, data):
        """
        Parses provided data from the server
        """
        data = {"time": datetime.datetime.now(),
                "sender": self.client_id,
                "flag": flag,
                "data": data}
        return data

    @staticmethod
    def unpack_login_data(data):
        """
        Unpack login data received from the server.

        Parameters
        ----------
        data : dict
            Data received from the server.

        Returns
        -------
        tuple
            Unpacked login data.
        """
        return (data["data"][0], data["data"][1], data["data"][2])

    @staticmethod
    def unpack_elo_data(data):
        """
        Unpack Elo rating data received from the server.

        Parameters
        ----------
        data : dict
            Data received from the server.

        Returns
        -------
        tuple
            Unpacked Elo rating data.
        """
        return (data["data"][0], data["data"][1])

    @staticmethod
    def unpack_winrate_data(data):
        """
        Unpack win rate data received from the server.

        Parameters
        ----------
        data : dict
            Data received from the server.

        Returns
        -------
        float
            Unpacked win rate data.
        """
        return data["data"][0]

    @staticmethod
    def unpack_challenger_data(data):
        """
        Unpack challenger data received from the server.

        Parameters
        ----------
        data : dict
            Data received from the server.

        Returns
        -------
        list
            Unpacked challenger data.
        """
        return data["data"]

    @staticmethod
    def unpack_match_history_data(data):
        """
        Unpack match history data received from the server.

        Parameters
        ----------
        data : dict
            Data received from the server.

        Returns
        -------
        tuple
            Unpacked match history data.
        """
        return (data["data"][0], data["data"][1])


if __name__ == "__main__":
    raise RuntimeError("This module is designed for import only.")
