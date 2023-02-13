# Game Start Settings
TITLE = "Fibonacci Base Division Game"
GAME_NAME = "Base Fibonacci Division Game"
BG_COLOR = (255, 255, 255)

AXIS_COLOR = "blue"
CIRCLE_COLOR = "blue"

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500
START_X = 80
START_Y = 80
BLOCK_SIZE = 60
DEBUG_MODE = True
SKIP_MENU = True
GAME_ICON_PATH = "./assets/fib_bg1.png"

# Background Image Settings. Lower Alpha is more transparent
BG_IMG = "assets/fib_bg1.png"
IMG_ALPHA = 128
BABY_MODE = False

# Problem setup
LOWER_BOUND = 4
UPPER_BOUND = 10

HIGHLIGHT_MOVES = True

# SOUND
VOLUME = 0.7

class SoundFile:
    VALID_MOVE = './sounds/valid_sound.mp3'
    INVALID_MOVE = './sounds/invalid_sound.mp3'
    WIN_GAME = './sounds/win_game_sound.mp3'
    LOSE_GAME = './sounds/lose_game_sound.mp3'
