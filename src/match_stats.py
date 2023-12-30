from ball import Ball

class MatchStats:
    def __init__(self, entities):
        
        # Filter out the ball from the entities
        self.entities = [entity for entity in entities if not isinstance(entity, Ball)]

        # Initialize stats only for the filtered entities
        self.stats = {entity: {'touches': 0, 'goals': 0, 'possession_time': 0} for entity in self.entities}
        self.winner = None

    def add_touch(self, entity):
        if entity in self.stats:
            self.stats[entity]['touches'] += 1

    def add_goal(self, entity):
        if entity in self.stats:
            self.stats[entity]['goals'] += 1

    def update_possession(self, entity, time):
        if entity in self.stats:
            self.stats[entity]['possession_time'] += time

    def set_winner(self, winner):
        self.winner = winner

    def get_stats(self):
        return self.stats, self.winner

