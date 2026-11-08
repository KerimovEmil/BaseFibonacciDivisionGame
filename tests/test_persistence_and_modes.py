import tempfile
import unittest
from pathlib import Path
from tests._pygame_compat import ensure_pygame

pygame = ensure_pygame()

from zdg import persistence, sound
from zdg.app import App
from zdg.problem import Problem
from zdg.scenes.menu_scene import MenuScene
from zdg.scenes.game_scene import GameScene


class PersistenceAndModesTests(unittest.TestCase):
    def setUp(self):
        pygame.init()
        pygame.font.init()

    def test_persistence_roundtrip_and_app_restore(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            save_file = Path(tmpdir) / "save.json"
            sound.set_muted(False)

            app1 = App(save_path=save_file)
            self.assertEqual(app1.difficulty, "Medium")
            self.assertEqual(app1.best_scores, {})

            app1.set_difficulty("Hard")
            app1.record_best("15 = 3 × 5", 6)
            app1.record_best("15 = 3 × 5", 9)  # worse score should not overwrite
            sound.set_muted(True)
            app1.save_state()

            # New App instance loads persisted state
            sound.set_muted(False)
            app2 = App(save_path=save_file)
            self.assertEqual(app2.difficulty, "Hard")
            self.assertEqual(app2.best_scores.get("15 = 3 × 5"), 6)
            self.assertTrue(sound.muted)

            # Corrupted file gracefully falls back to defaults
            save_file.write_text("{corrupted json", encoding="utf-8")
            loaded = persistence.load_save(save_file)
            self.assertEqual(loaded["difficulty"], "Medium")
            self.assertEqual(loaded["best_scores"], {})
            sound.set_muted(False)

    def test_daily_and_custom_problems(self):
        d1 = Problem.daily(date_str="2026-11-07", difficulty="Medium")
        d2 = Problem.daily(date_str="2026-11-07", difficulty="Medium")
        self.assertEqual((d1.divisor, d1.quotient, d1.dividend), (d2.divisor, d2.quotient, d2.dividend))
        self.assertEqual(d1.mode_label, "Daily · 2026-11-07")

        c = Problem.custom(11, 7)
        self.assertEqual(c.divisor, 7)
        self.assertEqual(c.quotient, 11)
        self.assertEqual(c.dividend, 77)
        self.assertEqual(c.mode_label, "Custom")

        with self.assertRaises(ValueError):
            Problem.custom(0, 5)

    def test_menu_scene_daily_and_custom_flows(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            app = App(save_path=Path(tmpdir) / "save.json")
            menu = MenuScene(app)
            surface = pygame.Surface((1280, 820), pygame.SRCALPHA)

            # Step custom factors: starts at (3, 5) -> step to (4, 6)
            menu._step_custom(1, 1)
            self.assertEqual((menu.custom_a, menu.custom_b), (4, 6))
            menu.update(0.016)
            menu.draw(surface)

            # Press 'c' to launch custom game
            menu.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_c))
            self.assertIsInstance(app._next_scene, GameScene)
            self.assertEqual(app._next_scene.problem.label, "24 = 4 × 6")
            self.assertEqual(app._next_scene.problem.mode_label, "Custom")

            # Press 'd' to launch Daily Challenge
            menu.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_d))
            self.assertIsInstance(app._next_scene, GameScene)
            self.assertTrue(app._next_scene.problem.mode_label.startswith("Daily ·"))

    def test_cell_value_inspector_on_hover_and_select(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            app = App(save_path=Path(tmpdir) / "save.json")
            scene = GameScene(app, problem=Problem.custom(3, 5))
            surface = pygame.Surface((1280, 820), pygame.SRCALPHA)

            # Bottom-left cell (row = height - 1, col = 0) has row_fib = 1, col_fib = 13 (since 15 = 13 + 2)
            r = scene.grid.height - 1
            c = 0
            pos = scene.board.cell_center(r, c)
            scene.handle_event(pygame.event.Event(pygame.MOUSEMOTION, pos=pos))
            self.assertEqual(scene.hovered_cell, (r, c))

            info = scene.inspected_cell_info()
            self.assertIsNotNone(info)
            self.assertEqual(info["row_fib"], 1)
            self.assertEqual(info["col_fib"], 13)
            self.assertEqual(info["unit_value"], 13)
            self.assertEqual(info["count"], 1)
            self.assertEqual(info["total_value"], 13)
            self.assertIn("1 × 13 = 13", info["summary"])

            # Render scene with active inspector
            scene.draw(surface)

    def test_extreme_mode_win_conditions_and_ui(self):
        from zdg.grid import Grid, is_extreme_win_state
        from zdg.settings import TILE_LIVE, TILE_GOOD

        # 8 = 2 * 4 -> Wait: let's test divisor = 4 (fib '101', rows 0 and 2) and quotient = 5 (fib '1000')
        # so there are 2 target rows (row 0 and row 2) and 1 non-target row (row 1).
        prob = Problem(difficulty="Extreme", divisor=4, quotient=5)
        self.assertTrue(prob.extreme)
        self.assertEqual(prob.display_label(solved=False), "20 ÷ 4 = ?")
        self.assertEqual(prob.display_label(solved=True), "20 = 4 × 5")

        grid = Grid(prob.grid_width, prob.grid_height, prob)
        self.assertTrue(grid.extreme)
        self.assertEqual(grid.target_rows(), (0, 2))
        self.assertEqual(grid.target_row_mask(), (True, False, True))
        self.assertTrue(grid.is_target_row(0))
        self.assertFalse(grid.is_target_row(1))
        self.assertTrue(grid.is_target_row(2))
        self.assertFalse(grid.is_win())

        w = grid.width
        # Identical target rows, but non-target row 1 still has a piece -> NOT a win
        partial = [[0] * w for _ in range(3)]
        partial[0][-1] = 2
        partial[2][-1] = 2
        partial[1][0] = 1
        grid.set_state(partial)
        self.assertFalse(grid.is_win())

        # All pieces in target rows, but target rows 0 and 2 differ -> NOT a win
        diff_rows = [[0] * w for _ in range(3)]
        diff_rows[0] = [0] * (w - 2) + [1, 0]
        diff_rows[2] = [0] * (w - 2) + [0, 2]
        grid.set_state(diff_rows)
        self.assertFalse(grid.is_win())

        # Non-canonical identical arrangement in target rows (e.g. stacked/split tiles)
        # with all non-target rows empty -> IS a win in Extreme mode!
        identical_non_canonical = [[0] * w for _ in range(3)]
        identical_non_canonical[0] = [0] * (w - 3) + [1, 0, 2]
        identical_non_canonical[2] = [0] * (w - 3) + [1, 0, 2]
        grid.set_state(identical_non_canonical)
        self.assertTrue(grid.is_win())
        self.assertTrue(is_extreme_win_state(identical_non_canonical, grid.target_row_mask()))

        # Verify BoardView does not leak target squares via tile colors or inspector in Extreme mode
        with tempfile.TemporaryDirectory() as tmpdir:
            app = App(save_path=Path(tmpdir) / "save.json")
            menu = MenuScene(app)
            # Press '4' to select Extreme difficulty and verify persistence
            menu.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_4))
            self.assertEqual(app.difficulty, "Extreme")
            app_reloaded = App(save_path=Path(tmpdir) / "save.json")
            self.assertEqual(app_reloaded.difficulty, "Extreme")

            scene = GameScene(app, problem=Problem(difficulty="Extreme", divisor=4, quotient=5))
            surface = pygame.Surface((1280, 820), pygame.SRCALPHA)

            # Find a solution cell and place 1 tile in it while board is not yet won
            sol_r, sol_c = next(
                (r, c)
                for r in range(scene.grid.height)
                for c in range(scene.grid.width)
                if scene.grid.array[r][c].solution
            )
            scene.grid.array[sol_r][sol_c].value = 1
            self.assertFalse(scene.grid.is_win())
            # Tile color must remain TILE_LIVE (not TILE_GOOD) so target column is not leaked
            self.assertEqual(
                scene.board._tile_colors(scene.grid.array[sol_r][sol_c]),
                TILE_LIVE,
            )

            # Inspector in Extreme mode indicates Target Row for any column in a target row
            non_sol_c = next(
                c for c in range(scene.grid.width) if not scene.grid.array[sol_r][c].solution
            )
            info_target_row = scene.board.cell_math_info(sol_r, non_sol_c)
            self.assertTrue(info_target_row["is_target_row"])
            self.assertIn("Target Row", info_target_row["summary"])

            info_non_target_row = scene.board.cell_math_info(1, sol_c)
            self.assertFalse(info_non_target_row["is_target_row"])
            self.assertNotIn("Target", info_non_target_row["summary"])

            # Render Extreme mode board and HUD before and after winning
            scene.draw(surface)
            scene.grid.set_state(identical_non_canonical)
            scene._check_win()
            self.assertIsNotNone(scene.win)
            self.assertEqual(scene.win.problem_label, "20 = 4 × 5")
            self.assertEqual(
                scene.board._tile_colors(scene.grid.array[sol_r][sol_c]),
                TILE_GOOD,
            )
            scene.win.update(0.5)
            scene.draw(surface)


if __name__ == "__main__":
    unittest.main()
