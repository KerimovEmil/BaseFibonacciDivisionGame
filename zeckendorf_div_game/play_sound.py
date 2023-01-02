from zeckendorf_div_game.settings import SoundFile, VOLUME
from pygame import mixer


class PlaySound:
    def __init__(self, sound: str):
        mixer.init()
        mixer.music.set_volume(VOLUME)
        mixer.music.load(getattr(SoundFile, sound))
        mixer.music.play()
