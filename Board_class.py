from constant import WIDTH
from sprite_groups import groups
from random import randrange


class Board:
    def __init__(self, width, height, left, top, cell_size):
        """Доска для юнитов."""
        self.width = width
        self.height = height
        self.left = left
        self.top = top
        self.cell_size = cell_size
        self.board = [[0] * width for _ in range(height)]

    def get_click(self, mouse_pos, entity):
        """Обрабатываем клик."""
        cell = self.get_cell(mouse_pos)
        return self.on_click(cell=cell, entity=entity)

    def get_cell(self, mouse_pos):
        """Проверка координат."""
        x, y = mouse_pos
        i = (y - self.top) // self.cell_size
        j = (x - self.left) // self.cell_size
        if 0 <= i < self.height and 0 <= j < self.width:
            return j, i
        else:
            return None

    def on_click(self, entity, cell=None):
        """Спавн юнита/моба."""
        try:
            # Если клетка занята, то вызываем ошибку
            units_coord = tuple(map(lambda s: ((s.rect.centerx - self.left) // self.cell_size,
                                               (s.rect.centery - self.top) // self.cell_size),
                                    groups["characters"]))
            if any(map(lambda coord: coord == cell, units_coord)):
                return False

            # Иначе спавним юнита и возвращаем True
            setting = ((cell[0] * self.cell_size + self.left + self.cell_size / 2,
                        cell[1] * self.cell_size + self.top + self.cell_size / 2),
                       groups['rows'][cell[1]])
            entity(*setting)
            return True
        except Exception:
            return False

    def spawn_mob(self, entity):
        """Спавн мобов."""
        try:
            row = randrange(0, 5)
            setting = ((WIDTH, row * self.cell_size + self.top + self.cell_size / 2), groups['rows'][row])
            entity(*setting)
        except Exception:
            pass
