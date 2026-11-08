"""Ensures tests can import and exercise UI/Scene modules even in headless
environments where pygame is not installed, while using real pygame whenever
available (e.g. desktop and GitHub Actions CI).
"""
import sys
import types


def ensure_pygame():
    try:
        import pygame
        return pygame
    except ModuleNotFoundError:
        pass

    pg = types.ModuleType("pygame")
    pg.SRCALPHA = 0x00010000
    pg.BLEND_RGBA_MULT = 0x8
    pg.QUIT = 256
    pg.KEYDOWN = 768
    pg.MOUSEMOTION = 1024
    pg.MOUSEBUTTONDOWN = 1025
    pg.MOUSEBUTTONUP = 1026
    pg.MOUSEWHEEL = 1027

    for ch in "abcdefghijklmnopqrstuvwxyz0123456789":
        setattr(pg, f"K_{ch}", ord(ch))
    pg.K_ESCAPE = 27
    pg.K_RETURN = 13
    pg.K_SPACE = 32
    pg.K_BACKSPACE = 8
    pg.K_LEFT = 1073741904
    pg.K_RIGHT = 1073741903
    pg.K_UP = 1073741906
    pg.K_DOWN = 1073741905

    class Rect:
        def __init__(self, *args):
            if len(args) == 1:
                a = args[0]
                if isinstance(a, Rect):
                    self.x, self.y, self.width, self.height = a.x, a.y, a.width, a.height
                else:
                    self.x, self.y, self.width, self.height = int(a[0]), int(a[1]), int(a[2]), int(a[3])
            elif len(args) == 2:
                (x, y), (w, h) = args
                self.x, self.y, self.width, self.height = int(x), int(y), int(w), int(h)
            elif len(args) == 4:
                self.x, self.y, self.width, self.height = (int(v) for v in args)
            else:
                raise TypeError(f"Invalid Rect args: {args}")

        @property
        def w(self):
            return self.width

        @property
        def h(self):
            return self.height

        @property
        def left(self):
            return self.x

        @property
        def top(self):
            return self.y

        @property
        def right(self):
            return self.x + self.width

        @property
        def bottom(self):
            return self.y + self.height

        @property
        def centerx(self):
            return self.x + self.width // 2

        @property
        def centery(self):
            return self.y + self.height // 2

        @property
        def center(self):
            return (self.centerx, self.centery)

        @center.setter
        def center(self, pt):
            self.x = int(pt[0]) - self.width // 2
            self.y = int(pt[1]) - self.height // 2

        @property
        def topleft(self):
            return (self.x, self.y)

        @topleft.setter
        def topleft(self, pt):
            self.x, self.y = int(pt[0]), int(pt[1])

        @property
        def midleft(self):
            return (self.x, self.centery)

        @midleft.setter
        def midleft(self, pt):
            self.x = int(pt[0])
            self.y = int(pt[1]) - self.height // 2

        @property
        def midbottom(self):
            return (self.centerx, self.bottom)

        @midbottom.setter
        def midbottom(self, pt):
            self.x = int(pt[0]) - self.width // 2
            self.y = int(pt[1]) - self.height

        @property
        def size(self):
            return (self.width, self.height)

        def inflate(self, dx, dy):
            nx = self.x - int(dx) // 2
            ny = self.y - int(dy) // 2
            nw = self.width + int(dx)
            nh = self.height + int(dy)
            return Rect(nx, ny, nw, nh)

        def move(self, dx, dy):
            return Rect(self.x + int(dx), self.y + int(dy), self.width, self.height)

        def collidepoint(self, *args):
            px, py = args[0] if len(args) == 1 else args
            return self.x <= px < self.right and self.y <= py < self.bottom

        def copy(self):
            return Rect(self.x, self.y, self.width, self.height)

    class Surface:
        def __init__(self, size, flags=0):
            self._w = max(1, int(size[0]))
            self._h = max(1, int(size[1]))
            self.flags = flags
            self._alpha = 255

        def get_rect(self, **kwargs):
            r = Rect(0, 0, self._w, self._h)
            for k, v in kwargs.items():
                setattr(r, k, v)
            return r

        def get_size(self):
            return (self._w, self._h)

        def get_width(self):
            return self._w

        def get_height(self):
            return self._h

        def convert(self):
            return self

        def convert_alpha(self):
            return self

        def copy(self):
            s = Surface((self._w, self._h), self.flags)
            s._alpha = self._alpha
            return s

        def set_alpha(self, a):
            self._alpha = a

        def get_alpha(self):
            return self._alpha

        def fill(self, color):
            pass

        def blit(self, src, pos, special_flags=0):
            return Rect(pos[0], pos[1], src._w, src._h) if isinstance(pos, (tuple, list)) else pos

    class Font:
        def __init__(self, face, size):
            self.size_px = size
            self.bold = False

        def set_bold(self, b):
            self.bold = b

        def render(self, text, antialias, color):
            w = max(1, len(str(text)) * max(6, self.size_px // 2))
            return Surface((w, max(1, self.size_px)))

        def size(self, text):
            w = max(1, len(str(text)) * max(6, self.size_px // 2))
            return (w, max(1, self.size_px))

    pg.Rect = Rect
    pg.Surface = Surface
    pg.init = lambda: None
    pg.quit = lambda: None

    font_mod = types.ModuleType("pygame.font")
    font_mod.init = lambda: None
    font_mod.match_font = lambda *a, **kw: None
    font_mod.Font = Font
    pg.font = font_mod

    draw_mod = types.ModuleType("pygame.draw")
    draw_mod.rect = lambda *a, **kw: None
    draw_mod.line = lambda *a, **kw: None
    draw_mod.circle = lambda *a, **kw: None
    draw_mod.polygon = lambda *a, **kw: None
    draw_mod.arc = lambda *a, **kw: None
    pg.draw = draw_mod

    display_mod = types.ModuleType("pygame.display")
    display_mod.set_mode = lambda size, *a, **kw: Surface(size)
    display_mod.set_caption = lambda *a, **kw: None
    display_mod.set_icon = lambda *a, **kw: None
    display_mod.flip = lambda: None
    pg.display = display_mod

    mouse_mod = types.ModuleType("pygame.mouse")
    mouse_mod.get_pos = lambda: (0, 0)
    pg.mouse = mouse_mod

    mixer_mod = types.ModuleType("pygame.mixer")
    mixer_mod.init = lambda: None
    mixer_mod.Sound = lambda path: types.SimpleNamespace(set_volume=lambda v: None, play=lambda: None)
    pg.mixer = mixer_mod

    time_mod = types.ModuleType("pygame.time")
    time_mod.Clock = lambda: types.SimpleNamespace(tick=lambda fps: 16)
    pg.time = time_mod

    event_mod = types.ModuleType("pygame.event")
    event_mod.get = lambda: []
    event_mod.Event = lambda t, **kw: types.SimpleNamespace(type=t, **kw)
    pg.event = event_mod

    transform_mod = types.ModuleType("pygame.transform")
    transform_mod.rotate = lambda surf, angle: surf
    transform_mod.smoothscale = lambda surf, size: Surface(size)
    pg.transform = transform_mod

    sys.modules["pygame"] = pg
    return pg
