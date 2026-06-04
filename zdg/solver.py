"""Breadth-first solver: finds a shortest sequence of moves to the solution.

The state space is small for the difficulty ranges we generate, so plain BFS with
a visited set and a node cap returns a provably-shortest path quickly.
"""
from collections import deque
from zdg import rules
from zdg.grid import is_win_state
from zdg.settings import SOLVER_MAX_NODES


def _as_tuple(state):
    return tuple(tuple(row) for row in state)


def solve(start_state, mask, max_nodes=SOLVER_MAX_NODES):
    """Return a shortest list of (row, col, direction) moves, or None.

    ``mask`` is the solution mask (tuple of tuple of bool).
    """
    start = _as_tuple(start_state)
    if is_win_state(start, mask):
        return []

    visited = {start}
    # queue holds (state, path)
    queue = deque([(start, [])])
    nodes = 0

    while queue:
        state, path = queue.popleft()
        for (r, c, d) in rules.legal_moves(state):
            nxt = _as_tuple(rules.apply(state, r, c, d))
            if nxt in visited:
                continue
            new_path = path + [(r, c, d)]
            if is_win_state(nxt, mask):
                return new_path
            visited.add(nxt)
            queue.append((nxt, new_path))
            nodes += 1
            if nodes >= max_nodes:
                return None
    return None


def hint(start_state, mask, max_nodes=SOLVER_MAX_NODES):
    """The first move of an optimal solution, or None if unsolvable/solved."""
    path = solve(start_state, mask, max_nodes)
    if not path:
        return None
    return path[0]


def optimal_length(start_state, mask, max_nodes=SOLVER_MAX_NODES):
    path = solve(start_state, mask, max_nodes)
    return None if path is None else len(path)
