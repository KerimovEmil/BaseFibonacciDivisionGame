import pygame
from zdg.game import Game
from zdg.first_screen import FirstScreen
from zdg.settings import TITLE, BG_COLOR, WINDOW_WIDTH, WINDOW_HEIGHT, SKIP_MENU, GAME_ICON_PATH


class Window:
    def __init__(self):
        self.screen = self.initialize_screen()
        self.difficulty = None
        self.first_screen = FirstScreen(window=self, screen=self.screen, skip=SKIP_MENU)

    @staticmethod
    def initialize_screen():
        pygame.init()
        game_icon = pygame.image.load(GAME_ICON_PATH)
        pygame.display.set_icon(game_icon)

        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(TITLE)
        screen.fill(BG_COLOR)
        pygame.display.flip()
        return screen

    def start_the_game(self):
        g = Game(self)
        g.start_game()

    def set_difficulty(self, value):
        self.difficulty = value
