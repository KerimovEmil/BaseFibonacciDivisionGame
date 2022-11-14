import pygame
import sys
from settings import TITLE, background_colour, WINDOW_WIDTH, WINDOW_HEIGHT, START_X, START_Y, BLOCK_SIZE
from font_settings import AXIS_FONT
from util import get_multiplication, convert_decimal_to_base_fib, get_first_n_zeckendorf_terms
from grid import Grid


class Game:
    def __init__(self, window):
        pygame.font.init()

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
        self.grid = Grid(screen=self.screen, grid_width=self.grid_width, grid_height=self.grid_height)

        self.build_initial_game_grid()

    def draw_labels(self, grid_width, grid_height):
        end_x, end_y = START_X + grid_width * BLOCK_SIZE, START_Y + grid_height * BLOCK_SIZE
        self.draw_x_labels(end_x, end_y)
        self.draw_y_labels(end_x, end_y)

    def place_label(self, curr_num: str, x: int, y: int):
        font_w, font_h = AXIS_FONT.size(curr_num)

        coords = x + (BLOCK_SIZE - font_w) // 2, y + (BLOCK_SIZE - font_h) // 2

        img = AXIS_FONT.render(curr_num, True, 'blue')
        self.screen.blit(img, coords)

    def draw_x_labels(self, end_x, end_y):
        fib_numbers = get_first_n_zeckendorf_terms(self.grid_width)[::-1]
        for ind, x in enumerate(range(START_X, end_x, BLOCK_SIZE)):
            self.place_label(str(fib_numbers[ind]), x, end_y)

    def draw_y_labels(self, end_x, end_y):
        fib_numbers = get_first_n_zeckendorf_terms(self.grid_height)[::-1]
        for ind, y in enumerate(range(START_Y, end_y, BLOCK_SIZE)):
            self.place_label(str(fib_numbers[ind]), end_x, y)

    def populate_problem(self, grid):
        """Add the product fib on the first row"""
        print(f'product={self.prod}, fib_product={self.fib_prod}')
        end_x, end_y = START_X + grid.grid_width * BLOCK_SIZE, START_Y + grid.grid_height * BLOCK_SIZE
        for x, x_pos in enumerate(range(START_X, end_x, BLOCK_SIZE)):
            if self.fib_prod[x] == '1':
                grid.array[grid.grid_height-1][x].change_value(add=1)
                grid.array[grid.grid_height-1][x].draw_circle(screen=self.screen)

        # highlight rows based on self.fib_div
        print(f'dividend={self.div}, fib_dividend={self.fib_div}')

        for y, y_pos in enumerate(range(START_Y, end_y, BLOCK_SIZE)):
            if self.fib_div[y] == '1':
                rect = pygame.Rect(START_X, y_pos, self.grid_width * BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(self.screen, 'green', rect, 5)

    def build_initial_game_grid(self):
        self.screen.fill('white')

        self.grid.draw_grid()
        self.draw_labels(grid_width=self.grid_width, grid_height=self.grid_height)
        self.populate_problem(grid=self.grid)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    sys.exit()

            pygame.display.update()
