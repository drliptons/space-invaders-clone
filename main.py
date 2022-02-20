from game import Game
from main_menu import MainMenu
from game_play import GamePlay
from credit import Credit


game = Game('ALIEN INVADERS', 800, 800)
main_menu = MainMenu(game)
game_play = GamePlay(game.screen)
credit = Credit(game.screen)

# Add scene to main menu
main_menu.gameplay_scene = game_play
main_menu.credit_scene = credit

# Add main menu to other scene
game_play.main_menu = main_menu
credit.main_menu = main_menu

# Run game
game.run(main_menu)
