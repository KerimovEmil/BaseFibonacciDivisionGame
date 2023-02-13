from zdg.background import Background
from zdg.draw_grid import DrawGrid
from zdg.play_sound import PlaySound


class UpdateGameScreen:
    def __init__(self, event_loop):
        self.event_loop = event_loop
        self.make_screen_black()
        self.insert_background_img()
        self.update_game_grid()
        self.update_move_counter()
        self.check_for_win()

    @property
    def grid(self):
        return self.event_loop.grid

    @property
    def screen(self):
        return self.event_loop.grid.screen

    @property
    def move_counter(self):
        return self.event_loop.game.move_counter

    def make_screen_black(self):
        self.screen.fill((255, 255, 255))

    def insert_background_img(self):
        Background(self.screen)

    def update_game_grid(self):
        DrawGrid(self.grid, self.screen)

    def update_move_counter(self):
        self.move_counter.refresh_screen()

    def check_for_win(self):
        if self.grid.is_win():
            PlaySound("WIN_GAME")
