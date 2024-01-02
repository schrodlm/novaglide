"""Main top-level script that runs the client.
"""
from game import Game
from configuration_mod import Config

class Client:
    def __init__(self) -> None:
        self.config = Config()
        self.g = Game(config = self.config.config)

    def main_lopp(self):
        """client side loop
        """
        while self.g.running:
            self.g.curr_menu.display_menu()
            #TODO: to be moved to the server side
            if self.g.play_match is True:
                self.g.start_match()

if __name__ == "__main__":
    client = Client()
    client.main_lopp()
