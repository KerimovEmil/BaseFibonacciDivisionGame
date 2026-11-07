"""Title screen: difficulty selection, play, daily challenge, custom puzzle, tutorial, quit."""
import math
import sys
import pygame
from zdg import theme
from zdg.problem import Problem
from zdg.scenes.scene import Scene
from zdg.ui.button import Button
from zdg.settings import (
    WINDOW_WIDTH, WINDOW_HEIGHT, GAME_NAME, TEXT, MUTED, ACCENT, PANEL, PANEL_LIGHT,
    DIFFICULTY_ORDER,
)
from zdg.util import get_first_n_zeckendorf_terms


class MenuScene(Scene):
    def __init__(self, app):
        super().__init__(app)
        self._pulse = 0.0
        cf = getattr(app, "custom_factors", (3, 5))
        self.custom_a = int(cf[0])
        self.custom_b = int(cf[1])
        cx = WINDOW_WIDTH // 2
        pill_w, pill_h, gap = 130, 46, 14
        total = len(DIFFICULTY_ORDER) * pill_w + (len(DIFFICULTY_ORDER) - 1) * gap
        start = cx - total // 2
        self.diff_buttons = []
        for i, name in enumerate(DIFFICULTY_ORDER):
            rect = (start + i * (pill_w + gap), 350, pill_w, pill_h)
            self.diff_buttons.append(
                Button(rect, name, on_click=lambda n=name: self._set_diff(n))
            )

        self.play_btn = Button(
            (cx - 160, 418, 320, 56),
            "Play",
            on_click=self._play,
            kind="primary",
            icon="solve",
            font_size=26,
            tooltip="Start a random puzzle at selected difficulty (Enter)",
        )
        self.daily_btn = Button(
            (cx - 160, 486, 320, 48),
            "Daily Challenge",
            on_click=self._play_daily,
            icon="hint",
            font_size=20,
            tooltip="Play today's seeded puzzle (D)",
        )

        # Custom factor stepper row: [-] a [+]  ×  [-] b [+]   [Play a×b]
        cy = 550
        self.a_minus_btn = Button((cx - 160, cy, 34, 42), "-", on_click=lambda: self._step_custom(-1, 0), font_size=20)
        self.a_plus_btn = Button((cx - 86, cy, 34, 42), "+", on_click=lambda: self._step_custom(1, 0), font_size=20)
        self.b_minus_btn = Button((cx - 26, cy, 34, 42), "-", on_click=lambda: self._step_custom(0, -1), font_size=20)
        self.b_plus_btn = Button((cx + 48, cy, 34, 42), "+", on_click=lambda: self._step_custom(0, 1), font_size=20)
        self.custom_btn = Button(
            (cx + 94, cy, 66, 42),
            "Go",
            on_click=self._play_custom,
            font_size=18,
            tooltip="Launch custom factor puzzle (C)",
        )
        self.custom_controls = [
            self.a_minus_btn,
            self.a_plus_btn,
            self.b_minus_btn,
            self.b_plus_btn,
            self.custom_btn,
        ]

        if sys.platform == "emscripten":
            self.tutorial_btn = Button(
                (cx - 160, 608, 320, 48), "How to Play", on_click=self._tutorial, font_size=18
            )
            self.quit_btn = None
            self.buttons = (
                self.diff_buttons
                + [self.play_btn, self.daily_btn]
                + self.custom_controls
                + [self.tutorial_btn]
            )
        else:
            self.tutorial_btn = Button(
                (cx - 160, 608, 155, 48), "How to Play", on_click=self._tutorial, font_size=18
            )
            self.quit_btn = Button(
                (cx + 5, 608, 155, 48), "Quit", on_click=self._quit, kind="ghost", font_size=18
            )
            self.buttons = (
                self.diff_buttons
                + [self.play_btn, self.daily_btn]
                + self.custom_controls
                + [self.tutorial_btn, self.quit_btn]
            )

    def _set_diff(self, name):
        if hasattr(self.app, "set_difficulty"):
            self.app.set_difficulty(name)
        else:
            self.app.difficulty = name

    def _step_custom(self, da, db):
        self.custom_a = max(2, min(13, self.custom_a + da))
        self.custom_b = max(2, min(13, self.custom_b + db))
        self.app.custom_factors = (self.custom_a, self.custom_b)

    def _play(self):
        from zdg.scenes.game_scene import GameScene
        self.app.go_to(GameScene(self.app))

    def _play_daily(self):
        from zdg.scenes.game_scene import GameScene
        prob = Problem.daily(difficulty=self.app.difficulty)
        self.app.go_to(GameScene(self.app, problem=prob))

    def _play_custom(self):
        from zdg.scenes.game_scene import GameScene
        prob = Problem.custom(self.custom_a, self.custom_b)
        self.app.go_to(GameScene(self.app, problem=prob))

    def _tutorial(self):
        from zdg.scenes.tutorial_scene import TutorialScene
        self.app.go_to(TutorialScene(self.app))

    def _quit(self):
        self.app.running = False

    def handle_event(self, event):
        for b in self.buttons:
            if b.handle_event(event):
                return
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self._play()
            elif event.key == getattr(pygame, "K_d", None):
                self._play_daily()
            elif event.key == getattr(pygame, "K_c", None):
                self._play_custom()
            elif event.key in (getattr(pygame, "K_t", None), getattr(pygame, "K_h", None)):
                self._tutorial()
            elif event.key == getattr(pygame, "K_1", None):
                self._set_diff("Easy")
            elif event.key == getattr(pygame, "K_2", None):
                self._set_diff("Medium")
            elif event.key == getattr(pygame, "K_3", None):
                self._set_diff("Hard")
            elif event.key == pygame.K_ESCAPE:
                self._quit()

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
            surface.blit(chip, (fx + i * 46, 96))
            theme.text(surface, f, theme.get_font(16, True), (*TEXT, a),
                       center=(fx + i * 46 + 19, 115))

        theme.text(surface, "Base Fibonacci", theme.get_font(60, True), TEXT,
                   center=(cx, 192))
        theme.text(surface, "Division", theme.get_font(60, True), ACCENT,
                   center=(cx, 250))
        theme.text(surface, "Factor the number by sliding tiles through Fibonacci moves",
                   theme.get_font(19), MUTED, center=(cx, 302))
        theme.text(surface, "DIFFICULTY", theme.get_font(13, True), MUTED,
                   center=(cx, 332))

        # Custom factor values between stepper buttons
        cy = 571
        theme.text(surface, str(self.custom_a), theme.get_font(20, True), TEXT,
                   center=(cx - 106, cy))
        theme.text(surface, "×", theme.get_font(20, True), ACCENT,
                   center=(cx - 39, cy))
        theme.text(surface, str(self.custom_b), theme.get_font(20, True), TEXT,
                   center=(cx + 28, cy))

        for b in self.buttons:
            b.draw(surface)
        for b in self.buttons:
            b.draw_tooltip(surface)

        prod = self.custom_a * self.custom_b
        theme.text(
            surface,
            f"Custom puzzle: {prod} = {min(self.custom_a, self.custom_b)} × {max(self.custom_a, self.custom_b)}   ·   Easy / Medium / Hard sets random & daily range",
            theme.get_font(14),
            MUTED,
            center=(cx, WINDOW_HEIGHT - 32),
        )
