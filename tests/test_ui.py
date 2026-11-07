import os
import unittest

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

from tests._pygame_compat import ensure_pygame  # noqa: E402
pygame = ensure_pygame()
from zdg import theme  # noqa: E402

from zdg.problem import Problem  # noqa: E402
from zdg.grid import Grid  # noqa: E402
from zdg.ui.board_view import BoardView  # noqa: E402


class TestUI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.font.init()
        pygame.display.set_mode((1000, 720))

    def test_shadow_and_ring_caches_reuse_surfaces(self):
        surf = pygame.Surface((200, 200), pygame.SRCALPHA)
        theme._shadow_cache.clear()
        theme.draw_shadow(surf, (20, 20, 80, 40), radius=10, spread=6, alpha=70)
        self.assertEqual(len(theme._shadow_cache), 1)
        cached = next(iter(theme._shadow_cache.values()))
        theme.draw_shadow(surf, (50, 60, 80, 40), radius=10, spread=6, alpha=70)
        self.assertEqual(len(theme._shadow_cache), 1)
        self.assertIs(next(iter(theme._shadow_cache.values())), cached)

        r1 = theme.glow_ring(64, (100, 150, 250), alpha=120, thickness=4)
        r2 = theme.glow_ring(64, (100, 150, 250), alpha=120, thickness=4)
        self.assertIs(r1, r2)

    def test_board_view_flight_animations_and_drag_badge(self):
        p = Problem(difficulty="Easy", lower=3, upper=4)
        g = Grid(p.grid_width, p.grid_height, p)
        bv = BoardView(g)
        bv.layout(pygame.Rect(36, 130, 928, 480))
        surf = pygame.Surface((1000, 720))

        # Trigger a split move on the bottom row
        bv.record_move(g.height - 1, 0, "RIGHT")
        self.assertGreaterEqual(len(bv._flights), 1)

        # Render mid-flight and with a multi-tile drag ghost
        cell = g.array[g.height - 1][0]
        cell.value = 2
        bv.update(0.05)
        bv.draw(surf, drag=(cell, (400, 300)))
        self.assertGreaterEqual(len(bv._flights), 1)

        # Advance past animation duration; flights should complete
        bv.update(0.5)
        self.assertEqual(len(bv._flights), 0)


if __name__ == "__main__":
    unittest.main()
