class Cell:
    def __init__(self, value=0, grid_row_pos=0, grid_col_pos=0):
        self.value = value
        self.grid_row_pos = grid_row_pos
        self.grid_col_pos = grid_col_pos
        self.rect_obj = None

    def distance(self, other):
        return abs(other.grid_row_pos - self.grid_row_pos) + abs(other.grid_col_pos - self.grid_col_pos)

    def change_value(self, add=1):
        self.value += add

    def set_rect_obj(self, rect_obj):
        self.rect_obj = rect_obj

    def collide_point(self, pos):
        """Returns if the position collides with the rectangle object"""
        return self.rect_obj.collidepoint(pos)
