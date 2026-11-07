"""The application shell: window, shared background, async main loop, scene switching.

The loop is `async` and yields every frame so the exact same code runs under
pygbag/WASM (web) and on the desktop.
"""
import asyncio
import pygame
from zdg import theme, sound, persistence
from zdg.settings import (
    TITLE, WINDOW_WIDTH, WINDOW_HEIGHT, FPS, GAME_ICON_PATH,
    BG_TOP, BG_BOTTOM, BG_IMG, BG_IMG_ALPHA, DEFAULT_DIFFICULTY,
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
        self.clock = pygame.time.Clock()
        self.running = True
        self._save_path = save_path
        saved = persistence.load_save(self._save_path)
        self.difficulty = saved.get("difficulty", DEFAULT_DIFFICULTY)
        self.best_scores = dict(saved.get("best_scores", {}))
        self.custom_factors = (3, 5)
        self._scene = None
        self._next_scene = None
        self._background = self._build_background()
        sound.init()
        sound.set_muted(saved.get("muted", False))

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
            self._scene = self._next_scene
            self._next_scene = None
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

            self.screen.blit(self._background, (0, 0))
            self._scene.draw(self.screen)
            pygame.display.flip()

            self._apply_scene_switch()
            await asyncio.sleep(0)

        pygame.quit()


async def main():
    await App().run()
