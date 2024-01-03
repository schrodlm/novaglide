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
        waiting = False
        while self.g.running:
            if waiting is False:
                self.g.curr_menu.display_menu()
            if self.g.play_match is True:
                server_reply = self.g.net.send(self.g.parse_data("queued_solo",["no_data"]))
                if server_reply["flag"] == "game_started":
                    self.g.status = "ingame"
                    self.g.start_match(server_reply["data"])
                    self.g.play_match = False
                if server_reply["flag"] == "waiting_for_opponents":
                    waiting = True
if __name__ == "__main__":
    client = Client()
    client.main_lopp()
