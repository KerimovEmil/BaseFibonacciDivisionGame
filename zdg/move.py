"""
Thin wrapper around :mod:`zdg.rules` kept for backwards compatibility and for the
interactive layer. All move semantics live in ``rules`` so gameplay and the
solver share one definition.
"""
from zdg import rules


class Move:
    def __init__(self, grid, col: int, row: int, direction: str) -> None:
        self.grid = grid
        self.col = col
        self.row = row
        self.direction = direction

    def __repr__(self):
        dr, dc = rules.DELTA[self.direction]
        return (f"Moved {self.direction} from ({self.row},{self.col}) "
                f"to ({self.row + dr},{self.col + dc})")

    def is_valid(self, col: int, row: int, direction: str) -> bool:
        return rules.is_valid(self.grid.state(), row, col, direction)

    def make_move(self) -> bool:
        """Apply to the live grid; return whether it was legal."""
        return self.grid.apply_move(self.row, self.col, self.direction)
