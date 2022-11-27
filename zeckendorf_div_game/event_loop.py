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

    def start(self):
        clicked = False
        moved = None
        clicked_cell = None
        offset_x, offset_y = None, None
        pos_x, pos_y = None, None

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == keys.MOUSEMOTION:
                    if clicked:
                        mouse_x, mouse_y = event.pos
                        if clicked_cell:
                            pos_x = mouse_x + offset_x
                            pos_y = mouse_y + offset_y
                            self.reset_screen_and_redraw_grid()
                            pygame.draw.circle(self.grid.screen, 'blue', (pos_x, pos_y), 0.6 * BLOCK_SIZE / 2)

                if event.type == keys.KEYDOWN:
                    print("keydown")
                if event.type == keys.MOUSEBUTTONDOWN and event.button == 1:
                    print("mouse down")
                    clicked_cell = self.mouse_position_collide_with_piece(event)

                    if clicked_cell:
                        clicked = True
                        mouse_x, mouse_y = event.pos
                        offset_x = clicked_cell.rect_obj.center[0] - mouse_x
                        offset_y = clicked_cell.rect_obj.center[1] - mouse_y
                        pos_x = clicked_cell.rect_obj.center[0]
                        pos_y = clicked_cell.rect_obj.center[1]

                if event.type == keys.MOUSEBUTTONUP and clicked:
                    print("mouse up")
                    clicked = False
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
                        pass
                    else:
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

                    if moved:
                        self.increment_moves()
                        moved = None

                    self.reset_screen_and_redraw_grid()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    sys.exit()

            pygame.display.update()

    def mouse_position_collide_with_piece(self, event):

        for cell in self.grid.non_empty_cells():
            if cell.collide_point(event.pos):
                print("COLLISION WITH CIRCLE")
                # create new dragging object
                c_obj = pygame.draw.circle(self.grid.screen, 'blue', cell.rect_obj.center, 0.6 * BLOCK_SIZE / 2)

                # remove one of the existing circles
                cell.value -= 1
                return cell
