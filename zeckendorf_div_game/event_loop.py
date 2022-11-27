import pygame
import pygame.locals as keys
import sys
from zeckendorf_div_game.settings import BLOCK_SIZE
from zeckendorf_div_game.draw_grid import DrawGrid
from zeckendorf_div_game.background import Background
from zeckendorf_div_game.move import Move
from zeckendorf_div_game.play_sound import PlaySound


class EventLoop:
    def __init__(self, game):
        self.game = game

    @property
    def grid(self):
        return self.game.grid

    @property
    def screen(self):
        return self.game.screen

    @property
    def draw_grid(self):
        return self.game.draw_grid

    def increment_moves(self):
        self.game.move_counter.increment()

    def refresh_move_counter(self):
        self.game.move_counter.refresh_screen()

    def reset_screen_and_redraw_grid(self):
        self.grid.screen.fill((255, 255, 255))
        Background(self.screen)
        DrawGrid(self.grid, self.screen)

        self.refresh_move_counter()

        if self.grid.is_win():
            PlaySound("WIN_GAME")

    @staticmethod
    def quit():
        pygame.quit()
        sys.exit()

    @staticmethod
    def key_down():
        print("key down")

    def mouse_motion(self, event, clicked, clicked_cell, offset_x, offset_y):
        """Returns the x and y position of the mouse plus offset"""
        pos_x, pos_y = None, None

        if clicked:
            mouse_x, mouse_y = event.pos
            if clicked_cell:
                pos_x = mouse_x + offset_x
                pos_y = mouse_y + offset_y
                self.reset_screen_and_redraw_grid()
                pygame.draw.circle(self.grid.screen, 'blue', (pos_x, pos_y), 0.6 * BLOCK_SIZE / 2)

        return pos_x, pos_y

    def mouse_down(self, event):
        """Returns the x and y position of the mouse plus offset"""
        print("mouse down")
        clicked_cell = self.mouse_position_collide_with_piece(event)

        clicked = False
        pos_x = pos_y = offset_x = offset_y = None

        if clicked_cell:
            clicked = True
            mouse_x, mouse_y = event.pos
            offset_x = clicked_cell.rect_obj.center[0] - mouse_x
            offset_y = clicked_cell.rect_obj.center[1] - mouse_y
            pos_x = clicked_cell.rect_obj.center[0]
            pos_y = clicked_cell.rect_obj.center[1]

        return clicked, clicked_cell, pos_x, pos_y, offset_x, offset_y

    def mouse_up_and_clicked(self, clicked_cell, pos_x, pos_y) -> bool:
        """
        Logic of what to do when the circle was let go.
        Args:
            clicked_cell: previous cell that was clicked
            pos_x: the x position of where the circle was dropped
            pos_y: the y position of where the circle was dropped

        Returns: boolean weather the move happened or not

        """
        print("mouse up")
        new_cell = None

        # undo the visual
        clicked_cell.value += 1

        # find cell that user dropped mouse in
        for cell in self.grid.cells():
            if cell.collide_point((pos_x, pos_y)):
                new_cell = cell
                break

        # figure out implied direction (maybe method in move class)
        if clicked_cell.distance(new_cell) != 1:
            return False

        if new_cell.grid_row_pos > clicked_cell.grid_row_pos:
            direction = 'DOWN'
        elif new_cell.grid_row_pos < clicked_cell.grid_row_pos:
            direction = 'UP'
        elif new_cell.grid_col_pos < clicked_cell.grid_col_pos:
            direction = 'LEFT'
        else:
            direction = 'RIGHT'

        print(f'clicked_row:{clicked_cell.grid_row_pos}, clicked_col:{clicked_cell.grid_col_pos},'
              f'new_cell_row:{new_cell.grid_row_pos}, new_cell_col:{new_cell.grid_col_pos},'
              f'direction: {direction}')

        # pass into move class
        moved = Move(self.grid, cell_y=clicked_cell.grid_row_pos, cell_x=clicked_cell.grid_col_pos,
                     direction=direction).make_move()
        print("moved is: ", moved)

        return moved

    def start(self):
        clicked = False
        clicked_cell = None
        offset_x = offset_y = None
        pos_x = pos_y = None

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

                if event.type == keys.MOUSEMOTION:
                    pos_x, pos_y = self.mouse_motion(event, clicked, clicked_cell, offset_x, offset_y)

                if event.type == keys.KEYDOWN:
                    self.key_down()

                if event.type == keys.MOUSEBUTTONDOWN and event.button == 1:
                    clicked, clicked_cell, pos_x, pos_y, offset_x, offset_y = self.mouse_down(event)

                if event.type == keys.MOUSEBUTTONUP and clicked:
                    moved = self.mouse_up_and_clicked(clicked_cell, pos_x, pos_y)

                    clicked = False
                    pos_x = pos_y = offset_x = offset_y = None

                    if moved:
                        self.increment_moves()

                    self.reset_screen_and_redraw_grid()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    self.quit()

            pygame.display.update()

    def mouse_position_collide_with_piece(self, event):

        for cell in self.grid.non_empty_cells():
            if cell.collide_point(event.pos):
                print("COLLISION WITH CIRCLE")
                # create new dragging object
                pygame.draw.circle(self.grid.screen, 'blue', cell.rect_obj.center, 0.6 * BLOCK_SIZE / 2)

                # remove one of the existing circles
                cell.value -= 1
                return cell
