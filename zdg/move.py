from zdg.play_sound import PlaySound


class Move:

    def __init__(self, grid, col: int, row: int, direction: str) -> None:
        """
        Change the board position based on the move.
        Args:
            col: x index location of array
            row: y index location of array
            direction: 'DOWN', 'UP', 'LEFT', 'RIGHT'

        Returns: boolean if the move was valid

        """
        self.grid = grid
        self.col = col  # x index of cell in array
        self.row = row  # y index of cell in array
        self.direction = direction

        self.direction_handler = {
            "LEFT": self.move_left,
            "RIGHT": self.move_right,
            "UP": self.move_up,
            "DOWN": self.move_down
        }

    def __repr__(self):
        move_output = {
            "LEFT": (-1, 0),
            "RIGHT": (1, 0),
            "UP": (0, -1),
            "DOWN": (0, 1),
        }

        a = f"Moved {self.direction} "
        b = f"from ({self.row},{self.col})"

        row_move, col_move = move_output[self.direction]
        c = f"to ({self.row + row_move},{self.col + col_move})"
        return a + b + c

    @property
    def array(self):
        return self.grid.array

    def is_valid(self, col: int, row: int, direction: str) -> bool:
        """
        Computes if the move is valid
        Args:
            col: x index location of array
            row: y index location of array
            direction: 'DOWN', 'UP', 'LEFT', 'RIGHT'

        Returns: boolean if the move was valid
        """
        if direction == 'LEFT':
            if col == (self.grid.width - 1):
                # special case
                return self.array[row][col].value > 1
            return self.array[row][col + 1].value >= 1

        if direction == 'RIGHT':
            return col != (self.grid.width - 1)

        if direction == 'DOWN':
            return row != (self.grid.height - 1)

        if direction == 'UP':
            if row == (self.grid.height - 1):
                # special case
                return self.array[row][col].value > 1
            else:
                return self.array[row + 1][col].value >= 1

    def make_move(self) -> bool:
        """Directly modifies the grid object and returns weather the move was performed successfully"""
        if not self.is_valid(self.col, self.row, self.direction):
            print('move was not valid')
            PlaySound("INVALID_MOVE")
            return False

        self.direction_handler[self.direction](self.row, self.col)
        PlaySound("VALID_MOVE")
        print(self)
        return True

    def move_left(self, r: int, c: int):
        if c == (self.grid.width - 1):
            # special case
            if self.array[r][c].value > 1:
                self.array[r][c].change_value(-2)
                self.array[r][c - 1].change_value(1)
        else:
            self.array[r][c].change_value(-1)
            self.array[r][c + 1].change_value(-1)
            self.array[r][c - 1].change_value(1)

    # any use or not?
    # change_value
    def change_value(self, r: int, c: int, value: int):
        self.array[r][c].change_value(value)

    def move_right(self, r: int, c: int):
        if self.col == (self.grid.width - 2):  # second last row
            self.array[r][c].change_value(-1)
            self.array[r][c + 1].change_value(2)
        else:
            self.array[r][c].change_value(-1)
            self.array[r][c + 1].change_value(1)
            self.array[r][c + 2].change_value(1)

    def move_up(self, r: int, c: int):
        if self.row == (self.grid.height - 1):
            # special case
            if self.array[r][c].value > 1:
                self.array[r][c].change_value(-2)
                self.array[r - 1][c].change_value(1)
        else:
            self.array[r - 1][c].change_value(1)
            self.array[r][c].change_value(-1)
            self.array[r + 1][c].change_value(-1)

    def move_down(self, r: int, c: int):
        if self.row == (self.grid.height - 2):  # second last row
            self.array[r][c].change_value(-1)
            self.array[r + 1][c].change_value(2)
        else:
            self.array[r][c].change_value(-1)
            self.array[r + 1][c].change_value(1)
            self.array[r + 2][c].change_value(1)
