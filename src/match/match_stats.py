"""
MatchStats Module
-----------------

Module for the MatchStatsData class, encapsulating match statistics and winner information in a game environment.
"""
import pygame

from game_objects.ball import Ball
from game_objects.player import Player

# pylint: disable=too-few-public-methods
class MatchStats:
    """
    Class for managing match statistics.

    Attributes
    ----------
    entities : list
        A list containing Player entities in the match.
    stats : dict
        A dictionary containing statistics for each entity in the match.
    winner : str
        The name of the winner entity.

    Parameters
    ----------
    entities : pygame.sprite.Group
        A group containing Player and Ball entities in the match.

    Raises
    ------
    TypeError
        If entities in the group are not instances of Player or Ball.
    """
    def __init__(self, entities: pygame.sprite.Group):
        for entity in entities:
            if not isinstance(entity, (Player, Ball)):
                raise TypeError("Entities must be Player or Ball")

        # Filter out the ball from the entities
        self.entities = [
            entity for entity in entities if not isinstance(entity, Ball)]

        # Initialize stats only for the filtered entities
        self.stats = {entity.name: {'touches': 0, 'goals': 0,
                                    'possession_time': 0, 'elo': 0} for entity in self.entities}
        self.winner = None

    def set_elo(self, entity: Player):
        """
        Set the Elo rating for a given entity.

        Parameters
        ----------
        entity : Player
            The entity for which to set the Elo rating.
        """
        if entity.name in self.stats:
            self.stats[entity.name]['elo'] = entity.elo

    def add_touch(self, entity: Player):
        """
        Increment the touch count for a given entity.

        Parameters
        ----------
        entity : Player
            The entity for which to increment the touch count.
        """
        if entity.name in self.stats:
            self.stats[entity.name]['touches'] += 1

    def add_goal(self, entity: Player):
        """
        Increment the goal count for a given entity.

        Parameters
        ----------
        entity : Player
            The entity for which to increment the goal count.
        """
        if entity.name in self.stats:
            self.stats[entity.name]['goals'] += 1

    def set_winner(self, winner: str):
        """
        Set the winner of the match.

        Parameters
        ----------
        winner : str
            The name of the winning entity.
        """
        self.winner = winner

    def get_stats_tuple(self):
        """
        Get match statistics as a tuple.

        Returns
        -------
        tuple
            A tuple containing match statistics dictionary and the winner's name.
        """
        return (self.stats, self.winner)
