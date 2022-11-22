import pygame
from settings import START_X, START_Y, BLOCK_SIZE
from font_settings import AXIS_FONT
from util import convert_decimal_to_base_fib, get_first_n_zeckendorf_terms
import pdb
from typing import List
from cell import Cell

import pdb

class Grid:
    def __init__(self, screen:'Screen',width:int,height:int,last_row:List[int]):
        self.screen = screen
        self.width = width
        self.height = height
        self.last_row = last_row

        self.end_x = START_X + self.width * BLOCK_SIZE
        self.end_y = START_Y + self.height * BLOCK_SIZE

        self.build_initial_array_of_cells()
        self.populate_initial_state_of_last_row()
        self.print()
        
    def print(self):
        for row in self.array:
            for cell in row:
                print(cell.value,end="")
            print()

    def build_initial_array_of_cells(self):
        self.array = [[Cell(value=0) for _ in range(self.width)] for _ in range(self.height)]

    def populate_initial_state_of_last_row(self):
        for x, x_pos in enumerate(range(START_X, self.end_x, BLOCK_SIZE)):
            if self.last_row[x] == '1':
                self.array[self.height-1][x].change_value(add=1)

    def get_starting_state_base_10(self):
        self.div, self.quot, self.prod = get_random_problem()


    def populate_problem(self, grid):
       """Add the product fib on the first row"""
 
       for x, x_pos in enumerate(range(START_X, self.end_x, BLOCK_SIZE)):
           if self.last_row[x] == '1':
               self.array[grid.height-1][x].change_value(add=1)

    def cells(self):
        return [cell for row in self.array for cell in row]   

    def cell_positions(self):
        raise NotImplemented

	# Likely want to append full cell object and the position    
    def circle_positions(self):
        res = []
        for cell in self.cells():
            if len(cell.ls_circle_obj) > 0:
                res.append([cell.ls_circle_obj[0],cell])
        return res


    def event_to_cell_positions(self,event):
        raise NotImplemented



 


