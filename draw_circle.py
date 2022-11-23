from settings import BLOCK_SIZE
import pygame


class DrawCircle:

    def __init__(self, cell, screen):
        self.cell = cell
        self.screen = screen

    def draw_circle_in_cell(self):
        self.num_circles[self.cell.value](self.cell, self.screen)

    @staticmethod
    def zero_circles(cell, screen):
        return

    @staticmethod
    def one_circle(cell, screen):
        center_pos = cell.rect_obj.center
        circle_obj = pygame.draw.circle(screen, 'red', center_pos, 0.6 * BLOCK_SIZE / 2)

    @staticmethod
    def two_circles(cell, screen):
        x1 = cell.rect_obj.centerx + cell.rect_obj.size[0] // 6
        y1 = cell.rect_obj.centery + cell.rect_obj.size[1] // 6

        x2 = cell.rect_obj.centerx - cell.rect_obj.size[0] // 6
        y2 = cell.rect_obj.centery - cell.rect_obj.size[1] // 6

        for x, y in ((x1, y1), (x2, y2)):
            pygame.draw.circle(screen, 'red', (x, y), 0.5 * BLOCK_SIZE / 2)

    @staticmethod
    def three_circles(cell, screen):
        x1 = cell.rect_obj.centerx
        y1 = cell.rect_obj.centery + cell.rect_obj.size[1] // 6

        x2 = cell.rect_obj.centerx - cell.rect_obj.size[0] // 6
        y2 = cell.rect_obj.centery - cell.rect_obj.size[1] // 6

        x3 = cell.rect_obj.centerx + cell.rect_obj.size[0] // 6
        y3 = cell.rect_obj.centery - cell.rect_obj.size[1] // 6

        for x, y in ((x1, y1), (x2, y2), (x3, y3)):
            pygame.draw.circle(screen, 'red', (x, y), 0.4 * BLOCK_SIZE / 2)

    num_circles = {
        0: zero_circles,
        1: one_circle,
        2: two_circles,
        3: three_circles
    }
