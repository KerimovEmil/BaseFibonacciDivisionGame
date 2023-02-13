import pygame

from zdg.font_settings import CIRCLE_FONT
from zdg.settings import BLOCK_SIZE


class DrawCircle:
    def __init__(self, cell, screen, colour='red'):
        self.cell = cell
        self.screen = screen
        self.colour = colour

    def draw_circle_in_cell(self, solution=False):
        if solution:
            num_circles = 1
        else:
            num_circles = self.cell.value

        if num_circles in self.num_circles.keys():
            self.num_circles[num_circles](cell=self.cell, screen=self.screen, colour=self.colour)
        else:
            self.one_circle(self.cell, self.screen, self.colour)
            self.number_in_circle(self.cell, self.screen, num_circles)

    @staticmethod
    def zero_circles(cell, screen, colour):
        return

    @staticmethod
    def number_in_circle(cell, screen, num):
        center_pos = cell.rect_obj.center
        x, y = center_pos[0], center_pos[1]
        font_w, font_h = CIRCLE_FONT.size(str(num))
        img = CIRCLE_FONT.render(str(num), True, 'white')
        coordinates = x - font_w // 2, y - font_h // 2

        screen.blit(img, coordinates)

    @staticmethod
    def one_circle(cell, screen, colour):
        center_pos = cell.rect_obj.center
        pygame.draw.circle(screen, colour, center_pos, 0.6 * BLOCK_SIZE / 2)

    @staticmethod
    def two_circles(cell, screen, colour):
        x1 = cell.rect_obj.centerx + cell.rect_obj.size[0] // 6
        y1 = cell.rect_obj.centery + cell.rect_obj.size[1] // 6

        x2 = cell.rect_obj.centerx - cell.rect_obj.size[0] // 6
        y2 = cell.rect_obj.centery - cell.rect_obj.size[1] // 6

        for x, y in ((x1, y1), (x2, y2)):
            pygame.draw.circle(screen, colour, (x, y), 0.5 * BLOCK_SIZE / 2)

    @staticmethod
    def three_circles(cell, screen, colour):
        x1 = cell.rect_obj.centerx
        y1 = cell.rect_obj.centery + cell.rect_obj.size[1] // 6

        x2 = cell.rect_obj.centerx - cell.rect_obj.size[0] // 6
        y2 = cell.rect_obj.centery - cell.rect_obj.size[1] // 6

        x3 = cell.rect_obj.centerx + cell.rect_obj.size[0] // 6
        y3 = cell.rect_obj.centery - cell.rect_obj.size[1] // 6

        for x, y in ((x1, y1), (x2, y2), (x3, y3)):
            pygame.draw.circle(screen, colour, (x, y), 0.4 * BLOCK_SIZE / 2)

    num_circles = {
        0: zero_circles,
        1: one_circle,
        2: two_circles,
        3: three_circles
    }
