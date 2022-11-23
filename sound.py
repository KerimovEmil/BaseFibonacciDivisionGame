from settings import VALID_SOUND,INVALID_SOUND
from pygame import mixer
class Sound:
	def __init__(self,valid_move:bool):
		self.valid_move = valid_move
		self.play_sound()

	def play_sound(self):
		mixer.init()
		mixer.music.set_volume(0.7)
		if self.valid_move:
			mixer.music.load(VALID_SOUND)
		else:
			mixer.music.load(INVALID_SOUND)

		mixer.music.play()

