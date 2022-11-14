import pygame
from settings import START_X, START_Y, BLOCK_SIZE


class Grid:
    def __init__(self, screen, grid_width, grid_height):
        self.screen = screen
        self.grid_width = grid_width
        self.grid_height = grid_height

        self.array = [[Cell(value=0) for _ in range(self.grid_width)] for _ in range(self.grid_height)]

    def draw_grid(self):
        end_x, end_y = START_X + self.grid_width * BLOCK_SIZE, START_Y + self.grid_height * BLOCK_SIZE
        for x, x_pos in enumerate(range(START_X, end_x, BLOCK_SIZE)):
            for y, y_pos in enumerate(range(START_Y, end_y, BLOCK_SIZE)):
                rect = pygame.Rect(x_pos, y_pos, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(self.screen, 'black', rect, 1)
                self.array[y][x].set_rect_obj(rect)

    def is_valid_move(self, cell_x: int, cell_y: int, direction: str) -> bool:
        """
        Computes if the move is valid
        Args:
            cell_x: x index location of array
            cell_y: y index location of array
            direction: 'DOWN', 'UP', 'LEFT', 'RIGHT'

        Returns: boolean if the move was valid
        """
        # todo confirm that the bottom left is self.width, self.height and not 0,0
        if direction == 'LEFT':
            if cell_x == self.grid_width:
                # special case
                return self.array[cell_y][cell_x].value > 1
            return self.array[cell_y][cell_x + 1].value > 1

        if direction == 'RIGHT':
            return cell_x != self.grid_width

        if direction == 'DOWN':
            return cell_y != self.grid_height

        if direction == 'UP':
            if cell_y == self.grid_height:
                # special case
                return self.array[cell_y][cell_x].value > 1
            else:
                return self.array[cell_y + 1][cell_x].value > 1

    def move(self, cell_x: int, cell_y: int, direction: str) -> bool:
        """
        Change the board position based on the move.
        Args:
            cell_x: x index location of array
            cell_y: y index location of array
            direction: 'DOWN', 'UP', 'LEFT', 'RIGHT'

        Returns: boolean if the move was valid

        """
        if not self.is_valid_move(cell_x, cell_y, direction):
            return False

        if direction == 'LEFT':
            if cell_x == self.grid_width:
                # special case
                if self.array[cell_y][cell_x].value > 1:
                    self.array[cell_y][cell_x].change_value(-2)
                    self.array[cell_y][cell_x - 1].change_value(1)
            self.array[cell_y][cell_x].change_value(-1)
            self.array[cell_y][cell_x+1].change_value(-1)
            self.array[cell_y][cell_x-1].change_value(1)

        if direction == 'RIGHT':
            if cell_x == self.grid_width - 1:
                self.array[cell_y][cell_x].change_value(-1)
                self.array[cell_y][cell_x+1].change_value(2)
            else:
                self.array[cell_y][cell_x].change_value(-1)
                self.array[cell_y][cell_x + 1].change_value(1)
                self.array[cell_y][cell_x + 2].change_value(1)

        if direction == 'DOWN':
            if cell_y == self.grid_height - 1:
                self.array[cell_y][cell_x].change_value(-1)
                self.array[cell_y - 1][cell_x].change_value(2)
            else:
                self.array[cell_y][cell_x].change_value(-1)
                self.array[cell_y - 1][cell_x].change_value(1)
                self.array[cell_y - 2][cell_x].change_value(1)
            return cell_y != self.grid_height

        if direction == 'UP':
            if cell_y == self.grid_height:
                # special case
                if self.array[cell_y][cell_x].value > 1:
                    self.array[cell_y][cell_x].change_value(-2)
                    self.array[cell_y-1][cell_x].change_value(1)
            else:
                self.array[cell_y+1][cell_x].change_value(1)
                self.array[cell_y][cell_x].change_value(-1)
                self.array[cell_y-1][cell_x].change_value(-1)
        return True


class Cell:
    def __init__(self, value):
        self.value = value
        self.rect_obj = None
        self.ls_circle_obj = []

    def change_value(self, add=1):
        self.value += add

    def set_rect_obj(self, rect_obj):
        self.rect_obj = rect_obj

    def draw_circle(self, screen):
        if self.value == 0:
            return
        elif self.value == 1:
            center_pos = self.rect_obj.center

            circle_obj = pygame.draw.circle(screen, 'red', center_pos,  0.6 * BLOCK_SIZE / 2)
            self.ls_circle_obj.append(circle_obj)

        # todo implement 2 circles
        else:
            raise NotImplementedError
