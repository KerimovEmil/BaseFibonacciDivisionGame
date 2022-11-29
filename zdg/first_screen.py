import pygame_menu

from zdg.settings import WINDOW_WIDTH, WINDOW_HEIGHT, GAME_NAME


class FirstScreen:
    def __init__(self, window=None, screen=None, skip=False):
        self.window = window
        self.screen = screen
        self.skip = skip
        self.menu = self.create_menu()

    def create_menu(self):
        if self.skip:
            self.window.start_the_game()
            return

        menu = pygame_menu.Menu(
            GAME_NAME,
            WINDOW_WIDTH,
            WINDOW_HEIGHT,
            theme=pygame_menu.themes.THEME_BLUE
        )
        menu.add.text_input('Name :', default='John Doe')
        menu.add.selector('Difficulty :', [('Hard', 1), ('Medium', 2), ('Easy', 3)],
                          onchange=self.window.set_difficulty)
        menu.add.button('Play', self.window.start_the_game)
        menu.add.button('Quit', pygame_menu.events.EXIT)
        menu.mainloop(self.screen)

        return menu
