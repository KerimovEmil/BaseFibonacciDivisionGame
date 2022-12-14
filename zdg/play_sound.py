from zdg.settings import SoundFile
from pygame import mixer


class PlaySound:
    def __init__(self, sound: str):
        mixer.init()
        mixer.music.set_volume(0.7)
        mixer.music.load(getattr(SoundFile, sound))
        mixer.music.play()
