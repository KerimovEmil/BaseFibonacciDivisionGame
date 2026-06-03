"""Render representative game states to PNGs for the README (headless).

Run:  SDL_VIDEODRIVER=dummy python tools/screenshot.py
Output: assets/screenshots/*.png
"""
import os
import sys
import random

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame  # noqa: E402
from zdg.app import App  # noqa: E402
from zdg import solver  # noqa: E402

OUT = "assets/screenshots"


def _frame(app, scene, steps=2, dt=0.016):
    app._scene = scene
    for _ in range(steps):
        scene.update(dt)
        app.screen.blit(app._background, (0, 0))
        scene.draw(app.screen)
    return app.screen


def _save(surface, name):
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, name)
    pygame.image.save(surface, path)
    print("saved", path)


def shoot_menu(app):
    from zdg.scenes.menu_scene import MenuScene
    _save(_frame(app, MenuScene(app), steps=30), "menu.png")


def shoot_tutorial(app):
    from zdg.scenes.tutorial_scene import TutorialScene
    sc = TutorialScene(app)
    sc.page = 1  # the "Split" page with a diagram
    _save(_frame(app, sc, steps=3), "tutorial.png")


def shoot_game(app):
    from zdg.scenes.game_scene import GameScene
    random.seed(11)
    sc = GameScene(app)
    # Select the optimal tile so highlights + the hint arrow agree, showcasing
    # both the valid-move highlighting and the hint feature at once.
    hint = solver.hint(sc.grid.state(), sc.mask)
    if hint:
        hr, hc, _ = hint
        sc._on_press(sc.board.cell_center(hr, hc))
        sc.dragging = False  # keep selection visible (not mid-drag)
        sc.hint_move = hint
    sc.moves = 2
    _save(_frame(app, sc, steps=40), "gameplay.png")


def shoot_win(app):
    from zdg.scenes.game_scene import GameScene
    from zdg.scenes.win_overlay import WinOverlay
    random.seed(11)
    sc = GameScene(app)
    path = solver.solve(sc.grid.state(), sc.mask)
    for (r, c, d) in path:
        sc.grid.apply_move(r, c, d)
    sc.moves = len(path)
    sc.win = WinOverlay(len(path), 42, sc.optimal,
                        on_again=lambda: None, on_menu=lambda: None)
    _save(_frame(app, sc, steps=24, dt=0.03), "win.png")


def main():
    app = App()
    shoot_menu(app)
    shoot_tutorial(app)
    shoot_game(app)
    shoot_win(app)


if __name__ == "__main__":
    main()
