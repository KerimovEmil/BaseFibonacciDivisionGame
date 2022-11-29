import pygame
from zdg.event import Event
from zdg.settings import BLOCK_SIZE


class MouseMotionEvent(Event):
    def process_event(self):
        super().process_event()

        if not self.dragging_piece():
            return

        self.update_clicked_piece_location(self.event)
        self.update_game_screen()
        self.highlight_selected_piece()

    def highlight_selected_piece(self):
        screen = self.grid.screen
        color = 'blue'
        block_size = 0.6 * BLOCK_SIZE / 2
        pos = (self.event.pos[0], self.event.pos[1])

        pygame.draw.circle(screen, color, pos, block_size)

    def update_clicked_piece_location(self, event):
        self.clicked_piece.update_event(event)
