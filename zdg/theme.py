"""Reusable drawing helpers: fonts, gradients, rounded tiles, shadows, glows.

Everything here is pure pygame and works identically on desktop and under
pygbag/WASM (no external font files required — falls back to pygame's builtin
font when a nicer system font is unavailable).
"""
import pygame

_font_cache = {}
_grad_cache = {}
_tile_cache = {}

# Preferred system faces (used for crisp screenshots on desktop); the builtin
# pygame font is the guaranteed fallback (e.g. on the web build).
_PREFERRED = ["Avenir Next", "Helvetica Neue", "Segoe UI", "Arial", "DejaVu Sans"]
_resolved_face = None


def _resolve_face():
    global _resolved_face
    if _resolved_face is not None:
        return _resolved_face
    for name in _PREFERRED:
        path = pygame.font.match_font(name.replace(" ", "").lower())
        if path:
            _resolved_face = path
            return path
    _resolved_face = ""  # signals "use builtin"
    return _resolved_face


def get_font(size: int, bold: bool = False) -> pygame.font.Font:
    key = (size, bold)
    if key in _font_cache:
        return _font_cache[key]
    face = _resolve_face()
    if face:
        font = pygame.font.Font(face, size)
        font.set_bold(bold)
    else:
        font = pygame.font.Font(None, int(size * 1.15))
        font.set_bold(bold)
    _font_cache[key] = font
    return font


def vgradient(size, top_color, bottom_color) -> pygame.Surface:
    """A vertical gradient surface, cached by (size, colors)."""
    key = (size, top_color, bottom_color)
    if key in _grad_cache:
        return _grad_cache[key]
    w, h = size
    surf = pygame.Surface(size).convert()
    for y in range(h):
        t = y / max(1, h - 1)
        color = (
            int(top_color[0] + (bottom_color[0] - top_color[0]) * t),
            int(top_color[1] + (bottom_color[1] - top_color[1]) * t),
            int(top_color[2] + (bottom_color[2] - top_color[2]) * t),
        )
        pygame.draw.line(surf, color, (0, y), (w, y))
    _grad_cache[key] = surf
    return surf


def rounded_rect(surface, rect, color, radius=12, width=0):
    pygame.draw.rect(surface, color, rect, width=width, border_radius=radius)


def draw_shadow(surface, rect, radius=14, offset=(0, 6), spread=10, alpha=90):
    """Soft drop shadow under a rounded rect."""
    rect = pygame.Rect(rect)
    shadow = pygame.Surface(
        (rect.width + spread * 2, rect.height + spread * 2), pygame.SRCALPHA)
    base = pygame.Rect(spread, spread, rect.width, rect.height)
    for i in range(spread, 0, -1):
        a = int(alpha * (i / spread) ** 2 / spread)
        grown = base.inflate(i * 2, i * 2)
        pygame.draw.rect(shadow, (0, 0, 0, a), grown,
                         border_radius=radius + i)
    surface.blit(shadow, (rect.x - spread + offset[0], rect.y - spread + offset[1]))


def tile_surface(size, grad_top, grad_bottom, radius=14) -> pygame.Surface:
    """A rounded tile with a vertical gradient and a soft top sheen."""
    key = (size, grad_top, grad_bottom, radius)
    if key in _tile_cache:
        return _tile_cache[key]
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    grad = vgradient((size, size), grad_top, grad_bottom).convert_alpha()
    mask = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.rect(mask, (255, 255, 255, 255),
                     (0, 0, size, size), border_radius=radius)
    grad.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    surf.blit(grad, (0, 0))
    # top sheen
    sheen = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.rect(sheen, (255, 255, 255, 46),
                     (size * 0.12, size * 0.10, size * 0.76, size * 0.30),
                     border_radius=radius)
    surf.blit(sheen, (0, 0))
    _tile_cache[key] = surf
    return surf


def glow_ring(diameter, color, alpha=130, thickness=4) -> pygame.Surface:
    """A soft circular glow ring used for highlighting valid targets."""
    surf = pygame.Surface((diameter, diameter), pygame.SRCALPHA)
    c = diameter // 2
    for i in range(6, 0, -1):
        a = int(alpha * (i / 6) ** 2 / 6) * thickness
        pygame.draw.circle(surf, (*color, min(255, a)), (c, c), c - i, max(1, i))
    return surf


def text(surface, string, font, color, center=None, topleft=None, midleft=None):
    img = font.render(str(string), True, color)
    rect = img.get_rect()
    if center is not None:
        rect.center = center
    elif topleft is not None:
        rect.topleft = topleft
    elif midleft is not None:
        rect.midleft = midleft
    surface.blit(img, rect)
    return rect
