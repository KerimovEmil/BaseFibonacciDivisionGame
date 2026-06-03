"""The application shell: window, shared background, async main loop, scene switching.

The loop is `async` and yields every frame so the exact same code runs under
pygbag/WASM (web) and on the desktop.
"""
import asyncio
import pygame
from zdg import theme, sound
from zdg.settings import (
    TITLE, WINDOW_WIDTH, WINDOW_HEIGHT, FPS, GAME_ICON_PATH,
    BG_TOP, BG_BOTTOM, BG_IMG, BG_IMG_ALPHA, DEFAULT_DIFFICULTY,
)


class App:
    def __init__(self):
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
        self.difficulty = DEFAULT_DIFFICULTY
        self.best_scores = {}        # problem label -> fewest moves this session
        self._scene = None
        self._next_scene = None
        self._background = self._build_background()
        sound.init()

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

    # ----- best score helper ---------------------------------------------
    def record_best(self, label, moves):
        cur = self.best_scores.get(label)
        if cur is None or moves < cur:
            self.best_scores[label] = moves

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
