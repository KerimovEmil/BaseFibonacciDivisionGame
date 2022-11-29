import pygame
import zdg.grid as Grid
import zdg.event as Event
from zdg.settings import CIRCLE_COLOR, BLOCK_SIZE


class PieceCollision:
    def __init__(self, event, grid):
        self.event = event
        self.grid = grid
        self.cell = self.collides_with_piece()

    def collides_with_piece(self):
        for cell in self.grid.non_empty_cells():
            if cell.collide_point(self.event.pos) == False:
                continue
            self.replace_piece_color(cell)
            cell.value -= 1
            return cell

    def replace_piece_color(self, cell):
        print("COLLISION WITH CIRCLE")
        pygame.draw.circle(self.grid.screen, CIRCLE_COLOR, cell.rect_obj.center, 0.6 * BLOCK_SIZE / 2)
