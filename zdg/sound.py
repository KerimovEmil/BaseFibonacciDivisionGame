"""Web-safe, mute-able sound. Every call is defensive: if the mixer is
unavailable (e.g. some browser/headless contexts) the game keeps running silently.
"""
import pygame
from zdg.settings import SoundFile, SOUND_ON

_sounds = {}
_ready = False
muted = not SOUND_ON


def init():
    global _ready
    if _ready:
        return
    try:
        pygame.mixer.init()
    except Exception:
        _ready = False
        return
    for name in ("VALID_MOVE", "INVALID_MOVE", "WIN_GAME"):
        base = getattr(SoundFile, name)
        snd = _load(base)
        if snd is not None:
            _sounds[name] = snd
    _ready = True


def _load(base):
    for ext in (".ogg", ".mp3", ".wav"):
        try:
            return pygame.mixer.Sound(base + ext)
        except Exception:
            continue
    return None


def play(name):
    if muted or not _ready:
        return
    snd = _sounds.get(name)
    if snd is None:
        return
    try:
        snd.set_volume(0.6)
        snd.play()
    except Exception:
        pass


def toggle_mute():
    global muted
    muted = not muted
    return muted
