class ClickedPiece:
    def __init__(self, cell=None, event=None):
        self.cell = cell
        self.event = event

    def update_event(self, event):
        self.event = event

    @property
    def row(self):
        return self.cell.row

    @property
    def col(self):
        return self.cell.col
