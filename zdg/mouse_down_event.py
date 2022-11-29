from zdg.event import Event
from zdg.piece_collision import PieceCollision
from zdg.settings import HIGHLIGHT_MOVES


class MouseDownEvent(Event):
    """
    Handles Mouse Down Event. Attributes Are:
     self.event
     self.event_loop
     self.clicked_piece
    """

    def process_event(self):
        super().process_event()
        if self.event.button != 1:
            return

        self.clicked_piece.cell = PieceCollision(self.event, self.grid).cell

        if self.dragging_piece():
            self.clicked_piece.update_event(self.event)

        self.highlight_possible_moves()

    def highlight_possible_moves(self):
        if HIGHLIGHT_MOVES:
            pass
