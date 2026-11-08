"""The puzzle model: a grid of :class:`Cell` plus win logic and move application.

Rendering and input live elsewhere; this class only knows about tile values and
which cells form the target ("solution") configuration.
"""
from zdg.cell import Cell
from zdg import rules


class Grid:
    def __init__(self, width: int, height: int, problem, extreme: bool = None):
        self.width = width
        self.height = height
        self.problem = problem
        self.extreme = (
            bool(getattr(problem, "extreme", False))
            if extreme is None
            else bool(extreme)
        )
        self.fib_dividend = problem.fib_dividend
        self.fib_divisor = problem.fib_divisor
        self.fib_quotient = problem.fib_quotient

        self.array = self._build_cells()
        self._seed_last_row()
        self._mark_solution_cells()

    # ----- construction ---------------------------------------------------
    def _build_cells(self):
        return [[Cell(value=0, row=i, col=j) for j in range(self.width)]
                for i in range(self.height)]

    def _seed_last_row(self):
        for x in range(self.width):
            if self.fib_dividend[x] == '1':
                self.array[self.height - 1][x].value += 1

    def _mark_solution_cells(self):
        for x, x_bit in enumerate(self.fib_quotient[::-1]):
            for y, y_bit in enumerate(self.fib_divisor):
                if y_bit == '1' and x_bit == '1':
                    self.array[y][-1 - x].solution = True

    # ----- state access ---------------------------------------------------
    def cells(self):
        return [cell for row in self.array for cell in row]

    def non_empty_cells(self):
        return [c for c in self.cells() if c.value > 0]

    def state(self):
        """Plain 2D list of tile counts (the canonical state for rules/solver)."""
        return [[c.value for c in row] for row in self.array]

    def set_state(self, state):
        for r, row in enumerate(state):
            for c, value in enumerate(row):
                self.array[r][c].value = value

    def solution_mask(self):
        return tuple(tuple(c.solution for c in row) for row in self.array)

    def target_rows(self):
        """Tuple of row indices that belong to the divisor's Zeckendorf representation."""
        return tuple(r for r, bit in enumerate(self.fib_divisor) if bit == '1')

    def target_row_mask(self):
        """Tuple of booleans marking which rows are target rows."""
        return tuple(bit == '1' for bit in self.fib_divisor)

    def is_target_row(self, row: int) -> bool:
        return 0 <= row < len(self.fib_divisor) and self.fib_divisor[row] == '1'

    @property
    def num_solution_cells(self) -> int:
        return self.fib_divisor.count('1') * self.fib_quotient.count('1')

    # ----- moves ----------------------------------------------------------
    def apply_move(self, row, col, direction) -> bool:
        if not rules.is_valid(self.state(), row, col, direction):
            return False
        self.set_state(rules.apply(self.state(), row, col, direction))
        return True

    def legal_targets(self, row, col):
        """Adjacent cells (row, col) the tile at (row, col) may move into."""
        targets = []
        state = self.state()
        for direction in rules.DIRECTIONS:
            if rules.is_valid(state, row, col, direction):
                dr, dc = rules.DELTA[direction]
                targets.append((row + dr, col + dc))
        return targets

    # ----- win ------------------------------------------------------------
    def is_win(self) -> bool:
        if self.extreme:
            return is_extreme_win_state(self.state(), self.target_rows())
        return is_win_state(self.state(), self.solution_mask())


def is_win_state(state, mask) -> bool:
    """A win: every solution cell holds exactly 1, every other cell holds 0."""
    for r, row in enumerate(state):
        for c, value in enumerate(row):
            if mask[r][c]:
                if value != 1:
                    return False
            elif value != 0:
                return False
    return True


def _normalize_target_rows(state, target_rows):
    rows = list(target_rows)
    if not rows:
        return []
    first = rows[0]
    if isinstance(first, (list, tuple)):
        return [r for r, row_mask in enumerate(rows) if any(row_mask)]
    if all(isinstance(x, bool) for x in rows) and len(rows) == len(state):
        return [r for r, flag in enumerate(rows) if flag]
    return [int(r) for r in rows]


def is_extreme_win_state(state, target_rows) -> bool:
    """An Extreme-mode win:
    - All non-target rows hold only 0s (all pieces are in the target rows).
    - Every target row has the exact same tile arrangement.
    - Target rows contain at least one piece.
    """
    if not state:
        return False
    t_indices = _normalize_target_rows(state, target_rows)
    if not t_indices:
        return False
    t_set = set(t_indices)
    first_row = list(state[t_indices[0]])
    if sum(first_row) <= 0 or any(v < 0 for v in first_row):
        return False
    for r, row in enumerate(state):
        if r in t_set:
            if list(row) != first_row:
                return False
        else:
            if any(v != 0 for v in row):
                return False
    return True
