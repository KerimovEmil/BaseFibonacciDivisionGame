
import pygame
from pygame.locals import * 
from settings import TITLE, BG_COLOR, WINDOW_WIDTH, WINDOW_HEIGHT, START_X, START_Y, BLOCK_SIZE
import pdb

class EventLoop:
    def __init__(self,game):
        self.game = game
        self.screen = game.screen

    @property
    def grid(self):
        return self.game.grid
    
    @property
    def draw_grid(self):
        return self.game.draw_grid

    # Define different event states in functions
    def start(self):
        clicked = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEMOTION:
                    self.mouse_position_collide_with_piece(event)
                    print("mouse motion")
                if event.type == KEYDOWN:
                    print("keydown")
                if event.type == MOUSEBUTTONDOWN:
                    print("mouse down")
                if event.type == MOUSEBUTTONUP:
                    print("mouse up")
                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    sys.exit()

            pygame.display.update()

    def mouse_position_collide_with_piece(self,event):
        # cell_positions = self.grid.cell_positions()
        circle_positions = self.grid.circle_positions()
        for circle,cell in circle_positions:
            if circle.collidepoint(event.pos):
                print("COLLISION WITH CIRCLE")
                pdb.set_trace()
                cell.ls_circle_obj = []
                self.draw_grid.draw_circles()
                pygame.display.update()
                # update screen to 


        # return