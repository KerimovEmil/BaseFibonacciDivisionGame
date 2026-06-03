"""Title screen: difficulty selection, play, tutorial, quit."""
import math
import pygame
from zdg import theme
from zdg.scenes.scene import Scene
from zdg.ui.button import Button
from zdg.settings import (
    WINDOW_WIDTH, WINDOW_HEIGHT, GAME_NAME, TEXT, MUTED, ACCENT, PANEL_LIGHT,
    DIFFICULTY_ORDER,
)
from zdg.util import get_first_n_zeckendorf_terms


class MenuScene(Scene):
    def __init__(self, app):
        super().__init__(app)
        self._pulse = 0.0
        cx = WINDOW_WIDTH // 2
        pill_w, pill_h, gap = 130, 48, 14
        total = len(DIFFICULTY_ORDER) * pill_w + (len(DIFFICULTY_ORDER) - 1) * gap
        start = cx - total // 2
        self.diff_buttons = []
        for i, name in enumerate(DIFFICULTY_ORDER):
            rect = (start + i * (pill_w + gap), 366, pill_w, pill_h)
            self.diff_buttons.append(
                Button(rect, name, on_click=lambda n=name: self._set_diff(n)))

        self.play_btn = Button((cx - 150, 446, 300, 60), "Play",
                               on_click=self._play, kind="primary",
                               icon="solve", font_size=26)
        self.tutorial_btn = Button((cx - 150, 520, 145, 50), "How to Play",
                                   on_click=self._tutorial, font_size=18)
        self.quit_btn = Button((cx + 5, 520, 145, 50), "Quit",
                               on_click=self._quit, kind="ghost", font_size=18)
        self.buttons = self.diff_buttons + [self.play_btn, self.tutorial_btn, self.quit_btn]

    def _set_diff(self, name):
        self.app.difficulty = name

    def _play(self):
        from zdg.scenes.game_scene import GameScene
        self.app.go_to(GameScene(self.app))

    def _tutorial(self):
        from zdg.scenes.tutorial_scene import TutorialScene
        self.app.go_to(TutorialScene(self.app))

    def _quit(self):
        self.app.running = False

    def handle_event(self, event):
        for b in self.buttons:
            b.handle_event(event)

    def update(self, dt):
        self._pulse += dt
        for b in self.diff_buttons:
            b.kind = "primary" if b.label == self.app.difficulty else "normal"
        mouse = pygame.mouse.get_pos()
        for b in self.buttons:
            b.update(mouse, dt)

    def draw(self, surface):
        cx = WINDOW_WIDTH // 2
        # decorative Fibonacci ribbon
        fibs = get_first_n_zeckendorf_terms(9)[::-1]
        fx = cx - (len(fibs) * 46) // 2
        for i, f in enumerate(fibs):
            a = 90 + int(80 * (math.sin(self._pulse * 2 + i * 0.5) + 1) / 2)
            chip = pygame.Surface((38, 38), pygame.SRCALPHA)
            pygame.draw.rect(chip, (*ACCENT, a // 3), chip.get_rect(), border_radius=8)
            surface.blit(chip, (fx + i * 46, 110))
            theme.text(surface, f, theme.get_font(16, True), (*TEXT, a),
                       center=(fx + i * 46 + 19, 129))

        theme.text(surface, "Base Fibonacci", theme.get_font(62, True), TEXT,
                   center=(cx, 210))
        theme.text(surface, "Division", theme.get_font(62, True), ACCENT,
                   center=(cx, 270))
        theme.text(surface, "Factor the number by sliding tiles through Fibonacci moves",
                   theme.get_font(20), MUTED, center=(cx, 322))
        theme.text(surface, "DIFFICULTY", theme.get_font(14, True), MUTED,
                   center=(cx, 348))

        for b in self.buttons:
            b.draw(surface)

        theme.text(surface, "Easy / Medium / Hard sets the size of the numbers",
                   theme.get_font(15), MUTED, center=(cx, WINDOW_HEIGHT - 36))
