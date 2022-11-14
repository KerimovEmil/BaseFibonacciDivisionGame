# Welcome to Fibonacci Game
# 2 options (can move up and down then enter to select or click on it)
# 	- Start Game
# 	- Tutorial
# Change screen after that
# show grid of cells and move counter
# Top-right corner: Move counter


# Change screen color to black on Click
# show the number 7 on click
# on "q" keypress, close the program
# when clicking at particular location, say "clicked at location"

import pygame
import pygame_menu
from game import Game

from settings import TITLE, background_colour, WINDOW_WIDTH, WINDOW_HEIGHT

SKIP_MENU = True


class Window:
    def build_window(self):
        self.initialize_screen()
        self.build_menu()

    def initialize_screen(self):
        pygame.init()
        
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.screen.fill(background_colour)
        pygame.display.flip()

    def start_the_game(self):
        g = Game(self)
        g.build_initial_game_grid()

    def set_difficulty(self, value, difficulty):
        self.difficulty = value

    def build_menu(self):
        menu = pygame_menu.Menu('Base Fibonacci Division Game', WINDOW_WIDTH, WINDOW_HEIGHT,
                                theme=pygame_menu.themes.THEME_BLUE)
        menu.add.text_input('Name :', default='John Doe')
        menu.add.selector('Difficulty :', [('Hard', 1), ('Medium', 2), ('Easy', 3)], onchange=self.set_difficulty)
        play_button = menu.add.button('Play', self.start_the_game)
        menu.add.button('Quit', pygame_menu.events.EXIT)

        if SKIP_MENU:
            menu.mainloop(self.screen, disable_loop=True)
            self.start_the_game()
        else:
            menu.mainloop(self.screen)


if __name__ == '__main__':
    w = Window()
    w.build_window()
