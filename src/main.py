"""_summary_
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
        if g.play_match is True:
            g.start_match()
        g.game_loop()

if __name__ == "__main__":
    main()
