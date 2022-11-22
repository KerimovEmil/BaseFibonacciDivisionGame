import pygame

from grid import Grid
from draw_grid import DrawGrid
from problem import Problem
from background import Background
from event_loop import EventLoop


class Game:
    def __init__(self, window):
        pygame.font.init()

        self.window = window
        self.screen = window.screen

        self.problem = None
        self.grid = None
        self.event_loop = None
        self.background = None
        self.draw_grid = None

    def start_game(self):
        self.screen.fill('white')
        self.problem = self.build_problem()
        self.grid = self.build_grid_instance()
        self.background = self.build_background_image()
        self.draw_grid = self.build_draw_grid_instance()
        self.build_user_event_loop()

    def build_problem(self):
        return Problem()

    def build_grid_instance(self):
        return Grid(
            screen=self.screen,
            width=self.grid_width,
            height=self.grid_height,
            last_row=self.problem_last_row()
        )

    def build_background_image(self):
        return Background(self.screen)

    def build_draw_grid_instance(self):
        return DrawGrid(self.grid, self.screen)

    @property
    def grid_width(self):
        return self.problem.grid_width

    @property
    def grid_height(self):
        return self.problem.grid_height

    def problem_last_row(self):
        return self.problem.grid_last_row()

    def build_user_event_loop(self):
        self.event_loop = EventLoop(self)
        self.event_loop.start()
