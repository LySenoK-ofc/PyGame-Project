import pygame

from Archer_class import Archer
from Orc_class import Orc
from constant import CHARACTER_SIZE, MOB_SIZE
from sprite_groups import characters
from random import randrange


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

    def render(self, screen):
        for i in range(self.height):
            for j in range(self.width):
                x = self.left + j * self.cell_size
                y = self.top + i * self.cell_size
                pygame.draw.rect(screen, 'white', (x, y, self.cell_size, self.cell_size), width=1)

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
            if cell is not None and all([(soldier.rect.x, soldier.rect.y) !=
                                         (int(cell[0] * self.cell_size + CHARACTER_SIZE[0] / 2.1 % self.cell_size),
                                          int(cell[1] * self.cell_size + CHARACTER_SIZE[1] / 2 % self.cell_size))
                                         for soldier in characters]):
                Archer((cell[0] * self.cell_size + CHARACTER_SIZE[0] / 2.1 % self.cell_size,
                        cell[1] * self.cell_size + CHARACTER_SIZE[1] / 2 % self.cell_size))
                print(cell)
        if entity == 'orc':
            Orc((1000, randrange(0, self.height) * self.cell_size + MOB_SIZE[1] / 2 % self.cell_size))
