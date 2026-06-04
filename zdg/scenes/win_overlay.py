"""Win celebration: dim + confetti + stats card with Play Again / Menu."""
import pygame
from zdg import theme
from zdg.particles import ParticleSystem
from zdg.ui.button import Button
from zdg.settings import (
    WINDOW_WIDTH, WINDOW_HEIGHT, PANEL, TEXT, MUTED, GOOD, ACCENT,
)


def _fmt_time(seconds):
    seconds = int(seconds)
    return f"{seconds // 60}:{seconds % 60:02d}"


class WinOverlay:
    def __init__(self, moves, seconds, optimal, on_again, on_menu):
        self.moves = moves
        self.seconds = seconds
        self.optimal = optimal
        self.particles = ParticleSystem()
        self.particles.burst(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, count=120)
        self._t = 0.0
        cx = WINDOW_WIDTH // 2
        self.card = pygame.Rect(cx - 230, WINDOW_HEIGHT // 2 - 170, 460, 340)
        self.again_btn = Button((cx - 200, self.card.bottom - 78, 190, 54),
                                "Play Again", on_click=on_again, kind="primary",
                                icon="new", font_size=22)
        self.menu_btn = Button((cx + 10, self.card.bottom - 78, 190, 54),
                               "Menu", on_click=on_menu, icon="menu", font_size=22)
        self.buttons = [self.again_btn, self.menu_btn]

    @property
    def perfect(self):
        return self.optimal is not None and self.moves == self.optimal

    def handle_event(self, event):
        for b in self.buttons:
            b.handle_event(event)

    def update(self, dt):
        self._t += dt
        self.particles.update(dt)
        if self._t > 1.2 and not self.particles.active and self._t % 2 < dt:
            self.particles.fountain(WINDOW_WIDTH, count=24)
        mouse = pygame.mouse.get_pos()
        for b in self.buttons:
            b.update(mouse, dt)

    def draw(self, surface):
        dim = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        dim.fill((10, 12, 24, 180))
        surface.blit(dim, (0, 0))

        scale = min(1.0, self._t * 4)
        card = self.card.inflate(-(1 - scale) * self.card.width,
                                 -(1 - scale) * self.card.height)
        theme.draw_shadow(surface, card, radius=22, spread=18, alpha=120)
        theme.rounded_rect(surface, card, PANEL, radius=22)
        pygame.draw.rect(surface, ACCENT, card, width=1, border_radius=22)

        if scale >= 1.0:
            cx = card.centerx
            theme.text(surface, "Solved!", theme.get_font(48, True), GOOD,
                       center=(cx, card.y + 64))
            label = "Perfect — optimal solution!" if self.perfect else "Nicely done."
            theme.text(surface, label, theme.get_font(20), MUTED,
                       center=(cx, card.y + 104))
            stats = [("Moves", str(self.moves)),
                     ("Time", _fmt_time(self.seconds))]
            if self.optimal is not None:
                stats.append(("Optimal", str(self.optimal)))
            sw = 120
            sx = cx - (len(stats) * sw) // 2 + sw // 2
            for name, value in stats:
                theme.text(surface, value, theme.get_font(34, True), TEXT,
                           center=(sx, card.y + 162))
                theme.text(surface, name, theme.get_font(14, True), MUTED,
                           center=(sx, card.y + 192))
                sx += sw
            for b in self.buttons:
                b.draw(surface)

        self.particles.draw(surface)
