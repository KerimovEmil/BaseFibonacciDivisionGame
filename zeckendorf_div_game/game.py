import pygame

from zeckendorf_div_game.grid import Grid
from zeckendorf_div_game.draw_grid import DrawGrid
from zeckendorf_div_game.problem import Problem
from zeckendorf_div_game.background import Background
from zeckendorf_div_game.event_loop import EventLoop
from zeckendorf_div_game.move_counter import MoveCounter


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
        self.move_counter = 0
        self.difficulty = window.difficulty
        self.game_over = False

    def start_game(self):
        self.screen.fill('white')
        self.problem = self.build_problem()
        self.grid = self.build_grid_instance()
        self.background = self.build_background_image()
        self.draw_grid = self.build_draw_grid_instance()
        self.move_counter = self.build_move_counter()
        self.build_user_event_loop()

    def build_move_counter(self):
        return MoveCounter(self.screen)

    def build_problem(self):
        return Problem(difficulty=self.difficulty)

    def build_grid_instance(self):
        return Grid(
            screen=self.screen,
            width=self.grid_width,
            height=self.grid_height,
            problem=self.problem
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

    def build_user_event_loop(self):
        self.event_loop = EventLoop(self)
        self.event_loop.start()
