"""Top status bar (problem banner + stat chips) and the collapsible move log."""
import pygame
from zdg import theme
from zdg.settings import PANEL, PANEL_LIGHT, TEXT, MUTED, ACCENT, GOOD


def _fmt_time(seconds):
    seconds = int(seconds)
    return f"{seconds // 60}:{seconds % 60:02d}"


def draw_top_bar(surface, area, problem_label, moves, seconds, best, optimal,
                 inspector_text=None, mode_label=None):
    theme.rounded_rect(surface, area, PANEL, radius=16)

    header = mode_label or "Build"
    theme.text(surface, header, theme.get_font(18, True), ACCENT,
               topleft=(area.x + 22, area.y + 16))
    theme.text(surface, problem_label, theme.get_font(34, True), TEXT,
               topleft=(area.x + 22, area.y + 36))

    if inspector_text:
        pill_w = min(380, max(220, len(inspector_text) * 9 + 28))
        pill = pygame.Rect(0, 0, pill_w, 40)
        pill.center = (area.centerx - 20, area.centery)
        theme.rounded_rect(surface, pill, PANEL_LIGHT, radius=10)
        theme.text(surface, inspector_text, theme.get_font(15, True), ACCENT,
                   center=pill.center)

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
        self.scroll_offset = 0  # lines scrolled up from bottom

    def add(self, text_line):
        self.entries.append(text_line)
        self.scroll_offset = 0

    def sync(self, entries):
        self.entries = list(entries)
        self.scroll_offset = 0

    def clear(self):
        self.entries.clear()
        self.scroll_offset = 0

    def toggle(self):
        self.open = not self.open

    def close_rect(self, panel_rect):
        return pygame.Rect(panel_rect.right - 38, panel_rect.y + 12, 24, 24)

    def handle_event(self, event, screen_rect, top, bottom):
        if not self.open:
            return False
        rect = self.panel_rect(screen_rect, top, bottom)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.close_rect(rect).collidepoint(event.pos):
                self.open = False
                return True
            if rect.collidepoint(event.pos):
                return True
        elif hasattr(pygame, "MOUSEWHEEL") and event.type == pygame.MOUSEWHEEL:
            line_h = 24
            max_lines = max(1, (rect.height - 70) // line_h)
            max_scroll = max(0, len(self.entries) - max_lines)
            self.scroll_offset = max(0, min(max_scroll, self.scroll_offset + event.y))
            return True
        return False

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
        crect = self.close_rect(rect)
        theme.rounded_rect(surface, crect, PANEL_LIGHT, radius=6)
        theme.text(surface, "×", theme.get_font(18, True), MUTED,
                   center=crect.center)
        pygame.draw.line(surface, PANEL_LIGHT, (rect.x + 18, rect.y + 46),
                         (rect.right - 18, rect.y + 46), 2)
        font = theme.get_font(16)
        line_h = 24
        max_lines = max(1, (rect.height - 70) // line_h)
        max_scroll = max(0, len(self.entries) - max_lines)
        offset = max(0, min(max_scroll, self.scroll_offset))
        end_idx = len(self.entries) - offset
        start_idx = max(0, end_idx - max_lines)
        shown = self.entries[start_idx:end_idx]
        y = rect.y + 58
        for i, entry in enumerate(shown):
            theme.text(surface, f"{start_idx + i + 1}. {entry}", font, MUTED,
                       topleft=(rect.x + 18, y))
            y += line_h

