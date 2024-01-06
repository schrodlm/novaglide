from game_objects.ball import Ball
import sys

class MatchStatsData:
    def __init__(self, stats, winner):
        self.stats = stats
        self.winner = winner
class MatchStats:
    def __init__(self, entities):
        
        # Filter out the ball from the entities
        self.entities = [entity for entity in entities if not isinstance(entity, Ball)]

        # Initialize stats only for the filtered entities
        self.stats = {entity.name: {'touches': 0, 'goals': 0, 'possession_time': 0} for entity in self.entities}
        print(self.stats)
        self.winner = None


    def add_touch(self, entity):
        print("touch" + entity.name)

        if entity.name in self.stats:
            self.stats[entity.name]['touches'] += 1

    def add_goal(self, entity):

        print("goal" + entity.name)
        if entity.name in self.stats:
            self.stats[entity.name]['goals'] += 1

    def update_possession(self, entity, time):
        if entity.name in self.stats:
            self.stats[entity.name]['possession_time'] += time

    def set_winner(self, winner):
        self.winner = winner

    def get_stats(self):
        return MatchStatsData(self.stats, self.winner)
    

    def get_stats_tuple(self):
        return (self.stats, self.winner)

