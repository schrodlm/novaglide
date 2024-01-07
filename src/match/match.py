"""
Match Module
------------

A module for managing and updating the state of a 1v1 match in a pygame-based game, including player actions, ball dynamics, and match statistics.
"""
import pygame
from pygame import Vector2
from match.match_stats import MatchStats

# pylint: disable=too-many-instance-attributes
# pylint: disable=too-few-public-methods
class Match():
    """
    A class to initialize and manage the basic state of a game match.

    Attributes
    ----------
    config : dict
        Configuration settings for the match.
    max_height : int
        Maximum height of the game display.
    max_width : int
        Maximum width of the game display.
    display : pygame.Surface
        The main display surface of the game.
    match_duration : int
        Duration of the match in seconds.
    score : tuple
        Current score of the match.
    tiebreak : bool
        Flag to indicate if the match is in a tiebreak.
    end_game_in_tiebreak : bool
        Flag to end the game during a tiebreak.
    entities : pygame.sprite.Group
        Group containing all game entities.
    solids : pygame.sprite.Group
        Group containing all solid objects.
    border : pygame.Rect
        The border of the play area.
    clock : pygame.time.Clock
        Clock object for managing frame rate.
    dt : float
        Time delta for frame rate management.
    last_tick : int
        Timestamp of the last tick.
    ttime : int
        Total time passed.
    playing : bool
        Flag indicating if the match is currently playing.
    goal1 : pygame.Rect
        Rect object for the first goal.
    goal2 : pygame.Rect
        Rect object for the second goal.
    mpos_1 : tuple
        Mouse position for player 1.
    mpos_2 : tuple
        Mouse position for player 2.
    start_time : int
        Start time of the match.
    elapsed_time : float
        Elapsed time since the start of the match.
    dash_time_1 : float
        Remaining dash cooldown time for player 1.
    hook_time_1 : float
        Remaining hook cooldown time for player 1.
    dash_time_2 : float
        Remaining dash cooldown time for player 2.
    hook_time_2 : float
        Remaining hook cooldown time for player 2.
    remaining_time : float
        Remaining time of the match.

    Parameters
    ----------
    config : dict
        Configuration settings for the match.
    """

    def __init__(self, config):
        pygame.init()
        self.config = config
        self.max_height, self.max_width = self.config["resolution"][
            "height"], self.config["resolution"]["width"]
        # Define borders
        self.display = pygame.Surface((self.max_width, self.max_height))
        self.match_duration = 30
        self.score = (0, 0)
        self.tiebreak = False
        self.end_game_in_tiebreak = False
        self.entities = pygame.sprite.Group()
        self.solids = pygame.sprite.Group()

        self.border = self.display.get_rect()
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.last_tick = pygame.time.get_ticks()
        self.ttime = self.clock.tick()
        self.clock.tick(60)
        self.playing = True
        # Define goals as rectangles
        goal_width = 20  # Width of the goal, adjust as needed
        goal_height = 100  # Height of the goal, adjust as needed
        self.goal1 = pygame.Rect(
            0, (self.max_height - goal_height) // 2, goal_width, goal_height)
        self.goal2 = pygame.Rect(
            self.max_width - goal_width, (self.max_height - goal_height) // 2, goal_width, goal_height)

        self.mpos_1 = (0, 0)
        self.mpos_2 = (0, 0)
        # Get the current time in milliseconds
        self.start_time = pygame.time.get_ticks()
        self.elapsed_time = 0
        self.dash_time_1 = 0
        self.hook_time_1 = 0
        self.dash_time_2 = 0
        self.hook_time_2 = 0
        self.remaining_time = self.match_duration


class Match1v1(Match):
    """
    A subclass of Match for managing 1v1 game matches.

    Attributes
    ----------
    p1_id : str
        Identifier for player 1.
    p2_id : str
        Identifier for player 2.
    p1 : Player
        Player 1 object.
    p2 : Player
        Player 2 object.
    ball : Ball
        Ball object in the match.
    match_stats : MatchStats
        Object for tracking match statistics.
    p_1_update : Any
        Update information for player 1.
    p_2_update : Any
        Update information for player 2.
    p1_end_game_notified : bool
        Flag indicating if player 1 has been notified of game end.
    p2_end_game_notified : bool
        Flag indicating if player 2 has been notified of game end.

    Parameters
    ----------
    config : dict
        Configuration settings for the match.
    p1 : Player
        Player 1 object.
    p2 : Player
        Player 2 object.
    ball : Ball
        Ball object in the match.
    p1_id : str
        Identifier for player 1.
    p2_id : str
        Identifier for player 2.
    """

    # pylint: disable=too-many-arguments
    def __init__(self, config, p1, p2, ball, p1_id, p2_id):
        super().__init__(config)
        self.p1_id = p1_id
        self.p2_id = p2_id
        self.p1 = p1
        self.p2 = p2
        self.ball = ball
        self.entities.add(self.ball, self.p1, self.p2)
        # Stat class initialized
        self.match_stats = MatchStats(entities=self.entities)
        self.match_stats.set_elo(p1)
        self.match_stats.set_elo(p2)
        self.p_1_update = None
        self.p_2_update = None

        self.p1_end_game_notified = False
        self.p2_end_game_notified = False


    def reset_ball(self):
        """
        Reset the ball to its initial position and speed.

        This method is called when a goal is scored or when the match is reset.
        """

        self.ball.x = self.max_width // 2
        self.ball.y = self.max_height // 2
        # Reset the ball's speed
        # You can set this to an initial speed or to zero
        self.ball.speed = Vector2(0, 0)
        # Update the ball's rect to reflect the new position
        self.ball.setRect()

    def end_tiebreak(self):
        """
        End the tiebreak phase of the match if it's currently in a tiebreak.
        """
        if self.tiebreak:
            self.end_game_in_tiebreak = True

    def update_game_state(self):
        """
        Update the game state, including ball-goal collisions, player-ball interactions, and cooldown calculations.
        """
        # Check for ball collision with goals
        if self.goal1.colliderect(self.ball.rect):
            # Ball has entered goal 1
            # Update score and reset ball position, etc.
            self.score = (self.score[0], self.score[1] + 1)
            self.match_stats.add_goal(self.p2)
            self.reset_ball()
            self.end_tiebreak()

        if self.goal2.colliderect(self.ball.rect):
            # Ball has entered goal 2, increment score for player 1
            self.score = (self.score[0] + 1, self.score[1])
            self.match_stats.add_goal(self.p1)
            self.reset_ball()
            self.end_tiebreak()

        if pygame.sprite.collide_circle(self.p1, self.ball) or pygame.sprite.collide_circle(self.p2, self.ball):
            # 1. Calculate the collision normal
            if pygame.sprite.collide_circle(self.p1, self.ball):
                collision_normal = self.ball.rect.center - \
                    Vector2(self.p1.rect.center)
                self.match_stats.add_touch(self.p1)
            else:
                collision_normal = self.ball.rect.center - \
                    Vector2(self.p2.rect.center)
                self.match_stats.add_touch(self.p2)

            collision_normal.normalize_ip()  # Normalize the vector to have a magnitude of 1

            # 2. Determine the new speed of the ball
            speed_magnitude = 20  # You can adjust this value as needed
            self.ball.speed = collision_normal * speed_magnitude

        self.dt = self.clock.tick(60) / 1000

        self.elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000
        self.remaining_time = max(self.match_duration - self.elapsed_time, 0)

        if self.p_1_update is not None:
            self.update_player_1(self.p_1_update)
        if self.p_2_update is not None:
            self.update_player_2(self.p_2_update)
        self.ball.update(self.border)

        # calculating cooldowns for both players
        # Player_1
        self.dash_time_1 = 10 - \
            abs(self.elapsed_time - self.p1.dash_cooldown_started)
        self.hook_time_1 = 20 - \
            abs(self.elapsed_time - self.p1.hook_cooldown_started)
        self.dash_time_1 = max(0, self.dash_time_1)
        self.dash_time_1 = min(self.dash_time_1, 10)
        self.hook_time_1 = max(0, self.hook_time_1)
        self.hook_time_1 = min(self.hook_time_1, 20)
        if self.p1.dash_cooldown_started == 0:
            self.dash_time_1 = 0
        if self.p1.hook_cooldown_started == 0:
            self.hook_time_1 = 0
        # Player_2
        self.dash_time_2 = 10 - \
            abs(self.elapsed_time - self.p2.dash_cooldown_started)
        self.hook_time_2 = 20 - \
            abs(self.elapsed_time - self.p2.hook_cooldown_started)
        self.dash_time_2 = max(0, self.dash_time_2)
        self.dash_time_2 = min(self.dash_time_2, 10)
        self.hook_time_2 = max(0, self.hook_time_2)
        self.hook_time_2 = min(self.hook_time_2, 20)
        if self.p2.dash_cooldown_started == 0:
            self.dash_time_2 = 0
        if self.p2.hook_cooldown_started == 0:
            self.hook_time_2 = 0

    def update_player_1(self, inputs):
        """
        Update the state of player 1 based on the given inputs.

        Parameters
        ----------
        inputs : list
            Input data for updating player 1's state.
        """
        self.p1.update(
            self.dt, None, inputs[0], self.elapsed_time, inputs[1], inputs[2])

    def update_player_2(self, inputs):
        """
        Update the state of player 2 based on the given inputs.

        Parameters
        ----------
        inputs : list
            Input data for updating player 2's state.
        """
        self.p2.update(
            self.dt, None, inputs[0], self.elapsed_time, inputs[1], inputs[2])

    def end_match(self):
        """
        End the match, determine the winner based on the score, and stop the game loop.

        Returns
        -------
        bool
            True if the match ends successfully.
        """
        # TODO: has  to return all the stats to the
        # Determine the winner based on the score
        if self.score[0] > self.score[1]:
            self.match_stats.set_winner(self.p1.name)
        elif self.score[0] < self.score[1]:
            self.match_stats.set_winner(self.p2.name)

        # Stop the game loop
        self.playing = False
        return True

    def get_match_stats(self):
        """
        Retrieve the match statistics.

        Returns
        -------
        tuple
            A tuple containing match statistics.
        """
        return self.match_stats.get_stats_tuple()

    def share_state(self):
        """
        Share the current state of the match.

        Returns
        -------
        list
            A list containing various elements of the match's current state.
        """
        return [self.remaining_time, self.score[0], self.score[1],
                self.p1.name, self.p2.name,
                self.p1.x, self.p1.y, self.p2.x, self.p2.y, self.p1.hook_coords.x,
                self.p1.hook_coords.y,
                self.p2.hook_coords.x, self.p2.hook_coords.y, self.dash_time_1,
                self.hook_time_1, self.dash_time_2, self.hook_time_2,
                self.ball.x, self.ball.y, self.p1.hooking, self.p2.hooking, self.tiebreak]

    def match_loop(self):
        """
        The main game loop for the match, handling state updates and match termination conditions.

        Returns
        -------
        bool
            False if the match continues, True if the match ends.
        """
        # main game loop
        self.update_game_state()
        # Update the timer
        # Convert milliseconds to seconds
        self.elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000
        if self.elapsed_time >= self.match_duration and self.score[0] == self.score[1]:
            self.tiebreak = True
            if self.end_game_in_tiebreak:
                return self.end_match()
        elif self.elapsed_time >= self.match_duration and self.score[0] != self.score[1]:
            return self.end_match()

        return False
