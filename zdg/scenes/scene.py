"""Base class for all scenes (menu, game, tutorial)."""


class Scene:
    def __init__(self, app):
        self.app = app

    def on_enter(self):
        pass

    def handle_event(self, event):
        pass

    def update(self, dt):
        pass

    def draw(self, surface):
        pass
