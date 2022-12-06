import pygame
from zdg.event import Event


class QuitGameEvent(Event):
    def process_event(self):
        super().process_event()
        pygame.quit()
