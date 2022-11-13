import pygame
import sys
from settings import TITLE,background_colour,game_width,game_height

class Game:
    def __init__(self,window):
        self.window = window
        self.screen = window.screen
        self.build_initial_game_grid()
    
    def drawGrid(self):
        blockSize = 20  # Set the size of the grid block
        for x in range(0, game_width, blockSize):
            for y in range(0, game_height, blockSize):
                rect = pygame.Rect(x, y, blockSize, blockSize)
                pygame.draw.rect(self.screen, 'black', rect, 1)


    def build_initial_game_grid(self):
        while True:
            self.screen.fill('white')
            self.drawGrid()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    sys.exit()

            pygame.display.update()