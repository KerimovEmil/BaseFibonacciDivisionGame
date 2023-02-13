from zdg.event import Event
from zdg.clicked_piece import ClickedPiece
from zdg.move import Move


class MouseUpEvent(Event):
    """
    Event: User Releases Mouse. If User was dragging 
    a piece and its been moved to a valid location, we
    can update the logic 

    Args:
        clicked_piece: previous cell that was clicked
        pos_x: the x position of where the circle was dropped
        pos_y: the y position of where the circle was dropped

    Attributes Are: 
         self.event
         self.event_loop
         self.clicked_piece
    """

    def process_event(self):
        super().process_event()
        if not self.dragging_piece():
            return None

        self.new_cell = self.get_new_cell()
        self.reset_clicked_piece_value()

        if self.is_new_cell_a_valid_move():
            self.move_piece_to_new_cell()
        else:
            self.reset_piece()

        self.update_game_screen()

    def is_new_cell_a_valid_move(self):
        return self.clicked_piece.cell.distance(self.new_cell) == 1

    def reset_clicked_piece_value(self):
        self.clicked_piece.cell.value += 1

    def get_new_cell(self):
        for cell in self.event_loop.grid.cells():
            if cell.collide_point((self.mouse_x, self.mouse_y)):
                return cell
        return None

    def move_piece_to_new_cell(self):
        if self.new_cell.row > self.clicked_piece.row:
            direction = 'DOWN'
        elif self.new_cell.row < self.clicked_piece.row:
            direction = 'UP'
        elif self.new_cell.col < self.clicked_piece.col:
            direction = 'LEFT'
        else:
            direction = 'RIGHT'

        # pass into move class
        moved = Move(
            self.grid,
            row=self.clicked_piece.cell.row,
            col=self.clicked_piece.cell.col,
            direction=direction
        ).make_move()

        if moved:
            self.increment_moves()

        self.clicked_piece = ClickedPiece()

    def increment_moves(self):
        self.event_loop.game.move_counter.increment()
