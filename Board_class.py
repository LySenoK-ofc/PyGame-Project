from sprite_groups import *
from Units import Archer, Knight
from Mobs import Orc
from random import randrange
from Map_constructor import Map_tile


class Board:
    def __init__(self, width, height, left, top, cell_size):
        self.width = width
        self.height = height
        self.left = left
        self.top = top
        self.cell_size = cell_size
        self.board = [[0] * width for _ in range(height)]

    def render(self, map_tile):
        for i in range(self.height):
            for j in range(self.width):
                x = self.left + j * self.cell_size
                y = self.top + i * self.cell_size
                Map_tile(map_tiles, [x, y], map_tile)

    def get_click(self, mouse_pos, entity):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell, entity)

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        i = (y - self.top) // self.cell_size
        j = (x - self.left) // self.cell_size
        if 0 <= i < self.height and 0 <= j < self.width:
            return j, i
        else:
            return None

    def on_click(self, cell=None, entity=Orc):
        print(entity)

        if entity == Archer:
            if cell and all([((soldier.rect.center[0] - self.left) // self.cell_size,
                              (soldier.rect.center[1] - self.top) // self.cell_size) != cell
                             for soldier in characters]):
                Archer((cell[0] * self.cell_size + self.left + self.cell_size / 2,
                        cell[1] * self.cell_size + self.top + self.cell_size / 2),
                       grop_of_row=globals()[f'row{cell[1]}'])

        elif entity == Knight:
            if cell and all([((soldier.rect.center[0] - self.left) // self.cell_size,
                              (soldier.rect.center[1] - self.top) // self.cell_size) != cell
                             for soldier in characters]):
                Knight((cell[0] * self.cell_size + self.left + self.cell_size / 2,
                        cell[1] * self.cell_size + self.top + self.cell_size / 2),
                       grop_of_row=globals()[f'row{cell[1]}'])

        elif entity == Orc:
            for i in range(1):
                row = randrange(0, 5)
                Orc((1000, row * self.cell_size + self.top + self.cell_size / 2), grop_of_row=globals()[f'row{row}'])
