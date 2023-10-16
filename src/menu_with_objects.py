#import GameInitializer
from menu_initializer import GameInitializer
import os
#init GameInitializer
game = GameInitializer()
os.chdir(os.path.dirname(os.path.abspath(__file__)))

#run game
game.load_resources()
game.start_app()