"""
Main Module
-----------

Main top-level script that runs the client.
"""
from game import Game
from configuration_mod import Config

# pylint: disable=too-few-public-methods
class Client:
    """
    Main client class for initializing and running the game client.

    Attributes
    ----------
    config : Config
        Configuration settings for the game.
    game : Game
        The main game instance.
    """
    def __init__(self) -> None:
        self.config = Config()
        self.game = Game(config=self.config.config)

    def main_lopp(self):
        """client side loop
        """

        while self.game.running:
            self.game.curr_menu.display_menu()
            response = self.game.response
            if response is not None and response["flag"] == "game_state_1":
                self.game.status = "ingame"
                self.game.start_match(response["data"])
                self.game.play_match = False

            if self.game.play_match is True:
                server_reply = self.game.net.send(
                    self.game.parse_data("queued_solo", ["no_data"]))
                self.game.status = "Waiting_for_opponent"
                self.game.play_match = False
                if server_reply["flag"] == "game_state_1":
                    self.game.status = "ingame"
                    self.game.start_match(server_reply["data"])
                    self.game.play_match = False


if __name__ == "__main__":
    CLIENT = Client()
    CLIENT.main_lopp()
