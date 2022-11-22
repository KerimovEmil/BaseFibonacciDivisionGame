from settings import WINDOW_WIDTH, WINDOW_HEIGHT, BG_IMG, IMG_ALPHA
import pygame


class Background:
    def __init__(self, screen):
        self.screen = screen

        image = pygame.image.load(BG_IMG).convert_alpha()
        image.set_alpha(IMG_ALPHA)
        bgimage = pygame.transform.scale(image, (WINDOW_WIDTH, WINDOW_HEIGHT))

        self.screen.blit(bgimage, (0, 0))
