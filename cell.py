class Cell:
    def __init__(self, value=0):
        self.value = value
        self.rect_obj = None
        self.ls_circle_obj = []

    def change_value(self, add=1):
        self.value += add

    def set_rect_obj(self, rect_obj):
        self.rect_obj = rect_obj

    def collide_point(self, pos):
        """Returns if the position collides with the rectangle object"""
        return self.rect_obj.collidepoint(pos)
