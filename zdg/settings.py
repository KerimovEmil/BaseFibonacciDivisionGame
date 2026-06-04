"""Game-wide tunables: window, layout, difficulty, palette and sound paths."""

# ----- window ------------------------------------------------------------
TITLE = "Fibonacci Division"
GAME_NAME = "Base Fibonacci Division"
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 720
FPS = 60
GAME_ICON_PATH = "assets/fib_bg1.png"

# ----- layout ------------------------------------------------------------
TOP_BAR_H = 96
BOTTOM_BAR_H = 88
BOARD_MARGIN = 36
MAX_BLOCK_SIZE = 96
MIN_BLOCK_SIZE = 44
TILE_GAP = 8            # gap between tiles within a cell
ANIM_MS = 150           # tile move animation duration

# ----- difficulty --------------------------------------------------------
# name -> (lower, upper) bounds for the two random factors
DIFFICULTIES = {
    "Easy": (2, 5),
    "Medium": (4, 8),
    "Hard": (6, 13),
}
DIFFICULTY_ORDER = ["Easy", "Medium", "Hard"]
DEFAULT_DIFFICULTY = "Medium"

# ----- behaviour ---------------------------------------------------------
HIGHLIGHT_MOVES = True
SOUND_ON = True
SOLVER_MAX_NODES = 300_000

# ----- palette (RGB) -----------------------------------------------------
BG_TOP = (22, 26, 44)
BG_BOTTOM = (40, 47, 78)
PANEL = (32, 38, 62)
PANEL_LIGHT = (44, 52, 84)
GRID_LINE = (66, 75, 112)
GRID_CELL = (37, 44, 70)

TEXT = (236, 240, 255)
MUTED = (150, 162, 200)
ACCENT = (126, 158, 255)

# tile gradients (top, bottom)
TILE_LIVE = ((96, 165, 250), (56, 120, 235))      # blue – needs to move
TILE_GOOD = ((52, 211, 153), (16, 168, 120))      # green – correctly placed
TILE_OVER = ((251, 146, 60), (234, 110, 30))      # orange – overfilled target
TILE_TEXT = (255, 255, 255)

TARGET_SLOT = (250, 204, 21)                       # gold dashed target outline
HIGHLIGHT = (167, 243, 208)                        # mint valid-move ring
DRAG_GHOST = (190, 215, 255)

GOOD = (52, 211, 153)
WARN = (251, 146, 60)
DANGER = (248, 113, 113)

# background image overlay
BG_IMG = "assets/fib_bg1.png"
BG_IMG_ALPHA = 26


class SoundFile:
    VALID_MOVE = 'sounds/valid_sound'
    INVALID_MOVE = 'sounds/invalid_sound'
    WIN_GAME = 'sounds/win_game_sound'
