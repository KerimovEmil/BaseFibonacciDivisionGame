class Cell:
    def __init__(self, value=0, row=0, col=0, solution=False):
        self.value = value
        self.row = row
        self.col = col
        self.solution = solution  # true if this cell needs to be part of the final solution
        self.rect_obj = None

        self.is_highlight = False

    def distance(self, other):
        if other is None:
            return None

        return abs(other.row - self.row) + abs(other.col - self.col)

    def change_value(self, add=1):
        self.value += add

    def set_rect_obj(self, rect_obj):
        self.rect_obj = rect_obj

    def collide_point(self, pos):
        """Returns if the position collides with the rectangle object"""
        return self.rect_obj.collidepoint(pos)
