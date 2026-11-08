"""The application shell: window, shared background, async main loop, scene switching.

The loop is `async` and yields every frame so the exact same code runs under
pygbag/WASM (web) and on the desktop.
"""
import asyncio
import sys
import pygame
from zdg import theme, sound, persistence
from zdg.settings import (
    TITLE, WINDOW_WIDTH, WINDOW_HEIGHT, FPS, GAME_ICON_PATH,
    BG_TOP, BG_BOTTOM, BG_IMG, BG_IMG_ALPHA, DEFAULT_DIFFICULTY,
    PANEL, PANEL_LIGHT, TEXT, MUTED, ACCENT, TILE_LIVE, TILE_GOOD, TARGET_SLOT,
)


class App:
    def __init__(self, save_path=None):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(TITLE)
        try:
            pygame.display.set_icon(pygame.image.load(GAME_ICON_PATH))
        except Exception:
            pass
        self._draw_initial_splash(progress=0.35, status="Loading Fibonacci engine…")
        self.clock = pygame.time.Clock()
        self.running = True
        self._save_path = save_path
        saved = persistence.load_save(self._save_path)
        self.difficulty = saved.get("difficulty", DEFAULT_DIFFICULTY)
        self.best_scores = dict(saved.get("best_scores", {}))
        self.custom_factors = (3, 5)
        self._scene = None
        self._next_scene = None
        self._transition_alpha = 220.0
        self._web_loader_dismissed = False
        self._background = self._build_background()
        self._draw_initial_splash(progress=0.80, status="Initializing audio & assets…")
        sound.init()
        sound.set_muted(saved.get("muted", False))
        self._draw_initial_splash(progress=1.0, status="Ready!")

    # ----- initial splash -------------------------------------------------
    def _draw_initial_splash(self, progress=0.5, status="Loading…"):
        """Paint an immediate branded loading screen so startup is never blank."""
        try:
            bg = theme.vgradient((WINDOW_WIDTH, WINDOW_HEIGHT), BG_TOP, BG_BOTTOM)
            self.screen.blit(bg, (0, 0))
            cx, cy = WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2
            card = pygame.Rect(cx - 230, cy - 125, 460, 250)
            theme.draw_shadow(self.screen, card, radius=22, spread=16, alpha=95)
            theme.rounded_rect(self.screen, card, PANEL, radius=22)

            fib_chips = ["21", "13", "8", "5", "3", "2", "1"]
            chip_size, gap = 38, 10
            total_w = len(fib_chips) * chip_size + (len(fib_chips) - 1) * gap
            sx = cx - total_w // 2
            sy = card.y + 34
            for i, label in enumerate(fib_chips):
                colors = TILE_GOOD if i in (2, 6) else TILE_LIVE
                tile = theme.tile_surface(chip_size, colors[0], colors[1], radius=9)
                self.screen.blit(tile, (sx + i * (chip_size + gap), sy))
                theme.text(
                    self.screen,
                    label,
                    theme.get_font(15, True),
                    (255, 255, 255),
                    center=(sx + i * (chip_size + gap) + chip_size // 2, sy + chip_size // 2),
                )

            theme.text(
                self.screen,
                "Base Fibonacci Division",
                theme.get_font(28, True),
                TEXT,
                center=(cx, card.y + 114),
            )
            theme.text(
                self.screen,
                "Zeckendorf Tile Puzzle",
                theme.get_font(15),
                MUTED,
                center=(cx, card.y + 144),
            )

            track = pygame.Rect(cx - 170, card.y + 174, 340, 10)
            theme.rounded_rect(self.screen, track, BG_TOP, radius=5)
            fill_w = max(12, int(track.width * max(0.0, min(1.0, progress))))
            fill = pygame.Rect(track.x, track.y, fill_w, track.height)
            theme.rounded_rect(self.screen, fill, ACCENT, radius=5)

            theme.text(
                self.screen,
                status,
                theme.get_font(13, True),
                MUTED,
                center=(cx, card.y + 206),
            )
            pygame.display.flip()
        except Exception:
            pass

    @staticmethod
    def _dismiss_web_loader():
        if sys.platform != "emscripten":
            return
        try:
            import platform
            if hasattr(platform.window, "dismissFibLoader"):
                platform.window.dismissFibLoader()
        except Exception:
            pass

    # ----- background -----------------------------------------------------
    def _build_background(self):
        bg = theme.vgradient((WINDOW_WIDTH, WINDOW_HEIGHT), BG_TOP, BG_BOTTOM).convert()
        try:
            img = pygame.image.load(BG_IMG).convert_alpha()
            img = pygame.transform.smoothscale(img, (WINDOW_WIDTH, WINDOW_HEIGHT))
            img.set_alpha(BG_IMG_ALPHA)
            bg.blit(img, (0, 0))
        except Exception:
            pass
        return bg

    # ----- scene management ----------------------------------------------
    def go_to(self, scene):
        self._next_scene = scene

    def _apply_scene_switch(self):
        if self._next_scene is not None:
            is_first = self._scene is None
            self._scene = self._next_scene
            self._next_scene = None
            self._transition_alpha = 210.0 if is_first else 140.0
            self._scene.on_enter()

    # ----- persistence & best score helpers -------------------------------
    def save_state(self):
        persistence.save_data(
            {
                "best_scores": self.best_scores,
                "difficulty": self.difficulty,
                "muted": sound.muted,
            },
            path=self._save_path,
        )

    def set_difficulty(self, name):
        self.difficulty = name
        self.save_state()

    def record_best(self, label, moves):
        cur = self.best_scores.get(label)
        if cur is None or moves < cur:
            self.best_scores[label] = moves
            self.save_state()

    # ----- main loop ------------------------------------------------------
    async def run(self):
        # Imported here to avoid a circular import at module load time.
        from zdg.scenes.menu_scene import MenuScene
        self.go_to(MenuScene(self))
        self._apply_scene_switch()

        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            dt = min(dt, 0.05)  # clamp after stalls (e.g. tab refocus)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self._scene.handle_event(event)

            self._scene.update(dt)
            if self._transition_alpha > 0:
                self._transition_alpha = max(0.0, self._transition_alpha - dt * 680.0)

            self.screen.blit(self._background, (0, 0))
            self._scene.draw(self.screen)

            if self._transition_alpha > 1.0:
                veil = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
                veil.fill((*BG_TOP, int(self._transition_alpha)))
                self.screen.blit(veil, (0, 0))

            pygame.display.flip()
            if not self._web_loader_dismissed:
                self._web_loader_dismissed = True
                self._dismiss_web_loader()

            self._apply_scene_switch()
            await asyncio.sleep(0)

        pygame.quit()


async def main():
    await App().run()
