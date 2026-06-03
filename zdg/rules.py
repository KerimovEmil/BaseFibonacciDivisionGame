"""
Pure, side-effect-free implementation of the four Fibonacci-identity moves.

A *state* is a rectangular ``list[list[int]]`` (or tuple of tuples) of tile
counts. Row/col labels descend left->right and top->bottom, so a smaller index
means a *larger* Fibonacci number. Consecutive labels therefore satisfy
``F[i-1] == F[i] + F[i+1]``, which is what makes every move value-preserving.

Both the interactive ``Move`` class and the ``solver`` build on these functions,
so gameplay and solver can never disagree about what a legal move is.

Moves
-----
RIGHT / DOWN  -> *split* one tile into two smaller-labelled neighbours.
LEFT  / UP    -> *merge* two adjacent tiles into one larger-labelled tile.

Edge cases on the last column / bottom row use the ``2 * F == F'`` identity
(value 2 carries one tile to the larger-labelled neighbour).
"""
from typing import List, Tuple

State = List[List[int]]

DIRECTIONS = ("LEFT", "RIGHT", "UP", "DOWN")

# Unit step in (row, col) for each direction — used for animation/labels.
DELTA = {
    "LEFT": (0, -1),
    "RIGHT": (0, 1),
    "UP": (-1, 0),
    "DOWN": (1, 0),
}


def dimensions(state) -> Tuple[int, int]:
    return len(state), len(state[0])


def is_valid(state, row: int, col: int, direction: str) -> bool:
    """Return whether ``direction`` is a legal move for the tile at (row, col)."""
    height, width = dimensions(state)
    if row < 0 or col < 0 or row >= height or col >= width:
        return False
    if state[row][col] < 1:
        return False

    if direction == "LEFT":
        if col == width - 1:                     # last column: 2*F1 -> F2 carry
            return state[row][col] > 1
        if col == 0:                             # nothing larger to merge into
            return False
        return state[row][col + 1] >= 1

    if direction == "RIGHT":
        return col != width - 1                  # rightmost cannot split further

    if direction == "UP":
        if row == height - 1:                    # bottom row: 2*F1 -> F2 carry
            return state[row][col] > 1
        if row == 0:
            return False
        return state[row + 1][col] >= 1

    if direction == "DOWN":
        return row != height - 1

    return False


def apply(state, row: int, col: int, direction: str) -> State:
    """Return a NEW state with the move applied. Assumes ``is_valid`` is True."""
    height, width = dimensions(state)
    new = [list(r) for r in state]

    if direction == "LEFT":
        if col == width - 1:
            new[row][col] -= 2
            new[row][col - 1] += 1
        else:
            new[row][col] -= 1
            new[row][col + 1] -= 1
            new[row][col - 1] += 1

    elif direction == "RIGHT":
        if col == width - 2:                     # split label-2 tile into two 1s
            new[row][col] -= 1
            new[row][col + 1] += 2
        else:
            new[row][col] -= 1
            new[row][col + 1] += 1
            new[row][col + 2] += 1

    elif direction == "UP":
        if row == height - 1:
            new[row][col] -= 2
            new[row - 1][col] += 1
        else:
            new[row - 1][col] += 1
            new[row][col] -= 1
            new[row + 1][col] -= 1

    elif direction == "DOWN":
        if row == height - 2:
            new[row][col] -= 1
            new[row + 1][col] += 2
        else:
            new[row][col] -= 1
            new[row + 1][col] += 1
            new[row + 2][col] += 1

    return new


def legal_moves(state) -> List[Tuple[int, int, str]]:
    """Every legal (row, col, direction) for the given state."""
    height, width = dimensions(state)
    moves = []
    for r in range(height):
        for c in range(width):
            if state[r][c] < 1:
                continue
            for d in DIRECTIONS:
                if is_valid(state, r, c, d):
                    moves.append((r, c, d))
    return moves


def inverse(direction: str) -> str:
    """Direction that undoes ``direction`` (split <-> merge)."""
    return {"LEFT": "RIGHT", "RIGHT": "LEFT", "UP": "DOWN", "DOWN": "UP"}[direction]
