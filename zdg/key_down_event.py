# Separate these into separate files
from zdg.event import Event


class KeyDownEvent(Event):
    def process_event(self):
        super().process_event()
