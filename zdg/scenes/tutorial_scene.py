"""An illustrated, navigable walkthrough of the goal and the four moves."""
import pygame
from zdg import theme, sound, solver, rules
from zdg.scenes.scene import Scene
from zdg.problem import Problem
from zdg.grid import Grid
from zdg.ui.board_view import BoardView
from zdg.ui.button import Button
from zdg.settings import (
    WINDOW_WIDTH, WINDOW_HEIGHT, PANEL, PANEL_LIGHT, TEXT, MUTED, ACCENT, GOOD,
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
    ("Try It Yourself  ·  4 = 2 × 2", [
        "Practice right here! Follow the pulsing cyan hint or click/drag tiles",
        "to reach the gold target slot in 3 moves (Split → Carry → Carry).",
    ], "INTERACTIVE"),
    ("Smart Help", [
        "Stuck?  Hint lights the next best move.",
        "Solve plays the full optimal solution automatically.",
        "Undo, Redo and Reset are always available.",
        "Shortcuts: Arrows/WASD move · U undo · R redo · H hint · L log.",
    ], None),
]

INTERACTIVE_PAGE = 4


class TutorialScene(Scene):
    def __init__(self, app):
        super().__init__(app)
        self.page = 0
        cx = WINDOW_WIDTH // 2
        self.card_rect = pygame.Rect(cx - 380, 130, 760, 440)
        self.prev_btn = Button((cx - 250, WINDOW_HEIGHT - 96, 150, 52), "Back",
                               on_click=self._prev, icon="undo", font_size=20)
        self.next_btn = Button((cx + 100, WINDOW_HEIGHT - 96, 150, 52), "Next",
                               on_click=self._next, kind="primary", font_size=20)
        self.menu_btn = Button((36, WINDOW_HEIGHT - 96, 130, 52), "Menu",
                               on_click=self._menu, kind="ghost", icon="menu",
                               font_size=18)
        self.reset_mini_btn = Button(
            (self.card_rect.right - 126, self.card_rect.y + 20, 104, 38),
            "Reset", on_click=self._init_mini_board, icon="reset", font_size=16
        )
        self.buttons = [self.prev_btn, self.next_btn, self.menu_btn]
        self._init_mini_board()

    def _init_mini_board(self):
        self.mini_problem = Problem(lower=2, upper=2)
        self.mini_grid = Grid(
            self.mini_problem.grid_width,
            self.mini_problem.grid_height,
            self.mini_problem,
        )
        self.mini_board = BoardView(self.mini_grid)
        self.mini_area = pygame.Rect(
            self.card_rect.centerx - 200,
            self.card_rect.y + 165,
            400,
            220,
        )
        self.mini_board.layout(self.mini_area)
        self.mini_mask = self.mini_grid.solution_mask()
        self.mini_selected = None
        self.mini_highlight = []
        self.mini_dragging = False
        self.mini_drag_pos = (0, 0)
        self.mini_moves = 0
        self.mini_hint = solver.hint(self.mini_grid.state(), self.mini_mask)

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

    def _dot_centers(self):
        cx = WINDOW_WIDTH // 2
        dots = len(PAGES)
        dx = cx - (dots * 22) // 2 + 11
        y = self.card_rect.bottom + 26
        return [(dx + i * 22, y) for i in range(dots)]

    def _apply_mini_move(self, r, c, direction):
        if not self.mini_grid.apply_move(r, c, direction):
            sound.play("INVALID_MOVE")
            return False
        self.mini_board.record_move(r, c, direction)
        self.mini_moves += 1
        sound.play("WIN_GAME" if self.mini_grid.is_win() else "VALID_MOVE")
        self.mini_selected = None
        self.mini_highlight = []
        self.mini_dragging = False
        if self.mini_grid.is_win():
            self.mini_hint = None
        else:
            self.mini_hint = solver.hint(self.mini_grid.state(), self.mini_mask)
        return True

    @staticmethod
    def _direction(src, dst):
        sr, sc = src
        tr, tc = dst
        if tr < sr:
            return "UP"
        if tr > sr:
            return "DOWN"
        if tc < sc:
            return "LEFT"
        return "RIGHT"

    def handle_event(self, event):
        for b in self.buttons:
            if b.handle_event(event):
                return
        if self.page == INTERACTIVE_PAGE and self.reset_mini_btn.handle_event(event):
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for idx, (dx, dy) in enumerate(self._dot_centers()):
                if (event.pos[0] - dx) ** 2 + (event.pos[1] - dy) ** 2 <= 100:
                    self.page = idx
                    return
            if self.page == INTERACTIVE_PAGE:
                cell = self.mini_board.cell_at(event.pos)
                if self.mini_selected and cell and cell in self.mini_highlight:
                    self._apply_mini_move(
                        *self.mini_selected, self._direction(self.mini_selected, cell)
                    )
                    return
                if cell and self.mini_grid.array[cell[0]][cell[1]].value > 0:
                    self.mini_selected = cell
                    self.mini_highlight = self.mini_grid.legal_targets(*cell)
                    self.mini_dragging = True
                    self.mini_drag_pos = event.pos
                else:
                    self.mini_selected = None
                    self.mini_highlight = []
                    self.mini_dragging = False
        elif event.type == pygame.MOUSEMOTION and self.page == INTERACTIVE_PAGE and self.mini_dragging:
            self.mini_drag_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.page == INTERACTIVE_PAGE:
            if self.mini_dragging:
                self.mini_dragging = False
                target = self.mini_board.cell_at(event.pos)
                if (
                    target
                    and target in self.mini_highlight
                    and self.mini_selected
                    and target != self.mini_selected
                ):
                    self._apply_mini_move(
                        *self.mini_selected, self._direction(self.mini_selected, target)
                    )
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT, getattr(pygame, "K_BACKSPACE", -1)):
                self._prev()
            elif event.key in (pygame.K_RIGHT, pygame.K_SPACE, pygame.K_RETURN):
                self._next()
            elif event.key == pygame.K_ESCAPE:
                self._menu()
            elif self.page == INTERACTIVE_PAGE and event.key == pygame.K_r:
                self._init_mini_board()

    def update(self, dt):
        self.prev_btn.enabled = self.page > 0
        self.next_btn.label = "Play" if self.page == len(PAGES) - 1 else "Next"
        self.next_btn.icon = "solve" if self.page == len(PAGES) - 1 else None
        mouse = pygame.mouse.get_pos()
        for b in self.buttons:
            b.update(mouse, dt)
        if self.page == INTERACTIVE_PAGE:
            self.reset_mini_btn.update(mouse, dt)
            self.mini_board.update(dt)

    def draw(self, surface):
        cx = WINDOW_WIDTH // 2
        theme.text(surface, "How to Play", theme.get_font(40, True), TEXT,
                   center=(cx, 70))

        card = self.card_rect
        theme.draw_shadow(surface, card, radius=22, spread=16, alpha=90)
        theme.rounded_rect(surface, card, PANEL, radius=22)

        title, lines, diagram = PAGES[self.page]
        theme.text(surface, title, theme.get_font(32, True), ACCENT,
                   center=(cx, card.y + 52))
        y = card.y + 104
        for line in lines:
            theme.text(surface, line, theme.get_font(20), TEXT, center=(cx, y))
            y += 32

        if diagram == "INTERACTIVE":
            self.reset_mini_btn.draw(surface)
            skip = self.mini_selected if self.mini_dragging else None
            drag = None
            if self.mini_dragging and self.mini_selected:
                drag = (
                    self.mini_grid.array[self.mini_selected[0]][self.mini_selected[1]],
                    self.mini_drag_pos,
                )
            self.mini_board.draw(
                surface,
                selected=self.mini_selected,
                highlight=self.mini_highlight,
                hint=self.mini_hint,
                drag=drag,
                skip_cell=skip,
            )
            if self.mini_grid.is_win():
                theme.text(
                    surface,
                    f"Solved in {self.mini_moves} moves! You're ready to play!",
                    theme.get_font(18, True),
                    GOOD,
                    center=(cx, card.bottom - 26),
                )
            else:
                theme.text(
                    surface,
                    f"Moves: {self.mini_moves}  ·  Click or drag the highlighted tile",
                    theme.get_font(16, True),
                    MUTED,
                    center=(cx, card.bottom - 26),
                )
        elif diagram:
            diagram(surface, cx, card.bottom - 90)

        # page dots
        for i, (dx, dy) in enumerate(self._dot_centers()):
            color = ACCENT if i == self.page else PANEL_LIGHT
            pygame.draw.circle(surface, color, (dx, dy), 6)

        for b in self.buttons:
            b.draw(surface)
