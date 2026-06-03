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


if __name__ == "__main__":
    unittest.main()
