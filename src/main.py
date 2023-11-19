from game import Game

g = Game()

while g.running:
    g.curr_menu.display_menu()
    if(g.play_match == True):
        g.start_match()
    g.game_loop()