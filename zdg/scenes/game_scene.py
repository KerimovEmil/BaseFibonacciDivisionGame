"""The main play scene: board, drag input, smart-help buttons, win handling."""
import pygame
from zdg import theme, sound, solver
from zdg.scenes.scene import Scene
from zdg.scenes.win_overlay import WinOverlay
from zdg.problem import Problem
from zdg.grid import Grid
from zdg.history import History
from zdg.ui.board_view import BoardView
from zdg.ui.button import Button
from zdg.ui import hud
from zdg.settings import (
    WINDOW_WIDTH, WINDOW_HEIGHT, TOP_BAR_H, BOTTOM_BAR_H, BOARD_MARGIN,
    TEXT, MUTED, ACCENT,
)

AUTO_STEP = 0.28      # seconds between auto-solve moves
HINT_SHOW = 3.0       # how long a hint stays lit


class GameScene(Scene):
    def __init__(self, app):
        super().__init__(app)
        self.new_problem()
        self._build_buttons()

    # ----- setup ----------------------------------------------------------
    def new_problem(self):
        self.problem = Problem(difficulty=self.app.difficulty)
        self.grid = Grid(self.problem.grid_width, self.problem.grid_height, self.problem)
        self.board = BoardView(self.grid)
        self.history = History(self.grid.state())
        self.mask = self.grid.solution_mask()
        self.moves = 0
        self.elapsed = 0.0
        self.selected = None
        self.highlight = []
        self.dragging = False
        self.drag_pos = (0, 0)
        self.hint_move = None
        self._hint_timer = 0.0
        self.auto_moves = None
        self._auto_timer = 0.0
        self.move_log = hud.MoveLog()
        self.win = None
        self.optimal = solver.optimal_length(self.grid.state(), self.mask)
        self._layout()

    def on_enter(self):
        self._layout()

    # ----- layout ---------------------------------------------------------
    def _layout(self):
        m = BOARD_MARGIN
        self.top_rect = pygame.Rect(m, 18, WINDOW_WIDTH - 2 * m, TOP_BAR_H)
        self.board_rect = pygame.Rect(
            m, self.top_rect.bottom + 16, WINDOW_WIDTH - 2 * m,
            WINDOW_HEIGHT - self.top_rect.bottom - 16 - BOTTOM_BAR_H - 18)
        self.board.layout(self.board_rect)

    def _build_buttons(self):
        specs = [
            ("Undo", "undo", self.undo),
            ("Redo", "redo", self.redo),
            ("Reset", "reset", self.reset),
            ("Hint", "hint", self.do_hint),
            ("Solve", "solve", self.do_solve),
            ("New", "new", self.new_game),
            ("Sound", "sound", self.toggle_sound),
            ("Log", "menu", self.toggle_log),
            ("Menu", "menu", self.go_menu),
        ]
        m = BOARD_MARGIN
        n = len(specs)
        gap = 10
        total = WINDOW_WIDTH - 2 * m
        bw = (total - gap * (n - 1)) // n
        y = WINDOW_HEIGHT - BOTTOM_BAR_H + 14
        self.buttons = {}
        x = m
        for label, icon, cb in specs:
            self.buttons[label] = Button((x, y, bw, 54), label, on_click=cb, icon=icon)
            x += bw + gap

    # ----- actions --------------------------------------------------------
    def _busy(self):
        return self.auto_moves is not None or self.win is not None

    def undo(self):
        if self._busy():
            return
        state = self.history.undo()
        if state is not None:
            self.grid.set_state(state)
            self.moves = self.history.move_count
            self._clear_selection()
            self.move_log.add("Undo")

    def redo(self):
        if self._busy():
            return
        state = self.history.redo()
        if state is not None:
            self.grid.set_state(state)
            self.moves = self.history.move_count
            self._clear_selection()
            self.move_log.add("Redo")

    def reset(self):
        if self._busy():
            return
        state = self.history.reset_to_initial()
        self.grid.set_state(state)
        self.moves = 0
        self.move_log.clear()
        self._clear_selection()

    def do_hint(self):
        if self._busy():
            return
        move = solver.hint(self.grid.state(), self.mask)
        if move:
            self.hint_move = move
            self._hint_timer = HINT_SHOW

    def do_solve(self):
        if self._busy():
            return
        path = solver.solve(self.grid.state(), self.mask)
        if path:
            self.auto_moves = list(path)
            self._auto_timer = 0.0
            self._clear_selection()

    def new_game(self):
        if self.win is not None:
            self.win = None
        self.new_problem()

    def toggle_sound(self):
        muted = sound.toggle_mute()
        self.buttons["Sound"].icon = "mute" if muted else "sound"

    def toggle_log(self):
        self.move_log.toggle()

    def go_menu(self):
        from zdg.scenes.menu_scene import MenuScene
        self.app.go_to(MenuScene(self.app))

    # ----- move application ----------------------------------------------
    def _apply(self, r, c, direction, log=True):
        if not self.grid.apply_move(r, c, direction):
            sound.play("INVALID_MOVE")
            return False
        self.history.record(self.grid.state())
        self.moves += 1
        sound.play("VALID_MOVE")
        if log:
            self.move_log.add(f"{direction.title()} ({r},{c})")
        self._check_win()
        return True

    def _check_win(self):
        if self.grid.is_win():
            self.app.record_best(self.problem.label, self.moves)
            self.win = WinOverlay(self.moves, self.elapsed, self.optimal,
                                  on_again=self.new_game, on_menu=self.go_menu)
            sound.play("WIN_GAME")

    def _clear_selection(self):
        self.selected = None
        self.highlight = []
        self.dragging = False

    # ----- input ----------------------------------------------------------
    def handle_event(self, event):
        if self.win is not None:
            self.win.handle_event(event)
            return
        for b in self.buttons.values():
            b.handle_event(event)
        if self._busy():
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._on_press(event.pos)
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.drag_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self._on_release(event.pos)
        elif event.type == pygame.KEYDOWN:
            self._on_key(event.key)

    def _on_press(self, pos):
        cell = self.board.cell_at(pos)
        if cell and self.grid.array[cell[0]][cell[1]].value > 0:
            self.selected = cell
            self.dragging = True
            self.drag_pos = pos
            self.highlight = self.grid.legal_targets(*cell)
            self.hint_move = None
        else:
            self._clear_selection()

    def _on_release(self, pos):
        if not self.dragging:
            return
        self.dragging = False
        target = self.board.cell_at(pos)
        if target and target in self.highlight and self.selected:
            self._apply(*self.selected, self._direction(self.selected, target))
            self._clear_selection()
        # otherwise keep selection + highlights so the player still sees options

    def _on_key(self, key):
        if key == pygame.K_u:
            self.undo()
        elif key == pygame.K_r:
            self.redo()
        elif key == pygame.K_h:
            self.do_hint()
        elif key == pygame.K_n:
            self.new_game()
        elif key == pygame.K_ESCAPE:
            self.go_menu()

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

    # ----- update ---------------------------------------------------------
    def update(self, dt):
        self.board.update(dt)
        self.move_log.update(dt)
        for b in self.buttons.values():
            b.update(pygame.mouse.get_pos(), dt)

        self.buttons["Undo"].enabled = self.history.can_undo() and not self._busy()
        self.buttons["Redo"].enabled = self.history.can_redo() and not self._busy()

        if self.win is not None:
            self.win.update(dt)
            return

        self.elapsed += dt
        if self._hint_timer > 0:
            self._hint_timer -= dt
            if self._hint_timer <= 0:
                self.hint_move = None

        if self.auto_moves is not None:
            self._auto_timer -= dt
            if self._auto_timer <= 0:
                if self.auto_moves:
                    r, c, d = self.auto_moves.pop(0)
                    self._apply(r, c, d, log=True)
                    self._auto_timer = AUTO_STEP
                if not self.auto_moves:
                    self.auto_moves = None

    # ----- draw -----------------------------------------------------------
    def draw(self, surface):
        best = self.app.best_scores.get(self.problem.label)
        hud.draw_top_bar(surface, self.top_rect, self.problem.label,
                         self.moves, self.elapsed, best, self.optimal)

        # board panel
        theme.rounded_rect(surface, self.board_rect, (28, 33, 54), radius=16)
        skip = self.selected if self.dragging else None
        drag = None
        if self.dragging and self.selected:
            drag = (self.grid.array[self.selected[0]][self.selected[1]], self.drag_pos)
        self.board.draw(surface, selected=self.selected, highlight=self.highlight,
                        hint=self.hint_move, drag=drag, skip_cell=skip)

        self.move_log.draw(surface, pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT),
                           self.board_rect.y, self.board_rect.bottom)

        for b in self.buttons.values():
            b.draw(surface)

        if self.auto_moves is not None:
            theme.text(surface, "Auto-solving…", theme.get_font(18, True), ACCENT,
                       center=(self.board_rect.centerx, self.board_rect.y + 18))

        if self.win is not None:
            self.win.draw(surface)
