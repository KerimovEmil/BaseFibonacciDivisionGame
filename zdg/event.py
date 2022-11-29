import re
from zdg.update_game_screen import UpdateGameScreen
from zdg.clicked_piece import ClickedPiece


class Event:
    def __init__(self, event=None, event_loop=None):
        self.event = event
        self.event_loop = event_loop

    def __repr__(self):
        return " ".join(re.split('(?<=.)(?=[A-Z])', type(self).__name__))

    def process_event(self):
        pass

    def dragging_piece(self):
        return self.clicked_piece.cell

    def update_game_screen(self):
        UpdateGameScreen(self.event_loop)

    def reset_piece(self):
        self.clicked_piece = ClickedPiece()

    @property
    def mouse_x(self):
        return self.event.pos[0]

    @property
    def mouse_y(self):
        return self.event.pos[1]

    @property
    def grid(self):
        return self.event_loop.grid

    @property
    def clicked_piece(self):
        return self.event_loop.clicked_piece

    @clicked_piece.setter
    def clicked_piece(self, clicked_piece):
        self.event_loop.clicked_piece = clicked_piece
