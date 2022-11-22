from settings import START_X, START_Y, BLOCK_SIZE, DEBUG_MODE
from typing import List
from cell import Cell
from pygame import Surface


class Grid:
    def __init__(self, screen: Surface, width: int, height: int, last_row: List[int]):
        self.screen = screen
        self.width = width
        self.height = height
        self.last_row = last_row

        self.end_x = START_X + self.width * BLOCK_SIZE
        self.end_y = START_Y + self.height * BLOCK_SIZE

        self.array = self.build_initial_array_of_cells()
        self.populate_initial_state_of_last_row()

        if DEBUG_MODE:
            self.print()

    def print(self):
        for row in self.array:
            for cell in row:
                print(cell.value, end="")
            print()

    def build_initial_array_of_cells(self):
        return [[Cell(value=0) for _ in range(self.width)] for _ in range(self.height)]

    def populate_initial_state_of_last_row(self):
        for x, x_pos in enumerate(range(START_X, self.end_x, BLOCK_SIZE)):
            if self.last_row[x] == '1':
                self.array[self.height - 1][x].change_value(add=1)

    def cells(self):
        return [cell for row in self.array for cell in row]

    def non_empty_cells(self):
        res = []
        for cell in self.cells():
            if len(cell.ls_circle_obj) > 0:
                res.append(cell)
        return res

    def event_to_cell_positions(self, event):
        raise NotImplemented
