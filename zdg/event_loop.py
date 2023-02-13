import pygame
import pygame.locals as keys

from zdg.event import Event
from zdg.quit_game_event import QuitGameEvent
from zdg.key_down_event import KeyDownEvent
from zdg.mouse_down_event import MouseDownEvent
from zdg.mouse_motion_event import MouseMotionEvent
from zdg.mouse_up_event import MouseUpEvent
from zdg.clicked_piece import ClickedPiece


class EventLoop:
    def __init__(self, game):
        self.game = game
        self.clicked_piece = ClickedPiece()

    @property
    def grid(self):
        return self.game.grid

    def get_event_handler(self, event):
        event_handlers = {
            keys.MOUSEMOTION: MouseMotionEvent,
            keys.KEYDOWN: KeyDownEvent,
            keys.MOUSEBUTTONUP: MouseUpEvent,
            keys.MOUSEBUTTONDOWN: MouseDownEvent,
            pygame.QUIT: QuitGameEvent
        }
        handler = event_handlers.get(event.type, Event)

        return handler(event=event, event_loop=self)

    def start(self):
        while True:
            for event in pygame.event.get():
                event_handler = self.get_event_handler(event)
                event_handler.process_event()
            if pygame.get_init():
                pygame.display.update()
            else:
                break
