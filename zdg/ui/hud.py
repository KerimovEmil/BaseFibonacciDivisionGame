"""Top status bar (problem banner + stat chips) and the collapsible move log."""
import pygame
from zdg import theme
from zdg.settings import PANEL, PANEL_LIGHT, TEXT, MUTED, ACCENT, GOOD


def _fmt_time(seconds):
    seconds = int(seconds)
    return f"{seconds // 60}:{seconds % 60:02d}"


def draw_top_bar(surface, area, problem_label, moves, seconds, best, optimal):
    theme.rounded_rect(surface, area, PANEL, radius=16)

    theme.text(surface, "Build", theme.get_font(18, True), ACCENT,
               topleft=(area.x + 22, area.y + 16))
    theme.text(surface, problem_label, theme.get_font(34, True), TEXT,
               topleft=(area.x + 22, area.y + 36))

    chips = [("MOVES", str(moves), TEXT)]
    chips.append(("TIME", _fmt_time(seconds), TEXT))
    if best is not None:
        chips.append(("BEST", str(best), GOOD))
    if optimal is not None:
        chips.append(("OPTIMAL", str(optimal), ACCENT))

    chip_w, chip_h, gap = 96, 54, 10
    x = area.right - 22 - len(chips) * (chip_w + gap) + gap
    y = area.centery - chip_h // 2
    for label, value, color in chips:
        rect = pygame.Rect(x, y, chip_w, chip_h)
        theme.rounded_rect(surface, rect, PANEL_LIGHT, radius=12)
        theme.text(surface, label, theme.get_font(12, True), MUTED,
                   center=(rect.centerx, rect.y + 14))
        theme.text(surface, value, theme.get_font(24, True), color,
                   center=(rect.centerx, rect.y + 36))
        x += chip_w + gap


class MoveLog:
    """A right-edge panel that slides in/out and lists the moves made."""

    def __init__(self):
        self.entries = []
        self.open = False
        self._x = 1.0  # 1 = hidden (off right edge), 0 = fully shown
        self.width = 230

    def add(self, text_line):
        self.entries.append(text_line)

    def clear(self):
        self.entries.clear()

    def toggle(self):
        self.open = not self.open

    def update(self, dt):
        target = 0.0 if self.open else 1.0
        self._x += (target - self._x) * min(1, dt * 12)

    def panel_rect(self, screen_rect, top, bottom):
        hidden = self.width + 12
        x = screen_rect.right - self.width - 16 + int(self._x * hidden)
        return pygame.Rect(x, top, self.width, bottom - top)

    def draw(self, surface, screen_rect, top, bottom):
        if self._x > 0.985:
            return
        rect = self.panel_rect(screen_rect, top, bottom)
        theme.draw_shadow(surface, rect, radius=16, offset=(-4, 6),
                          spread=12, alpha=80)
        theme.rounded_rect(surface, rect, PANEL, radius=16)
        theme.text(surface, "Move Log", theme.get_font(20, True), TEXT,
                   topleft=(rect.x + 18, rect.y + 16))
        pygame.draw.line(surface, PANEL_LIGHT, (rect.x + 18, rect.y + 46),
                         (rect.right - 18, rect.y + 46), 2)
        font = theme.get_font(16)
        line_h = 24
        max_lines = (rect.height - 70) // line_h
        shown = self.entries[-max_lines:]
        start_index = len(self.entries) - len(shown)
        y = rect.y + 58
        for i, entry in enumerate(shown):
            theme.text(surface, f"{start_index + i + 1}. {entry}", font, MUTED,
                       topleft=(rect.x + 18, y))
            y += line_h
