import pygame
import pygame_menu
from zeckendorf_div_game.game import Game

from zeckendorf_div_game.settings import TITLE, BG_COLOR, WINDOW_WIDTH, WINDOW_HEIGHT, SKIP_MENU, GAME_ICON_PATH


class Window:
    def __init__(self):
        self.initialize_screen()
        self.build_menu()

        self.screen = None
        self.difficulty = None

    def initialize_screen(self):
        pygame.init()
        game_icon = pygame.image.load(GAME_ICON_PATH)
        pygame.display.set_icon(game_icon)

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.screen.fill(BG_COLOR)
        pygame.display.flip()

    def start_the_game(self):
        g = Game(self)
        g.start_game()

    def set_difficulty(self, value, difficulty):
        self.difficulty = value

    def build_menu(self):
        menu = pygame_menu.Menu('Base Fibonacci Division Game', WINDOW_WIDTH, WINDOW_HEIGHT,
                                theme=pygame_menu.themes.THEME_BLUE)
        menu.add.text_input('Name :', default='John Doe')
        menu.add.selector('Difficulty :', [('Hard', 1), ('Medium', 2), ('Easy', 3)], onchange=self.set_difficulty)
        menu.add.button('Play', self.start_the_game)
        menu.add.button('Quit', pygame_menu.events.EXIT)

        if SKIP_MENU:
            menu.mainloop(self.screen, disable_loop=True)
            self.start_the_game()
        else:
            menu.mainloop(self.screen)
