import pygame
from pygame.locals import *
import sys

from settings import TITLE, BG_COLOR, WINDOW_WIDTH, WINDOW_HEIGHT, START_X, START_Y, BLOCK_SIZE
from settings import DEBUG_MODE
from font_settings import AXIS_FONT

from util import convert_decimal_to_base_fib, get_first_n_zeckendorf_terms
from grid import Grid
from draw_grid import DrawGrid
from problem import Problem
from background import Background
from event_loop import EventLoop
import pdb

class Game:
    def __init__(self, window):
        pygame.font.init()

        self.window = window
        self.screen = window.screen

    def start_game(self):
        self.screen.fill('white')
        self.build_problem()
        self.build_grid_instance()
        self.build_background_image()
        self.build_draw_grid_instance()
        self.build_user_event_loop()

    def build_problem(self):
        self.problem = Problem()

    def build_grid_instance(self):
        self.grid = Grid(
            screen = self.screen,
            width = self.problem_width(),
            height = self.problem_height(),
            last_row = self.problem_last_row()
        )

    def build_background_image(self):
        self.background = Background(self.screen)
        self.background.render()

    def build_draw_grid_instance(self):
        self.draw_grid = DrawGrid(self.grid,self.screen)

    def problem_width(self):
        return self.problem.grid_width()

    def problem_height(self):
        return self.problem.grid_height()

    def problem_last_row(self):
        return self.problem.grid_last_row()

    def build_user_event_loop(self):
    	self.event_loop = EventLoop(self)
    	self.event_loop.start()
















