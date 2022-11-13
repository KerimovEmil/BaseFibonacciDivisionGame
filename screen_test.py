import pygame

from settings import *
class Game:
	def start_game(self):
		screen = pygame.display.set_mode((game_width, game_height))
		pygame.display.set_caption(TITLE)
		screen.fill(background_colour)
		pygame.display.flip()
		running = True
		while running:
		  for event in pygame.event.get():
		    if event.type == pygame.QUIT:
		      running = False


g = Game()
g.start_game()
