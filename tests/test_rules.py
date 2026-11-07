import random
import unittest

from zdg import rules
from zdg.problem import Problem
from zdg.grid import Grid
from zdg.move import Move
from zdg.util import get_first_n_zeckendorf_terms


def grid_value(state):
    """Weighted total: tile at (r,c) is worth rowFib[r] * colFib[c]. Invariant."""
    h, w = len(state), len(state[0])
    col_fib = get_first_n_zeckendorf_terms(w)[::-1]
    row_fib = get_first_n_zeckendorf_terms(h)[::-1]
    return sum(state[r][c] * row_fib[r] * col_fib[c]
               for r in range(h) for c in range(w))


class TestRules(unittest.TestCase):
    def test_every_legal_move_preserves_value(self):
        random.seed(1)
        for _ in range(30):
            p = Problem(difficulty="Medium")
            g = Grid(p.grid_width, p.grid_height, p)
            state = g.state()
            self.assertEqual(grid_value(state), p.dividend)
            for (r, c, d) in rules.legal_moves(state):
                after = rules.apply(state, r, c, d)
                self.assertEqual(grid_value(after), grid_value(state),
                                 msg=f"{d} at ({r},{c}) changed value on {p.label}")
                # tiles never go negative
                self.assertTrue(all(v >= 0 for row in after for v in row))

    def test_is_valid_rejects_empty_and_out_of_bounds(self):
        state = [[0, 1, 0], [0, 0, 0]]
        self.assertFalse(rules.is_valid(state, 0, 0, "RIGHT"))   # empty cell
        self.assertFalse(rules.is_valid(state, 5, 5, "LEFT"))    # out of bounds
        self.assertFalse(rules.is_valid(state, 0, 2, "RIGHT"))   # rightmost split

    def test_move_wrapper_matches_pure_apply(self):
        random.seed(2)
        p = Problem(difficulty="Easy")
        g = Grid(p.grid_width, p.grid_height, p)
        moves = rules.legal_moves(g.state())
        r, c, d = moves[0]
        expected = rules.apply(g.state(), r, c, d)
        Move(g, col=c, row=r, direction=d).make_move()
        self.assertEqual(g.state(), expected)

    def test_inverse_move_reverses_every_legal_move(self):
        random.seed(7)
        for _ in range(25):
            p = Problem(difficulty="Hard")
            g = Grid(p.grid_width, p.grid_height, p)
            state = g.state()
            for _step in range(8):
                legal = rules.legal_moves(state)
                for (r, c, d) in legal:
                    after = rules.apply(state, r, c, d)
                    ir, ic, idir = rules.inverse_move(r, c, d)
                    self.assertTrue(rules.is_valid(after, ir, ic, idir))
                    restored = rules.apply(after, ir, ic, idir)
                    self.assertEqual(restored, state)
                if legal:
                    r, c, d = random.choice(legal)
                    state = rules.apply(state, r, c, d)


if __name__ == "__main__":
    unittest.main()

