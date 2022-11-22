from settings import TITLE, BG_COLOR, WINDOW_WIDTH, WINDOW_HEIGHT, START_X, START_Y, BLOCK_SIZE
from util import convert_decimal_to_base_fib, get_first_n_zeckendorf_terms
import pygame
from pygame.locals import * 
from font_settings import AXIS_FONT

class DrawGrid:
    """
    Takes in a Grid Object and draws the grid

    """
    def __init__(self,grid:'Grid',screen:'Screen'):
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

       coords = x + (BLOCK_SIZE - font_w) // 2, y + (BLOCK_SIZE - font_h) // 2

       img = AXIS_FONT.render(curr_num, True, 'blue')
       self.screen.blit(img, coords)

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
                if cell.value == 1:
                    self.draw_circle_in_cell(cell)
    
    def draw_circle_in_cell(self,cell):
        center_pos = cell.rect_obj.center
        circle_obj = pygame.draw.circle(self.screen, 'red', center_pos,  0.6 * BLOCK_SIZE / 2)
        cell.ls_circle_obj.append(circle_obj)


