from play_sound import PlaySound
class Move:

    def __init__(self, grid, cell_x: int, cell_y: int, direction: str) -> None:
        """
        Change the board position based on the move.
        Args:
            cell_x: x index location of array
            cell_y: y index location of array
            direction: 'DOWN', 'UP', 'LEFT', 'RIGHT'

        Returns: boolean if the move was valid

        """
        self.grid = grid
        self.cell_x = cell_x  # x index of cell in array
        self.cell_y = cell_y  # y index of cell in array
        self.direction = direction

        self.direction_handler = {
            "LEFT": self.move_left,
            "RIGHT": self.move_right,
            "UP": self.move_up,
            "DOWN": self.move_down
        }

    @property
    def array(self):
        return self.grid.array

    def is_valid(self, cell_x: int, cell_y: int, direction: str) -> bool:
        """
        Computes if the move is valid
        Args:
            cell_x: x index location of array
            cell_y: y index location of array
            direction: 'DOWN', 'UP', 'LEFT', 'RIGHT'

        Returns: boolean if the move was valid
        """
        if direction == 'LEFT':
            if cell_x == (self.grid.width - 1):
                # special case
                return self.array[cell_y][cell_x].value > 1
            return self.array[cell_y][cell_x + 1].value >= 1

        if direction == 'RIGHT':
            return cell_x != (self.grid.width - 1)

        if direction == 'DOWN':
            return cell_y != (self.grid.height - 1)

        if direction == 'UP':
            if cell_y == (self.grid.height - 1):
                # special case
                return self.array[cell_y][cell_x].value > 1
            else:
                return self.array[cell_y + 1][cell_x].value >= 1

    def make_move(self) -> bool:
        """Directly modifies the grid object and returns weather the move was performed successfully"""
        if not self.is_valid(self.cell_x, self.cell_y, self.direction):
            print('move was not valid')
            # s = Sound(False)
            s = PlaySound("INVALID_MOVE")
            return False

        self.direction_handler[self.direction]()
        s = PlaySound("VALID_MOVE")
        return True

    def move_left(self):
        if self.cell_x == (self.grid.width - 1):
            # special case
            if self.array[self.cell_y][self.cell_x].value > 1:
                self.array[self.cell_y][self.cell_x].change_value(-2)
                self.array[self.cell_y][self.cell_x - 1].change_value(1)
        else:
            self.array[self.cell_y][self.cell_x].change_value(-1)
            self.array[self.cell_y][self.cell_x + 1].change_value(-1)
            self.array[self.cell_y][self.cell_x - 1].change_value(1)

    def move_right(self):
        if self.cell_x == (self.grid.width - 2):  # second last row
            self.array[self.cell_y][self.cell_x].change_value(-1)
            self.array[self.cell_y][self.cell_x + 1].change_value(2)
        else:
            self.array[self.cell_y][self.cell_x].change_value(-1)
            self.array[self.cell_y][self.cell_x + 1].change_value(1)
            self.array[self.cell_y][self.cell_x + 2].change_value(1)

    def move_up(self):
        if self.cell_y == (self.grid.height - 1):
            # special case
            if self.array[self.cell_y][self.cell_x].value > 1:
                self.array[self.cell_y][self.cell_x].change_value(-2)
                self.array[self.cell_y - 1][self.cell_x].change_value(1)
        else:
            self.array[self.cell_y - 1][self.cell_x].change_value(1)
            self.array[self.cell_y][self.cell_x].change_value(-1)
            self.array[self.cell_y + 1][self.cell_x].change_value(-1)

    def move_down(self):
        if self.cell_y == (self.grid.height - 2):  # second last row
            self.array[self.cell_y][self.cell_x].change_value(-1)
            self.array[self.cell_y + 1][self.cell_x].change_value(2)
        else:
            self.array[self.cell_y][self.cell_x].change_value(-1)
            self.array[self.cell_y + 1][self.cell_x].change_value(1)
            self.array[self.cell_y + 2][self.cell_x].change_value(1)
