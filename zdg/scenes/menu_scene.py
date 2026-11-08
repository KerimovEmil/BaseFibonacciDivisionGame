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
    TILE_LIVE, TILE_GOOD, TARGET_SLOT, DIFFICULTY_ORDER,
)
from zdg.util import get_first_n_zeckendorf_terms


def _ease_out_cubic(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return 1.0 - (1.0 - t) ** 3


def _ease_out_back(t: float) -> float:
    t = max(0.0, min(1.0, t))
    c1 = 1.70158
    c3 = c1 + 1.0
    return 1.0 + c3 * ((t - 1.0) ** 3) + c1 * ((t - 1.0) ** 2)


class MenuScene(Scene):
    def __init__(self, app):
        super().__init__(app)
        self._pulse = 0.0
        self._intro = 0.0
        cf = getattr(app, "custom_factors", (3, 5))
        self.custom_a = int(cf[0])
        self.custom_b = int(cf[1])
        self._ambient_tiles = self._build_ambient_tiles()
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

    @staticmethod
    def _build_ambient_tiles():
        """Deterministic ambient Fibonacci tiles that drift gently behind the menu."""
        specs = [
            (92, 140, 44, "13", 14.0, 0.0),
            (180, 520, 36, "5", 18.0, 1.1),
            (115, 360, 50, "34", 11.0, 2.3),
            (250, 640, 32, "2", 20.0, 3.4),
            (880, 170, 46, "21", 13.0, 0.7),
            (820, 470, 38, "8", 16.0, 1.9),
            (905, 330, 52, "55", 10.5, 2.8),
            (760, 630, 34, "3", 19.0, 4.1),
        ]
        return [
            {
                "x": float(x),
                "y": float(y),
                "size": size,
                "label": label,
                "speed": speed,
                "phase": phase,
            }
            for x, y, size, label, speed, phase in specs
        ]

    def on_enter(self):
        self._intro = 0.0

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
        prob = Problem.custom(
            self.custom_a,
            self.custom_b,
            extreme=(self.app.difficulty == "Hard"),
        )
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
        if self._intro < 1.0:
            self._intro = min(1.0, self._intro + dt * 1.45)
        for item in self._ambient_tiles:
            item["y"] -= item["speed"] * dt
            if item["y"] < -60:
                item["y"] = WINDOW_HEIGHT + 40
        for b in self.diff_buttons:
            b.kind = "primary" if b.label == self.app.difficulty else "normal"
        mouse = pygame.mouse.get_pos()
        for b in self.buttons:
            b.update(mouse, dt)

    def _draw_ambient(self, surface):
        for item in self._ambient_tiles:
            s = item["size"]
            dx = math.sin(self._pulse * 1.2 + item["phase"]) * 8.0
            x = int(item["x"] + dx)
            y = int(item["y"])
            box = pygame.Surface((s, s), pygame.SRCALPHA)
            pygame.draw.rect(box, (*ACCENT, 22), box.get_rect(), border_radius=10)
            pygame.draw.rect(box, (*ACCENT, 45), box.get_rect(), width=1, border_radius=10)
            surface.blit(box, (x, y))
            theme.text(
                surface,
                item["label"],
                theme.get_font(max(12, s // 3), True),
                (*MUTED, 55),
                center=(x + s // 2, y + s // 2),
            )

    def draw(self, surface):
        cx = WINDOW_WIDTH // 2
        self._draw_ambient(surface)

        # Choreographed Fibonacci ribbon with gradient tiles + gentle wave
        fibs = get_first_n_zeckendorf_terms(9)[::-1]
        fx = cx - (len(fibs) * 46) // 2
        for i, f in enumerate(fibs):
            local_t = max(0.0, min(1.0, (self._intro - i * 0.045) / 0.55))
            ease = _ease_out_back(local_t)
            wave = math.sin(self._pulse * 2.2 + i * 0.55) * 4.0
            drop_y = int((1.0 - ease) * -48 + wave)
            rx = fx + i * 46
            ry = 94 + drop_y
            rect = pygame.Rect(rx, ry, 38, 38)
            theme.draw_shadow(surface, rect, radius=10, offset=(0, 3), spread=5, alpha=65)
            colors = TILE_GOOD if i in (2, 5, 8) else TILE_LIVE
            tile = theme.tile_surface(38, colors[0], colors[1], radius=10)
            surface.blit(tile, rect.topleft)
            theme.text(surface, f, theme.get_font(15, True), (255, 255, 255),
                       center=rect.center)

        title_ease = _ease_out_cubic(min(1.0, self._intro / 0.65))
        title_dy = int((1.0 - title_ease) * 18)

        theme.text(surface, "Base Fibonacci", theme.get_font(60, True), TEXT,
                   center=(cx, 192 + title_dy))
        theme.text(surface, "Division", theme.get_font(60, True), ACCENT,
                   center=(cx, 250 + title_dy))
        theme.text(surface, "Factor the number by sliding tiles through Fibonacci moves",
                   theme.get_font(19), MUTED, center=(cx, 302 + title_dy))
        theme.text(surface, "DIFFICULTY", theme.get_font(13, True), MUTED,
                   center=(cx, 332 + title_dy))

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
            f"Custom puzzle: {prod} = {min(self.custom_a, self.custom_b)} × {max(self.custom_a, self.custom_b)}   ·   Easy / Medium / Hard sets mode & range",
            theme.get_font(14),
            MUTED,
            center=(cx, WINDOW_HEIGHT - 32),
        )
