class ShowValidMoves:
    def __init__(self, event, col, row):
        self.event = event
        self.col = col
        self.row = row
        self.left_valid = self.is_left_valid()
        self.right_valid = self.is_right_valid()
        self.top_valid = self.is_top_valid()
        self.bottom_valid = self.is_bottom_valid()

    @property
    def grid(self):
        return self.event.grid

    @property
    def grid(self):
        return self.event.grid

    def is_left_valid(self):
        return False

    def is_right_valid(self):
        return False

    def is_top_valid(self):
        return False

    def is_bottom_valid(self):
        return False
