from Soldier_class import Soldier
from Map_tiles_class import Map_tile
from sprite_groups import map_tiles, characters


class Board:
    def __init__(self, width, height, left, top, cell_size):
        self.width = width
        self.height = height
        self.left = left
        self.top = top
        self.cell_size = cell_size
        self.board = [[0] * width for _ in range(height)]

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, map_tile):
        for i in range(self.height):
            for j in range(self.width):
                x = self.left + j * self.cell_size
                y = self.top + i * self.cell_size
                Map_tile(map_tiles, [x, y], map_tile)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        i = (y - self.top) // self.cell_size
        j = (x - self.left) // self.cell_size
        if 0 <= i < self.height and 0 <= j < self.width:
            return j, i
        else:
            return None

    def on_click(self, cell):
        if cell is not None and not self.board[cell[1]][cell[0]]:
            Soldier(characters, (cell[0] * self.cell_size + self.left - 120,
                                 cell[1] * self.cell_size + self.top - 120))  # для demo_project Soldier(characters, cell)
            self.board[cell[1]][cell[0]] = 1
        print(cell)
