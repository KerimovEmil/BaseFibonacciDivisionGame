from font_settings import MOVE_COUNTER_FONT


class MoveCounter:
    def __init__(self, screen):
        self.count = 0
        self.screen = screen
        self.refresh_screen()

    def increment(self):
        self.count += 1

    def decrement(self):
        self.count -= 1

    def reset(self):
        self.count = 0

    def refresh_screen(self):
        img = MOVE_COUNTER_FONT.render(f"Moves: {self.count}", True, 'darkgreen')
        coordinates = 500, 20
        self.screen.blit(img, coordinates)
