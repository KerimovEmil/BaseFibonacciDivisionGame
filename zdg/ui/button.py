"""A rounded button with hover/press animation and an optional drawn glyph icon."""
import pygame
from zdg import theme
from zdg.settings import PANEL_LIGHT, ACCENT, TEXT, MUTED


def _lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


class Button:
    def __init__(self, rect, label, on_click=None, kind="normal",
                 icon=None, font_size=22, tooltip=None):
        self.rect = pygame.Rect(rect)
        self.label = label
        self.on_click = on_click
        self.kind = kind                # 'normal' | 'primary' | 'ghost'
        self.icon = icon                # name string drawn as a vector glyph
        self.font_size = font_size
        self.tooltip = tooltip
        self.enabled = True
        self._hover = 0.0               # 0..1 animated
        self._press = 0.0
        self._held = False

    # ----- input ----------------------------------------------------------
    def handle_event(self, event):
        if not self.enabled:
            return False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self._held = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            was = self._held
            self._held = False
            if was and self.rect.collidepoint(event.pos):
                if self.on_click:
                    self.on_click()
                return True
        return False

    def update(self, mouse_pos, dt):
        target = 1.0 if (self.enabled and self.rect.collidepoint(mouse_pos)) else 0.0
        self._hover += (target - self._hover) * min(1, dt * 14)
        ptarget = 1.0 if self._held else 0.0
        self._press += (ptarget - self._press) * min(1, dt * 22)

    # ----- draw -----------------------------------------------------------
    def draw(self, surface):
        base = ACCENT if self.kind == "primary" else PANEL_LIGHT
        if self.kind == "ghost":
            base = (base[0] - 8, base[1] - 8, base[2] - 8)
        hover_color = _lerp(base, (255, 255, 255), 0.14 * self._hover)
        color = _lerp(hover_color, (0, 0, 0), 0.12 * self._press)
        if not self.enabled:
            color = _lerp(color, PANEL_LIGHT, 0.6)

        rect = self.rect.move(0, int(2 * self._press))
        if self.enabled:
            theme.draw_shadow(surface, rect, radius=12, offset=(0, 4),
                              spread=7, alpha=70)
        theme.rounded_rect(surface, rect, color, radius=12)
        if self.kind == "primary":
            pygame.draw.rect(surface, _lerp(ACCENT, (255, 255, 255), 0.35),
                             rect, width=1, border_radius=12)

        txt_color = TEXT if self.enabled else MUTED
        cx, cy = rect.center
        if self.icon:
            ix = rect.x + 18
            _draw_icon(surface, self.icon, (ix, cy), txt_color)
            theme.text(surface, self.label, theme.get_font(self.font_size, True),
                       txt_color, midleft=(ix + 18, cy + 1))
        else:
            theme.text(surface, self.label, theme.get_font(self.font_size, True),
                       txt_color, center=(cx, cy + 1))


def _draw_icon(surface, name, center, color):
    """Tiny vector glyphs so buttons read at a glance without a font dependency."""
    cx, cy = center
    if name == "undo":
        pygame.draw.arc(surface, color, (cx - 9, cy - 8, 18, 16), 0.5, 3.6, 2)
        pygame.draw.polygon(surface, color, [(cx - 9, cy - 2), (cx - 4, cy - 7), (cx - 3, cy)])
    elif name == "redo":
        pygame.draw.arc(surface, color, (cx - 9, cy - 8, 18, 16), -0.6, 2.6, 2)
        pygame.draw.polygon(surface, color, [(cx + 9, cy - 2), (cx + 4, cy - 7), (cx + 3, cy)])
    elif name == "reset":
        pygame.draw.arc(surface, color, (cx - 9, cy - 9, 18, 18), 0.7, 6.0, 2)
        pygame.draw.polygon(surface, color, [(cx + 8, cy - 7), (cx + 9, cy - 1), (cx + 3, cy - 4)])
    elif name == "hint":
        pygame.draw.circle(surface, color, (cx, cy - 3), 6, 2)
        pygame.draw.line(surface, color, (cx - 3, cy + 5), (cx + 3, cy + 5), 2)
        pygame.draw.line(surface, color, (cx - 2, cy + 8), (cx + 2, cy + 8), 2)
    elif name == "solve":
        pygame.draw.polygon(surface, color, [(cx - 5, cy - 7), (cx - 5, cy + 7), (cx + 7, cy)])
    elif name == "new":
        pygame.draw.line(surface, color, (cx, cy - 7), (cx, cy + 7), 2)
        pygame.draw.line(surface, color, (cx - 7, cy), (cx + 7, cy), 2)
    elif name == "menu":
        for dy in (-6, 0, 6):
            pygame.draw.line(surface, color, (cx - 7, cy + dy), (cx + 7, cy + dy), 2)
    elif name in ("sound", "mute"):
        pygame.draw.polygon(surface, color, [(cx - 8, cy - 3), (cx - 3, cy - 3),
                                             (cx + 1, cy - 7), (cx + 1, cy + 7),
                                             (cx - 3, cy + 3), (cx - 8, cy + 3)])
        if name == "sound":
            pygame.draw.arc(surface, color, (cx + 1, cy - 7, 12, 14), -0.9, 0.9, 2)
        else:
            pygame.draw.line(surface, color, (cx + 4, cy - 5), (cx + 11, cy + 5), 2)
