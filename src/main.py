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
            response = self.g.response
            print(response)
            if response is not None and response["flag"] == "game_state_1":
                print("main_ingame")
                self.g.status = "ingame"
                self.g.start_match(response["data"])
                self.g.play_match = False

            if self.g.play_match is True:
                server_reply = self.g.net.send(self.g.parse_data("queued_solo",["no_data"]))
                self.g.status = "Waiting_for_opponent"
                self.g.play_match = False
                if server_reply["flag"] == "game_state_1":
                    self.g.status = "ingame"
                    self.g.start_match(server_reply["data"])
                    self.g.play_match = False
            
            


if __name__ == "__main__":
    client = Client()
    client.main_lopp()
