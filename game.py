import pygame
import sys
from settings import TITLE, background_colour, WINDOW_WIDTH, WINDOW_HEIGHT, START_X, START_Y, BLOCK_SIZE
from util import get_multiplication, convert_decimal_to_base_fib


class Game:
    def __init__(self, window):
        self.window = window
        self.screen = window.screen

        self.div, self.quot, self.prod = get_multiplication()
        self.fib_prod = convert_decimal_to_base_fib(self.prod)
        self.fib_quot = convert_decimal_to_base_fib(self.quot)
        self.fib_div = convert_decimal_to_base_fib(self.div)
        self.grid_width = len(self.fib_prod)
        self.grid_height = len(self.fib_div)

        print(self.div, self.quot, self.prod, self.fib_div, self.fib_quot, self.fib_prod, self.grid_height,
              self.grid_width)
        self.build_initial_game_grid()

    def drawGrid(self, grid_width, grid_height):
        end_x, end_y = START_X + grid_width * BLOCK_SIZE, START_Y + grid_height * BLOCK_SIZE
        for x in range(START_X, end_x, BLOCK_SIZE):
            for y in range(START_Y, end_y, BLOCK_SIZE):
                rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(self.screen, 'black', rect, 1)

    def draw_labels(self, grid_width, grid_height):
        end_x, end_y = START_X + grid_width * BLOCK_SIZE, START_Y + grid_height * BLOCK_SIZE
        pass

    def populate_problem(self, grid_width, grid_height):
        end_x, end_y = START_X + grid_width * BLOCK_SIZE, START_Y + grid_height * BLOCK_SIZE
        for x in range(START_X, end_x, BLOCK_SIZE):
            for y in range(START_Y, end_y, BLOCK_SIZE):
                if x == y:
                    pygame.draw.circle(self.screen, 'red', (x + BLOCK_SIZE / 2, y + BLOCK_SIZE / 2), 0.6 * BLOCK_SIZE / 2)

    def build_initial_game_grid(self):
        while True:
            self.screen.fill('white')
            self.drawGrid(grid_width=self.grid_width, grid_height=self.grid_height)
            self.draw_labels(grid_width=self.grid_width, grid_height=self.grid_height)
            self.populate_problem(grid_width=self.grid_width, grid_height=self.grid_height)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    sys.exit()

            pygame.display.update()
