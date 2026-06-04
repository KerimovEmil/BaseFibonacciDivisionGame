"""An illustrated, navigable walkthrough of the goal and the four moves."""
import pygame
from zdg import theme
from zdg.scenes.scene import Scene
from zdg.ui.button import Button
from zdg.settings import (
    WINDOW_WIDTH, WINDOW_HEIGHT, PANEL, PANEL_LIGHT, TEXT, MUTED, ACCENT,
    TILE_LIVE, TILE_GOOD, TARGET_SLOT,
)


def _mini_tile(surface, center, label, colors=TILE_LIVE, size=58, slot=False):
    rect = pygame.Rect(0, 0, size, size)
    rect.center = center
    if slot:
        layer = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.rect(layer, (*TARGET_SLOT, 200), layer.get_rect(),
                         width=3, border_radius=12)
        surface.blit(layer, rect.topleft)
        return
    theme.draw_shadow(surface, rect, radius=12, spread=6, alpha=70)
    tile = theme.tile_surface(size, colors[0], colors[1], radius=12)
    surface.blit(tile, rect.topleft)
    if label is not None:
        theme.text(surface, label, theme.get_font(26, True), (255, 255, 255),
                   center=center)


def _arrow(surface, start, end, color=ACCENT):
    pygame.draw.line(surface, color, start, end, 4)
    pygame.draw.polygon(surface, color, [
        (end[0], end[1]), (end[0] - 12, end[1] - 7), (end[0] - 12, end[1] + 7)])


# Each page: title, list of body lines, and a diagram drawing function.
def _diagram_goal(surface, cx, cy):
    _mini_tile(surface, (cx - 70, cy), None, slot=True)
    _arrow(surface, (cx - 30, cy), (cx + 20, cy))
    _mini_tile(surface, (cx + 70, cy), "1", TILE_GOOD)


def _diagram_split(surface, cx, cy):
    _mini_tile(surface, (cx - 90, cy), "5")
    _arrow(surface, (cx - 48, cy), (cx + 2, cy))
    _mini_tile(surface, (cx + 50, cy), "3")
    _mini_tile(surface, (cx + 112, cy), "2")


def _diagram_merge(surface, cx, cy):
    _mini_tile(surface, (cx - 112, cy), "3")
    _mini_tile(surface, (cx - 50, cy), "2")
    _arrow(surface, (cx - 8, cy), (cx + 42, cy))
    _mini_tile(surface, (cx + 90, cy), "5", TILE_GOOD)


def _diagram_carry(surface, cx, cy):
    _mini_tile(surface, (cx - 100, cy), "1")
    _mini_tile(surface, (cx - 40, cy), "1")
    _arrow(surface, (cx + 2, cy), (cx + 52, cy))
    _mini_tile(surface, (cx + 100, cy), "2", TILE_GOOD)


PAGES = [
    ("The Goal", [
        "Every puzzle is a division:  N = divisor × quotient.",
        "The bottom row starts holding N as Fibonacci tiles.",
        "Slide tiles until each glowing gold slot holds exactly one tile —",
        "that arrangement is the answer.",
    ], _diagram_goal),
    ("Split  ·  Right / Down", [
        "Drag a tile RIGHT or DOWN to split it.",
        "A Fibonacci number becomes the two smaller ones before it:",
        "5 = 3 + 2,   8 = 5 + 3,   and so on.",
    ], _diagram_split),
    ("Merge  ·  Left / Up", [
        "Drag a tile onto its LEFT or UP neighbour to merge.",
        "Two consecutive Fibonacci tiles fuse into the next one:",
        "3 + 2 = 5.   The total value never changes.",
    ], _diagram_merge),
    ("Edge Carry", [
        "On the last column and bottom row, two unit tiles combine:",
        "1 + 1 = 2.   This lets you climb back up the sequence",
        "from the edges of the board.",
    ], _diagram_carry),
    ("Smart Help", [
        "Stuck?  Hint lights the next best move.",
        "Solve plays the full optimal solution automatically.",
        "Undo, Redo and Reset are always available.",
        "Shortcuts: U undo · R redo · H hint · N new · Esc menu.",
    ], None),
]


class TutorialScene(Scene):
    def __init__(self, app):
        super().__init__(app)
        self.page = 0
        cx = WINDOW_WIDTH // 2
        self.prev_btn = Button((cx - 250, WINDOW_HEIGHT - 96, 150, 52), "Back",
                               on_click=self._prev, icon="undo", font_size=20)
        self.next_btn = Button((cx + 100, WINDOW_HEIGHT - 96, 150, 52), "Next",
                               on_click=self._next, kind="primary", font_size=20)
        self.menu_btn = Button((36, WINDOW_HEIGHT - 96, 130, 52), "Menu",
                               on_click=self._menu, kind="ghost", icon="menu",
                               font_size=18)
        self.buttons = [self.prev_btn, self.next_btn, self.menu_btn]

    def _prev(self):
        if self.page > 0:
            self.page -= 1

    def _next(self):
        if self.page < len(PAGES) - 1:
            self.page += 1
        else:
            from zdg.scenes.game_scene import GameScene
            self.app.go_to(GameScene(self.app))

    def _menu(self):
        from zdg.scenes.menu_scene import MenuScene
        self.app.go_to(MenuScene(self.app))

    def handle_event(self, event):
        for b in self.buttons:
            b.handle_event(event)

    def update(self, dt):
        self.prev_btn.enabled = self.page > 0
        self.next_btn.label = "Play" if self.page == len(PAGES) - 1 else "Next"
        self.next_btn.icon = "solve" if self.page == len(PAGES) - 1 else None
        mouse = pygame.mouse.get_pos()
        for b in self.buttons:
            b.update(mouse, dt)

    def draw(self, surface):
        cx = WINDOW_WIDTH // 2
        theme.text(surface, "How to Play", theme.get_font(40, True), TEXT,
                   center=(cx, 70))

        card = pygame.Rect(cx - 380, 130, 760, 420)
        theme.draw_shadow(surface, card, radius=22, spread=16, alpha=90)
        theme.rounded_rect(surface, card, PANEL, radius=22)

        title, lines, diagram = PAGES[self.page]
        theme.text(surface, title, theme.get_font(32, True), ACCENT,
                   center=(cx, card.y + 56))
        y = card.y + 120
        for line in lines:
            theme.text(surface, line, theme.get_font(21), TEXT, center=(cx, y))
            y += 36
        if diagram:
            diagram(surface, cx, card.bottom - 90)

        # page dots
        dots = len(PAGES)
        dx = cx - (dots * 22) // 2 + 11
        for i in range(dots):
            color = ACCENT if i == self.page else PANEL_LIGHT
            pygame.draw.circle(surface, color, (dx + i * 22, card.bottom + 34), 6)

        for b in self.buttons:
            b.draw(surface)
