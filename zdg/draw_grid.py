from zdg.settings import START_X, START_Y, BLOCK_SIZE
from zdg.util import get_first_n_zeckendorf_terms
import pygame
from zdg.font_settings import AXIS_FONT, AXIS_COLOR
from zdg.draw_circle import DrawCircle
from zdg.grid import Grid


class DrawGrid:
    """
    Takes in a Grid Object and draws the grid
    """

    def __init__(self, grid: Grid, screen: pygame.Surface):
        self.grid = grid
        self.screen = screen
        self.draw_grid()
        self.draw_labels()
        self.draw_circles()

    def draw_grid(self):
        end_x, end_y = START_X + self.grid.width * BLOCK_SIZE, START_Y + self.grid.height * BLOCK_SIZE

        for x, x_pos in enumerate(range(START_X, end_x, BLOCK_SIZE)):
            for y, y_pos in enumerate(range(START_Y, end_y, BLOCK_SIZE)):
                rect = pygame.Rect(x_pos, y_pos, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(self.screen, 'black', rect, 1)
                self.grid.array[y][x].set_rect_obj(rect)

    def draw_labels(self):
        end_x, end_y = START_X + self.grid.width * BLOCK_SIZE, START_Y + self.grid.height * BLOCK_SIZE
        self.draw_x_labels(end_x, end_y)
        self.draw_y_labels(end_x, end_y)

    def place_label(self, curr_num: str, x: int, y: int):
        font_w, font_h = AXIS_FONT.size(curr_num)

        coordinates = x + (BLOCK_SIZE - font_w) // 2, y + (BLOCK_SIZE - font_h) // 2

        img = AXIS_FONT.render(curr_num, True, AXIS_COLOR)
        self.screen.blit(img, coordinates)

    def draw_x_labels(self, end_x, end_y):
        fib_numbers = get_first_n_zeckendorf_terms(self.grid.width)[::-1]
        for ind, x in enumerate(range(START_X, end_x, BLOCK_SIZE)):
            self.place_label(str(fib_numbers[ind]), x, end_y)

    def draw_y_labels(self, end_x, end_y):
        fib_numbers = get_first_n_zeckendorf_terms(self.grid.height)[::-1]
        for ind, y in enumerate(range(START_Y, end_y, BLOCK_SIZE)):
            self.place_label(str(fib_numbers[ind]), end_x, y)

    def draw_circles(self):
        end_x, end_y = START_X + self.grid.width * BLOCK_SIZE, START_Y + self.grid.height * BLOCK_SIZE

        for x, x_pos in enumerate(range(START_X, end_x, BLOCK_SIZE)):
            for y, y_pos in enumerate(range(START_Y, end_y, BLOCK_SIZE)):
                cell = self.grid.array[y][x]

                if cell.solution:
                    dc = DrawCircle(cell=cell, screen=self.screen, colour=pygame.Color(0, 50, 0))
                    dc.draw_circle_in_cell(solution=True)

                if cell.value == 1 and cell.solution:
                    colour = 'yellow'
                else:
                    colour = 'red'

                dc = DrawCircle(cell, self.screen, colour=colour)
                dc.draw_circle_in_cell()
