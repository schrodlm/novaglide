import numpy as np
from random import randint
from typing import Tuple

class Elo:
    """
    Elo rating calculation for a two-player game.

    Attributes
    ----------
    BASELINE : int
        The baseline Elo value used in the calculation.
    SCALING_FACTOR : float
        Scaling factor applied to the Elo difference.
    COMPUTATIONAL_STABILITY : float
        A small value added to prevent log(0) in the calculation.

    Methods
    -------
    calculate_elo(player_1_elo: int, player_2_elo: int, winner: bool)
        Calculate the new Elo ratings for two players after a game.

    Raises
    ------
    TypeError
        If player_1_elo or player_2_elo is not integer or if winner is not bool.
    """
    BASELINE = 40
    # prevents 0 in log
    SCALING_FACTOR = 1/50
    COMPUTATIONAL_STABILITY = 0.00001

    @staticmethod
    def calculate_elo(player_1_elo: int, player_2_elo: int, winner: bool) -> Tuple[int,int]:
        """
        Calculate the new Elo ratings for two players after a game.

        Parameters
        ----------
        player_1_elo : int
            Elo rating of Player 1.
        player_2_elo : int
            Elo rating of Player 2.
        winner : bool
            True if Player 1 won, False if Player 2 won.

        Returns
        -------
        Tuple[int, int]
            A tuple containing the new Elo ratings for Player 1 and Player 2.
        """
        if not isinstance(player_1_elo, int) or not isinstance(player_2_elo, int):
            raise TypeError("Both player elos need to be integers")
        if not isinstance(winner, bool):
            raise TypeError("Winner has to be true or false")
        elo_difference = np.abs(int(player_1_elo) - int(player_2_elo))
        result = int(Elo.BASELINE + (elo_difference*Elo.SCALING_FACTOR) +
                     np.log((elo_difference + Elo.COMPUTATIONAL_STABILITY)))

        # player 1 won
        if winner:
            return (int(player_1_elo + result), int(player_2_elo - result))
        # player 2 won
        else:
            return (int(player_1_elo - result), int(player_2_elo + result))


if __name__ == "__main__":
    # simple simulation what does the elo return
    for _ in range(1000):
        a = randint(500, 7000)
        b = randint(500, 7000)
        winner = randint(1, 2)
        new_elo = Elo.calculate_elo(a, b, winner)
        print(f"Player 1: {a}, Player 2: {b}, Winner {winner} new elo{new_elo}, ammount: {np.abs(a - new_elo[0])}")
