import numpy as np 
from random import randint
class Elo:
    BASELINE = 40
    # prevents 0 in log
    SCALING_FACTOR = 1/50
    COMPUTATIONAL_STABILITY = 0.00001
    @staticmethod    
    def calculate_elo(player_1_elo: int, player_2_elo: int, winner: bool):
        elo_difference = np.abs(int(player_1_elo) - int(player_2_elo))
        result = int(Elo.BASELINE + (elo_difference*Elo.SCALING_FACTOR) + np.log((elo_difference+ Elo.COMPUTATIONAL_STABILITY)))
        
        #player 1 won
        if winner:
            return (int(player_1_elo + result), int(player_2_elo - result))
        #player 2 won
        else:
            return (int(player_1_elo - result), int(player_2_elo + result))

if __name__ == "__main__":
    #simple simulation what does the elo return
    for _ in range (1000):
        a = randint(500,7000)
        b = randint(500,7000)
        winner = randint(1,2)
        new_elo = Elo.calculate_elo(a, b, winner)
        print(f"Player 1: {a}, Player 2: {b}, Winner {winner} new elo{new_elo}, ammount: {np.abs(a - new_elo[0])}")