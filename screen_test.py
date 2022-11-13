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
import sys

from settings import *


class Game:
    def start_game(self):
        self.initialize_screen()
        self.build_menu()
        self.event_loop()

    def initialize_screen(self):
        pygame.init()
        self.screen = pygame.display.set_mode((game_width, game_height))
        pygame.display.set_caption(TITLE)
        self.screen.fill(background_colour)
        pygame.display.flip()

    def start_the_game(self):
        def drawGrid():
            blockSize = 20  # Set the size of the grid block
            for x in range(0, game_width, blockSize):
                for y in range(0, game_height, blockSize):
                    rect = pygame.Rect(x, y, blockSize, blockSize)
                    pygame.draw.rect(self.screen, 'black', rect, 1)

        self.screen.fill('white')

        while True:
            drawGrid()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    sys.exit()

            pygame.display.update()

    def set_difficulty(self, value, difficulty):
        self.difficulty = value

    def build_menu(self):
        menu = pygame_menu.Menu('Base Fibonacci Division Game', game_width, game_height,
                                theme=pygame_menu.themes.THEME_BLUE)
        menu.add.text_input('Name :', default='John Doe')
        menu.add.selector('Difficulty :', [('Hard', 1), ('Medium', 2), ('Easy', 3)], onchange=self.set_difficulty)
        menu.add.button('Play', self.start_the_game)
        menu.add.button('Quit', pygame_menu.events.EXIT)
        menu.mainloop(self.screen)

    def event_loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False


if __name__ == '__main__':
    g = Game()
    g.start_game()
