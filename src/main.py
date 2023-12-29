"""Main top-level script that runs the client.
"""
from game import Game
from configuration_mod import Config

def main():
    """client side loop
    """
    config = Config()
    g = Game(config = config.config)

    while g.running:
        g.curr_menu.display_menu()
        print("HERE")
        if g.play_match is True:
            g.start_match()
        g.game_loop()

if __name__ == "__main__":
    main()
