from enum import Enum


# Game Start Settings
TITLE = "Fibonacci Base Division Game"
BG_COLOR = (255, 255, 255)
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500
START_X = 80
START_Y = 80
BLOCK_SIZE = 60
DEBUG_MODE = True
SKIP_MENU = True
GAME_ICON_PATH = "assets/fib_bg1.png"

# Background Image Settings. Lower Alpha is more transparent
BG_IMG = "assets/fib_bg1.png"
IMG_ALPHA = 128
# BABY_MODE = True
BABY_MODE = False

#SOUND 
#VALID_SOUND="valid_sound.mp3"
#INVALID_SOUND="invalid_sound.mp3"

class SoundFile:
	VALID_MOVE = "valid_sound.mp3"
	# VALID_MOVE = "win_game_sound.mp3"
	INVALID_MOVE = "invalid_sound.mp3"
	WIN_GAME = "win_game_sound.mp3"
	LOSE_GAME = "lose_game_sound.mp3"
	


