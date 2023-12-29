"""_summary_
"""
from game import Game
from config import Config

def main():
    """_summary_
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
