import unittest
from tests._pygame_compat import ensure_pygame

pygame = ensure_pygame()

from zdg.history import History
from zdg.ui.hud import MoveLog
from zdg.ui.button import Button
from zdg.scenes.game_scene import GameScene
from zdg.scenes.win_overlay import WinOverlay


class DummyApp:
    def __init__(self, difficulty="Easy"):
        self.difficulty = difficulty
        self.best_scores = {}
        self.current_scene = None

    def record_best(self, problem_label, moves):
        prev = self.best_scores.get(problem_label)
        if prev is None or moves < prev:
            self.best_scores[problem_label] = moves

    def go_to(self, scene):
        self.current_scene = scene


class GameplayImprovementTests(unittest.TestCase):
    def setUp(self):
        pygame.init()
        pygame.font.init()

    def test_history_labels_and_move_log_sync(self):
        h = History([[1, 0], [0, 0]])
        log = MoveLog()
        h.record([[0, 1], [0, 0]], "Right (0,0)")
        h.record([[0, 0], [0, 1]], "Down (0,1)")
        log.sync(h.labels)
        self.assertEqual(log.entries, ["Right (0,0)", "Down (0,1)"])

        h.undo()
        log.sync(h.labels)
        self.assertEqual(log.entries, ["Right (0,0)"])

        h.redo()
        log.sync(h.labels)
        self.assertEqual(log.entries, ["Right (0,0)", "Down (0,1)"])

        h.reset_to_initial()
        log.sync(h.labels)
        self.assertEqual(log.entries, [])

    def test_move_log_scrolling_and_close_button(self):
        log = MoveLog()
        log.sync([f"Move {i}" for i in range(40)])
        log.toggle()
        log._x = 0.0
        screen_rect = pygame.Rect(0, 0, 1280, 820)
        surface = pygame.Surface((1280, 820), pygame.SRCALPHA)
        log.draw(surface, screen_rect, 100, 700)

        # Scroll up with mouse wheel inside panel
        panel = log.panel_rect(screen_rect, 100, 700)
        wheel_evt = pygame.event.Event(pygame.MOUSEWHEEL, y=2, pos=panel.center)
        consumed = log.handle_event(wheel_evt, screen_rect, 100, 700)
        self.assertTrue(consumed)
        self.assertEqual(log.scroll_offset, 2)

        # Click close button
        close_evt = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN, button=1, pos=log.close_rect(panel).center
        )
        self.assertTrue(log.handle_event(close_evt, screen_rect, 100, 700))
        self.assertFalse(log.open)

    def test_click_to_move_without_dragging(self):
        app = DummyApp("Easy")
        scene = GameScene(app)
        assert scene._initial_path is not None and len(scene._initial_path) > 0
        r, c, direction = scene._initial_path[0]
        from zdg import rules
        dr, dc = rules.DELTA[direction]
        dest = (r + dr, c + dc)

        src_pos = scene.board.cell_center(r, c)
        dst_pos = scene.board.cell_center(*dest)

        # Click 1: select source tile and release on same tile
        scene.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=src_pos))
        scene.handle_event(pygame.event.Event(pygame.MOUSEBUTTONUP, button=1, pos=src_pos))
        self.assertEqual(scene.selected, (r, c))
        self.assertIn(dest, scene.highlight)
        self.assertEqual(scene.moves, 0)

        # Click 2: click highlighted destination cell directly
        scene.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=dst_pos))
        scene.handle_event(pygame.event.Event(pygame.MOUSEBUTTONUP, button=1, pos=dst_pos))
        self.assertEqual(scene.moves, 1)
        self.assertIsNone(scene.selected)

    def test_keyboard_navigation_and_shortcuts(self):
        app = DummyApp("Easy")
        scene = GameScene(app)
        assert scene._initial_path is not None and len(scene._initial_path) > 0
        r, c, direction = scene._initial_path[0]
        scene._select_cell((r, c))

        key_map = {
            "UP": pygame.K_UP,
            "DOWN": pygame.K_DOWN,
            "LEFT": pygame.K_LEFT,
            "RIGHT": pygame.K_RIGHT,
        }
        scene.handle_event(pygame.event.Event(pygame.KEYDOWN, key=key_map[direction]))
        self.assertEqual(scene.moves, 1)
        self.assertEqual(len(scene.move_log.entries), 1)

        # Undo via keyboard 'u' syncs MoveLog
        scene.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_u))
        self.assertEqual(scene.moves, 0)
        self.assertEqual(scene.move_log.entries, [])

        # Toggle move log via 'l'
        self.assertFalse(scene.move_log.open)
        scene.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_l))
        self.assertTrue(scene.move_log.open)

    def test_auto_solve_does_not_record_best_score(self):
        app = DummyApp("Easy")
        scene = GameScene(app)
        scene.do_solve()
        self.assertTrue(scene.used_auto_solve)
        while scene.auto_moves is not None:
            scene.update(0.35)
        self.assertIsNotNone(scene.win)
        self.assertTrue(scene.win.auto_solved)
        self.assertNotIn(scene.problem.label, app.best_scores)

        # Compare with manual solve
        app2 = DummyApp("Easy")
        scene2 = GameScene(app2)
        for r, c, d in list(scene2._initial_path):
            scene2._apply(r, c, d)
        self.assertIsNotNone(scene2.win)
        self.assertFalse(scene2.win.auto_solved)
        self.assertEqual(app2.best_scores.get(scene2.problem.label), scene2.optimal)

        # WinOverlay keyboard Enter triggers Play Again
        scene2.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN))
        self.assertIsNone(scene2.win)
        self.assertEqual(scene2.moves, 0)

    def test_button_tooltip_rendering(self):
        btn = Button((100, 700, 120, 50), "Hint", tooltip="Highlight optimal next move (H)")
        surface = pygame.Surface((1280, 820), pygame.SRCALPHA)
        btn.update((160, 725), 0.5)
        self.assertGreater(btn._hover, 0.55)
        btn.draw(surface)
        btn.draw_tooltip(surface)


if __name__ == "__main__":
    unittest.main()
