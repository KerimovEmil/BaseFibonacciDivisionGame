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
        """Add the product fib on the first row"""

        print(f'product={self.prod}, fib_product={self.fib_prod}')
        end_x, end_y = START_X + grid_width * BLOCK_SIZE, START_Y + grid_height * BLOCK_SIZE
        last_row_y = START_Y + grid_height * BLOCK_SIZE
        for x, x_pos in enumerate(range(START_X, end_x, BLOCK_SIZE)):
            if self.fib_prod[x] == '1':
                pygame.draw.circle(self.screen, 'red', (x_pos + BLOCK_SIZE / 2, last_row_y - BLOCK_SIZE / 2), 0.6 * BLOCK_SIZE / 2)

        # highlight rows based on self.fib_div
        print(f'dividend={self.div}, fib_dividend={self.fib_div}')

        for y, y_pos in enumerate(range(START_Y, end_y, BLOCK_SIZE)):
            if self.fib_div[y] == '1':
                # rect = pygame.Rect(START_X, y_pos, end_x, BLOCK_SIZE)
                rect = pygame.Rect(START_X, y_pos, grid_width * BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(self.screen, 'green', rect, 5)


    def build_initial_game_grid(self):
        self.screen.fill('white')
        self.drawGrid(grid_width=self.grid_width, grid_height=self.grid_height)
        self.draw_labels(grid_width=self.grid_width, grid_height=self.grid_height)
        self.populate_problem(grid_width=self.grid_width, grid_height=self.grid_height)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    sys.exit()

            pygame.display.update()
