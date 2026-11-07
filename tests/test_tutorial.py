import unittest
from tests._pygame_compat import ensure_pygame

pygame = ensure_pygame()

from zdg import rules
from zdg.scenes.tutorial_scene import TutorialScene, PAGES, INTERACTIVE_PAGE


class DummyApp:
    def __init__(self, difficulty="Easy"):
        self.difficulty = difficulty
        self.best_scores = {}
        self.current_scene = None

    def record_best(self, problem_label, moves):
        self.best_scores[problem_label] = moves

    def go_to(self, scene):
        self.current_scene = scene


class TutorialSceneTests(unittest.TestCase):
    def setUp(self):
        pygame.init()
        pygame.font.init()

    def test_keyboard_and_dot_navigation(self):
        app = DummyApp()
        scene = TutorialScene(app)
        surface = pygame.Surface((1280, 820), pygame.SRCALPHA)

        self.assertEqual(scene.page, 0)
        scene.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT))
        self.assertEqual(scene.page, 1)
        scene.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT))
        self.assertEqual(scene.page, 0)

        # Jump directly to interactive page via page dot click
        dots = scene._dot_centers()
        scene.handle_event(
            pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=dots[INTERACTIVE_PAGE])
        )
        self.assertEqual(scene.page, INTERACTIVE_PAGE)

        # Draw all pages cleanly
        for i in range(len(PAGES)):
            scene.page = i
            scene.update(0.016)
            scene.draw(surface)

    def test_interactive_mini_board_playthrough_and_reset(self):
        app = DummyApp()
        scene = TutorialScene(app)
        scene.page = INTERACTIVE_PAGE
        surface = pygame.Surface((1280, 820), pygame.SRCALPHA)

        # Follow the 3 live hints via click-to-move to solve 4 = 2 x 2
        steps = 0
        while not scene.mini_grid.is_win() and steps < 10:
            self.assertIsNotNone(scene.mini_hint)
            r, c, d = scene.mini_hint
            dr, dc = rules.DELTA[d]
            src_pos = scene.mini_board.cell_center(r, c)
            dst_pos = scene.mini_board.cell_center(r + dr, c + dc)
            scene.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=src_pos))
            scene.handle_event(pygame.event.Event(pygame.MOUSEBUTTONUP, button=1, pos=src_pos))
            scene.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=dst_pos))
            scene.handle_event(pygame.event.Event(pygame.MOUSEBUTTONUP, button=1, pos=dst_pos))
            steps += 1

        self.assertTrue(scene.mini_grid.is_win())
        self.assertEqual(scene.mini_moves, 3)
        scene.update(0.05)
        scene.draw(surface)

        # Reset mini-board via 'r' key
        scene.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_r))
        self.assertFalse(scene.mini_grid.is_win())
        self.assertEqual(scene.mini_moves, 0)


if __name__ == "__main__":
    unittest.main()
