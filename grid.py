from settings import START_X, START_Y, BLOCK_SIZE, DEBUG_MODE
from cell import Cell
from pygame import Surface


class Grid:
    def __init__(self, screen: Surface, width: int, height: int, problem):
        self.screen = screen
        self.width = width
        self.height = height
        # self.last_row = last_row
        self.fib_dividend = problem.fib_dividend
        self.fib_divisor = problem.fib_divisor
        self.fib_quotient = problem.fib_quotient

        self.end_x = START_X + self.width * BLOCK_SIZE
        self.end_y = START_Y + self.height * BLOCK_SIZE

        self.array = self.build_initial_array_of_cells()
        self.populate_initial_state_of_last_row()
        self.populate_solution()

        if DEBUG_MODE:
            self.print()

    def num_solution_cells(self) -> int:
        """Return number of solution cells"""
        return self.fib_divisor.count('1') * self.fib_quotient.count('1')

    def is_win(self):
        """Returns if the position is a win"""
        ls_non_empty = self.non_empty_cells()

        if len(ls_non_empty) != self.num_solution_cells:
            return False

        for cell in ls_non_empty:
            if (cell.value != 1) or (not cell.solution):
                return False
        return True

    def print(self):
        for row in self.array:
            for cell in row:
                print(cell.value, end="")
            print()

    def build_initial_array_of_cells(self):
        return [[Cell(value=0, grid_row_pos=i, grid_col_pos=j) for j in range(self.width)] for i in range(self.height)]

    def populate_initial_state_of_last_row(self):
        for x, x_pos in enumerate(range(START_X, self.end_x, BLOCK_SIZE)):
            if self.fib_dividend[x] == '1':
                self.array[self.height - 1][x].change_value(add=1)

    def populate_solution(self):
        for x, x_pos in enumerate(self.fib_quotient[::-1]):
            for y, y_pos in enumerate(self.fib_divisor):
                if y_pos == '1' and x_pos == '1':
                    cell = self.array[y][-1 - x]
                    cell.solution = True

    def cells(self):
        return [cell for row in self.array for cell in row]

    def non_empty_cells(self):
        res = []
        for cell in self.cells():
            if cell.value > 0:
                res.append(cell)
        return res
