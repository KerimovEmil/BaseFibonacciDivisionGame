import pygame
import pygame.locals as keys
import sys
from settings import BLOCK_SIZE
from draw_grid import DrawGrid
from background import Background


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

    def reset_screen_and_redraw_grid(self):
        self.grid.screen.fill((255, 255, 255))
        Background(self.screen)
        DrawGrid(self.grid, self.screen)

    # Define different event states in functions
    def start(self):
        clicked = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == keys.MOUSEMOTION:
                    if clicked:
                        mouse_x, mouse_y = event.pos
                        if dragging_obj:
                            dragging_obj.x = mouse_x + offset_x
                            dragging_obj.y = mouse_y + offset_y
                            self.reset_screen_and_redraw_grid()
                            pygame.draw.circle(self.grid.screen, 'blue', dragging_obj.center, 0.6 * BLOCK_SIZE / 2)

                    # print("mouse motion")
                if event.type == keys.KEYDOWN:
                    print("keydown")
                if event.type == keys.MOUSEBUTTONDOWN and event.button == 1:
                    print("mouse down")
                    clicked = True
                    dragging_obj = self.mouse_position_collide_with_piece(event)

                    if dragging_obj:
                        mouse_x, mouse_y = event.pos
                        offset_x = dragging_obj.x - mouse_x
                        offset_y = dragging_obj.y - mouse_y

                if event.type == keys.MOUSEBUTTONUP:
                    clicked = False
                    print("mouse up")
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
                _ = cell.ls_circle_obj.pop()
                cell.value -= 1

                return c_obj
