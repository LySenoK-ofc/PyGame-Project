from sprite_groups import map_tiles, characters
from Archer_class import Archer
from Orc_class import Orc
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

    def on_click(self, cell=None, entity='orc'):
        if entity == 'soldier':
            if cell is not None and all([((soldier.rect.center[0] - self.left) // self.cell_size,
                                          (soldier.rect.center[1] - self.top) // self.cell_size) != cell
                                         for soldier in characters]):
                Archer((cell[0] * self.cell_size + self.left + self.cell_size / 2,
                        cell[1] * self.cell_size + self.top + self.cell_size / 2))
                print(cell)
        if entity == 'orc':
            Orc((1000, randrange(0, self.height) * self.cell_size + self.top + self.cell_size / 2))
