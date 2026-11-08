"""Renders the puzzle board: cells, Fibonacci axis labels, target slots, tiles,
valid-move highlights, hints, drag ghost — with subtle pop animations on change.
"""
import math
import pygame
from zdg import theme
from zdg.util import get_first_n_zeckendorf_terms
from zdg.settings import (
    GRID_CELL, GRID_LINE, MUTED, TEXT, TILE_GAP, ANIM_MS,
    TILE_LIVE, TILE_GOOD, TILE_OVER, TILE_TEXT, TARGET_SLOT, HIGHLIGHT, ACCENT,
    MAX_BLOCK_SIZE, MIN_BLOCK_SIZE,
)
from zdg import rules


class BoardView:
    def __init__(self, grid):
        self.grid = grid
        self.block = MAX_BLOCK_SIZE
        self.origin = (0, 0)
        self._rects = {}            # (r, c) -> pygame.Rect
        self._pulse = 0.0
        self._pops = {}             # (r, c) -> remaining seconds
        self._flights = []          # list of dict(src, dst, elapsed, duration)
        self._prev_state = grid.state()

    # ----- layout ---------------------------------------------------------
    def layout(self, area: pygame.Rect):
        """Fit the board (plus a label gutter) inside `area`, centered."""
        gw, gh = self.grid.width, self.grid.height
        gutter = 34  # room for axis labels on right + bottom
        block_w = (area.width - gutter) // gw
        block_h = (area.height - gutter) // gh
        self.block = max(MIN_BLOCK_SIZE, min(MAX_BLOCK_SIZE, block_w, block_h))
        board_w = gw * self.block
        board_h = gh * self.block
        ox = area.x + (area.width - gutter - board_w) // 2
        oy = area.y + (area.height - gutter - board_h) // 2
        self.origin = (ox, oy)
        self._rects = {}
        for r in range(gh):
            for c in range(gw):
                rect = pygame.Rect(ox + c * self.block, oy + r * self.block,
                                   self.block, self.block)
                self._rects[(r, c)] = rect
                self.grid.array[r][c].set_rect_obj(rect)

    def cell_at(self, pos):
        for (r, c), rect in self._rects.items():
            if rect.collidepoint(pos):
                return (r, c)
        return None

    def cell_center(self, r, c):
        return self._rects[(r, c)].center

    def cell_math_info(self, row: int, col: int) -> dict:
        """Return the Fibonacci axis weights and value breakdown for cell ``(row, col)``."""
        col_labels = [int(v) for v in get_first_n_zeckendorf_terms(self.grid.width)[::-1]]
        row_labels = [int(v) for v in get_first_n_zeckendorf_terms(self.grid.height)[::-1]]
        rf = row_labels[row]
        cf = col_labels[col]
        unit = rf * cf
        cell = self.grid.array[row][col]
        count = cell.value
        total = count * unit
        extreme = bool(getattr(self.grid, "extreme", False))
        is_target_row = self.grid.is_target_row(row) if hasattr(self.grid, "is_target_row") else False
        if extreme:
            is_target = bool(is_target_row)
        else:
            is_target = bool(cell.solution)
        summary = f"{rf} × {cf} = {unit}"
        return {
            "row": row,
            "col": col,
            "row_fib": rf,
            "col_fib": cf,
            "unit_value": unit,
            "count": count,
            "total_value": total,
            "is_target": is_target,
            "is_target_row": bool(is_target_row),
            "summary": summary,
        }

    # ----- animation ------------------------------------------------------
    def record_move(self, row: int, col: int, direction: str):
        """Spawn directional split/merge slide animations for a move."""
        h, w = self.grid.height, self.grid.width
        dur = ANIM_MS / 1000.0
        pairs = []
        if direction == "RIGHT":
            if col == w - 2:
                pairs.append(((row, col), (row, col + 1)))
            else:
                pairs.append(((row, col), (row, col + 1)))
                pairs.append(((row, col), (row, col + 2)))
        elif direction == "DOWN":
            if row == h - 2:
                pairs.append(((row, col), (row + 1, col)))
            else:
                pairs.append(((row, col), (row + 1, col)))
                pairs.append(((row, col), (row + 2, col)))
        elif direction == "LEFT":
            if col == w - 1:
                pairs.append(((row, col), (row, col - 1)))
            else:
                pairs.append(((row, col), (row, col - 1)))
                pairs.append(((row, col + 1), (row, col - 1)))
        elif direction == "UP":
            if row == h - 1:
                pairs.append(((row, col), (row - 1, col)))
            else:
                pairs.append(((row, col), (row - 1, col)))
                pairs.append(((row + 1, col), (row - 1, col)))

        for src, dst in pairs:
            if src in self._rects and dst in self._rects:
                self._flights.append({
                    "src": src,
                    "dst": dst,
                    "elapsed": 0.0,
                    "duration": dur,
                })

    def update(self, dt):
        self._pulse += dt
        for key in list(self._pops):
            self._pops[key] -= dt
            if self._pops[key] <= 0:
                del self._pops[key]
        alive = []
        for f in self._flights:
            f["elapsed"] += dt
            if f["elapsed"] < f["duration"]:
                alive.append(f)
        self._flights = alive

    def _detect_changes(self):
        state = self.grid.state()
        for r in range(self.grid.height):
            for c in range(self.grid.width):
                if state[r][c] != self._prev_state[r][c] and state[r][c] > 0:
                    self._pops[(r, c)] = ANIM_MS / 1000
        self._prev_state = state

    # ----- drawing --------------------------------------------------------
    def draw(self, surface, selected=None, highlight=None, hint=None,
             drag=None, skip_cell=None):
        self._detect_changes()
        highlight = highlight or []
        self._draw_cells(surface)
        self._draw_labels(surface)
        self._draw_target_slots(surface)
        self._draw_highlights(surface, highlight)
        if hint:
            self._draw_hint(surface, hint)
        self._draw_tiles(surface, selected, skip_cell)
        self._draw_flights(surface)
        if drag is not None:
            self._draw_drag_ghost(surface, *drag)

    def _draw_cells(self, surface):
        pad = 3
        for (r, c), rect in self._rects.items():
            inner = rect.inflate(-pad * 2, -pad * 2)
            theme.rounded_rect(surface, inner, GRID_CELL, radius=10)
            pygame.draw.rect(surface, GRID_LINE, inner, width=1, border_radius=10)

    def _draw_labels(self, surface):
        ox, oy = self.origin
        gw, gh = self.grid.width, self.grid.height
        col_fibs = get_first_n_zeckendorf_terms(gw)[::-1]
        row_fibs = get_first_n_zeckendorf_terms(gh)[::-1]
        font = theme.get_font(max(13, self.block // 5), True)
        extreme = bool(getattr(self.grid, "extreme", False))
        for c, fib in enumerate(col_fibs):
            cx = ox + c * self.block + self.block // 2
            theme.text(surface, fib, font, MUTED,
                       center=(cx, oy + gh * self.block + 16))
        for r, fib in enumerate(row_fibs):
            cy = oy + r * self.block + self.block // 2
            is_trow = extreme and self.grid.is_target_row(r)
            color = TARGET_SLOT if is_trow else MUTED
            theme.text(surface, fib, font, color,
                       center=(ox + gw * self.block + 16, cy))

    def _draw_target_slots(self, surface):
        if getattr(self.grid, "extreme", False):
            self._draw_target_rows(surface)
            return
        glow = (math.sin(self._pulse * 3) + 1) / 2  # 0..1
        for (r, c), rect in self._rects.items():
            cell = self.grid.array[r][c]
            if cell.solution and cell.value == 0:
                inner = rect.inflate(-12, -12)
                layer = pygame.Surface(inner.size, pygame.SRCALPHA)
                a = int(90 + 90 * glow)
                pygame.draw.rect(layer, (*TARGET_SLOT, a),
                                 layer.get_rect(), width=3, border_radius=10)
                pygame.draw.rect(layer, (*TARGET_SLOT, int(28 + 26 * glow)),
                                 layer.get_rect().inflate(-6, -6), border_radius=8)
                surface.blit(layer, inner.topleft)

    def _draw_target_rows(self, surface):
        """Highlight entire target rows (Extreme mode) without revealing target columns."""
        glow = (math.sin(self._pulse * 3) + 1) / 2  # 0..1
        gw = self.grid.width
        if gw <= 0:
            return
        for r in self.grid.target_rows():
            first_rect = self._rects.get((r, 0))
            last_rect = self._rects.get((r, gw - 1))
            if not first_rect or not last_rect:
                continue
            for c in range(gw):
                cell_rect = self._rects.get((r, c))
                if cell_rect:
                    inner = cell_rect.inflate(-8, -8)
                    cell_layer = pygame.Surface(inner.size, pygame.SRCALPHA)
                    pygame.draw.rect(
                        cell_layer,
                        (*TARGET_SLOT, int(22 + 20 * glow)),
                        cell_layer.get_rect(),
                        border_radius=9,
                    )
                    surface.blit(cell_layer, inner.topleft)

            row_rect = pygame.Rect(
                first_rect.left + 2,
                first_rect.top + 2,
                last_rect.right - first_rect.left - 4,
                first_rect.height - 4,
            )
            band = pygame.Surface(row_rect.size, pygame.SRCALPHA)
            border_alpha = int(115 + 85 * glow)
            pygame.draw.rect(
                band,
                (*TARGET_SLOT, border_alpha),
                band.get_rect(),
                width=3,
                border_radius=12,
            )
            surface.blit(band, row_rect.topleft)

    def _draw_highlights(self, surface, highlight):
        glow = (math.sin(self._pulse * 6) + 1) / 2
        for (r, c) in highlight:
            rect = self._rects.get((r, c))
            if not rect:
                continue
            inner = rect.inflate(-6, -6)
            fill = pygame.Surface(inner.size, pygame.SRCALPHA)
            pygame.draw.rect(fill, (*HIGHLIGHT, int(46 + 34 * glow)),
                             fill.get_rect(), border_radius=10)
            pygame.draw.rect(fill, (*HIGHLIGHT, int(170 + 60 * glow)),
                             fill.get_rect(), width=3, border_radius=10)
            surface.blit(fill, inner.topleft)
            # a soft dot in the center to read as "drop here"
            pygame.draw.circle(surface, (*HIGHLIGHT, 220), rect.center, 5)

    def _draw_hint(self, surface, hint):
        r, c, direction = hint
        rect = self._rects.get((r, c))
        if not rect:
            return
        ring = theme.glow_ring(self.block, ACCENT, alpha=150, thickness=5)
        surface.blit(ring, rect.topleft)
        dr, dc = rules.DELTA[direction]
        start = rect.center
        end = (start[0] + dc * self.block * 0.6, start[1] + dr * self.block * 0.6)
        pygame.draw.line(surface, ACCENT, start, end, 4)
        # arrow head
        ang = math.atan2(end[1] - start[1], end[0] - start[0])
        for off in (2.5, -2.5):
            hx = end[0] - 12 * math.cos(ang - off)
            hy = end[1] - 12 * math.sin(ang - off)
            pygame.draw.line(surface, ACCENT, end, (hx, hy), 4)

    def _tile_colors(self, cell):
        if getattr(self.grid, "extreme", False):
            if self.grid.is_win():
                return TILE_GOOD
            return TILE_LIVE
        if cell.solution and cell.value == 1:
            return TILE_GOOD
        if cell.solution and cell.value > 1:
            return TILE_OVER
        return TILE_LIVE

    def _draw_tiles(self, surface, selected, skip_cell):
        in_flight_dsts = {f["dst"] for f in self._flights}
        for (r, c), rect in self._rects.items():
            cell = self.grid.array[r][c]
            if cell.value <= 0:
                continue
            if skip_cell == (r, c):
                continue
            if (r, c) in in_flight_dsts and cell.value == 1:
                continue
            scale = 1.0
            if (r, c) in self._pops:
                t = self._pops[(r, c)] / (ANIM_MS / 1000)
                scale = 1.0 + 0.18 * t       # pop then settle
            self._blit_tile(surface, rect, cell, scale,
                            outlined=(selected == (r, c)))

    def _draw_flights(self, surface):
        for f in self._flights:
            src_rect = self._rects.get(f["src"])
            dst_rect = self._rects.get(f["dst"])
            if not src_rect or not dst_rect:
                continue
            raw_t = min(1.0, max(0.0, f["elapsed"] / max(0.001, f["duration"])))
            # Cubic ease-out
            t = 1.0 - (1.0 - raw_t) ** 3
            cx = int(src_rect.centerx + (dst_rect.centerx - src_rect.centerx) * t)
            cy = int(src_rect.centery + (dst_rect.centery - src_rect.centery) * t)
            dst_cell = self.grid.array[f["dst"][0]][f["dst"][1]]
            size = int(self.block - TILE_GAP * 2)
            grad_top, grad_bottom = self._tile_colors(dst_cell)
            tile = theme.tile_surface(size, grad_top, grad_bottom,
                                      radius=max(8, size // 6))
            pos = (cx - size // 2, cy - size // 2)
            theme.draw_shadow(surface, pygame.Rect(*pos, size, size),
                              radius=size // 6, offset=(0, 5), spread=7, alpha=85)
            surface.blit(tile, pos)

    def _blit_tile(self, surface, rect, cell, scale=1.0, outlined=False, alpha=255):
        size = int((self.block - TILE_GAP * 2) * scale)
        grad_top, grad_bottom = self._tile_colors(cell)
        tile = theme.tile_surface(size, grad_top, grad_bottom,
                                  radius=max(8, size // 6))
        if alpha < 255:
            tile = tile.copy()
            tile.set_alpha(alpha)
        pos = (rect.centerx - size // 2, rect.centery - size // 2)
        theme.draw_shadow(surface, pygame.Rect(*pos, size, size),
                          radius=size // 6, offset=(0, 4), spread=6, alpha=70)
        surface.blit(tile, pos)
        if outlined:
            pygame.draw.rect(surface, TEXT, pygame.Rect(*pos, size, size),
                             width=2, border_radius=max(8, size // 6))
        if cell.value > 1:
            theme.text(surface, cell.value,
                       theme.get_font(max(18, size // 2), True),
                       TILE_TEXT, center=rect.center)

    def _draw_drag_ghost(self, surface, cell, pos):
        size = int(self.block - TILE_GAP * 2)
        grad_top, grad_bottom = self._tile_colors(cell)
        tile = theme.tile_surface(size, grad_top, grad_bottom,
                                  radius=max(8, size // 6)).copy()
        tile.set_alpha(210)
        theme.draw_shadow(surface,
                          pygame.Rect(pos[0] - size // 2, pos[1] - size // 2, size, size),
                          radius=size // 6, offset=(0, 8), spread=10, alpha=110)
        surface.blit(tile, (pos[0] - size // 2, pos[1] - size // 2))
        if cell.value > 1:
            theme.text(surface, cell.value,
                       theme.get_font(max(18, size // 2), True),
                       TILE_TEXT, center=pos)

