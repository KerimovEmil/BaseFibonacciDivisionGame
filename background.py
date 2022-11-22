from settings import START_X,START_Y,WINDOW_WIDTH,WINDOW_HEIGHT,BG_IMG,IMG_ALPHA
import pygame
class Background(pygame.sprite.Sprite):
	def __init__(self,screen):
		self.screen = screen
		self.set_image()
		
	def set_image(self):
		image = pygame.image.load(BG_IMG).convert_alpha()
		image.set_alpha(IMG_ALPHA)
		self.bgimage = pygame.transform.scale(image, (WINDOW_WIDTH, WINDOW_HEIGHT))
		self.bgY=0
		self.bgX=0

	def render(self):
		self.screen.blit(self.bgimage,(self.bgX,self.bgY))
