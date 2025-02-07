from constant import WIDTH
from sprite_groups import *
from random import randrange


class Board:
    def __init__(self, width, height, left, top, cell_size):
        self.width = width
        self.height = height
        self.left = left
        self.top = top
        self.cell_size = cell_size
        self.board = [[0] * width for _ in range(height)]

    def get_click(self, mouse_pos, entity_type, entity):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell=cell, entity_type=entity_type, entity=entity)

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        i = (y - self.top) // self.cell_size
        j = (x - self.left) // self.cell_size
        if 0 <= i < self.height and 0 <= j < self.width:
            return j, i
        else:
            return None

    def on_click(self, entity, entity_type='Orcs', cell=None):
        print(entity)
        if entity_type == 'Troops':
            if cell and all([((soldier.rect.center[0] - self.left) // self.cell_size,
                              (soldier.rect.center[1] - self.top) // self.cell_size) != cell
                             for soldier in characters]):
                setting = ((cell[0] * self.cell_size + self.left + self.cell_size / 2,
                            cell[1] * self.cell_size + self.top + self.cell_size / 2),
                           globals()[f'row{cell[1]}'])
                entity(*setting)

        elif entity_type == 'Orcs':
            for i in range(1):
                row = randrange(0, 5)
                setting = ((WIDTH, row * self.cell_size + self.top + self.cell_size / 2), globals()[f'row{row}'])
                entity(*setting)
