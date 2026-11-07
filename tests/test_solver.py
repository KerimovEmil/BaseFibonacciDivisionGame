import random
import unittest

from zdg import solver
from zdg.problem import Problem
from zdg.grid import Grid


class TestSolver(unittest.TestCase):
    def test_solver_finds_winning_path(self):
        random.seed(3)
        for _ in range(12):
            p = Problem(difficulty="Medium")
            g = Grid(p.grid_width, p.grid_height, p)
            mask = g.solution_mask()
            path = solver.solve(g.state(), mask)
            self.assertIsNotNone(path, f"no path for {p.label}")
            for (r, c, d) in path:
                self.assertTrue(g.apply_move(r, c, d))
            self.assertTrue(g.is_win(), f"path did not win {p.label}")

    def test_already_solved_returns_empty(self):
        p = Problem(difficulty="Easy")
        g = Grid(p.grid_width, p.grid_height, p)
        mask = g.solution_mask()
        path = solver.solve(g.state(), mask)
        # drive to the solution, then a re-solve should be zero moves
        for (r, c, d) in path:
            g.apply_move(r, c, d)
        self.assertEqual(solver.solve(g.state(), mask), [])

    def test_hint_is_first_optimal_move(self):
        random.seed(4)
        p = Problem(difficulty="Medium")
        g = Grid(p.grid_width, p.grid_height, p)
        mask = g.solution_mask()
        path = solver.solve(g.state(), mask)
        self.assertEqual(solver.hint(g.state(), mask), path[0])

    def test_solver_scales_to_hard_puzzles(self):
        # Exhaustively test all Hard factor pairs (6 <= a <= b <= 13)
        for a in range(6, 14):
            for b in range(a, 14):
                p = Problem(difficulty="Hard", lower=a, upper=a)
                # Force exact pair (a, b)
                from zdg.util import convert_decimal_to_base_fib
                p.divisor, p.quotient, p.dividend = a, b, a * b
                p.fib_dividend = convert_decimal_to_base_fib(p.dividend)
                p.fib_divisor = convert_decimal_to_base_fib(p.divisor)
                p.fib_quotient = convert_decimal_to_base_fib(p.quotient)
                g = Grid(p.grid_width, p.grid_height, p)
                mask = g.solution_mask()
                path = solver.solve(g.state(), mask)
                self.assertIsNotNone(path, f"no path found for Hard puzzle {p.label}")
                for (r, c, d) in path:
                    self.assertTrue(g.apply_move(r, c, d))
                self.assertTrue(g.is_win(), f"path did not win Hard puzzle {p.label}")

    def test_unsolvable_state_returns_none(self):
        p = Problem(difficulty="Easy")
        g = Grid(p.grid_width, p.grid_height, p)
        bad_state = g.state()
        bad_state[0][0] += 1  # corrupt invariant value
        self.assertIsNone(solver.solve(bad_state, g.solution_mask()))


if __name__ == "__main__":
    unittest.main()


