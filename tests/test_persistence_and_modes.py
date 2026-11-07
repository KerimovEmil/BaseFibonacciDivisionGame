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


if __name__ == "__main__":
    unittest.main()
