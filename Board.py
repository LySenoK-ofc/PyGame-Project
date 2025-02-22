import game_dynamic_parameters
from constant import WIDTH
from sounds_manager import play_sound, sounds
from sprite_groups import groups
from random import randrange


class Board:
    def __init__(self, cell_size, coord):
        """Доска для юнитов."""
        self.cell_size = cell_size
        self.coord = coord
        self.width, self.height = len(set(x for x, y in self.coord)), len(set(y for x, y in self.coord))
        self.left, self.top = min(self.coord)

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
            if any(map(lambda coord: coord == cell, units_coord)) or game_dynamic_parameters.cash - entity.price < 0:
                return False

            # Иначе спавним юнита и возвращаем True
            setting = ((cell[0] * self.cell_size + self.left + self.cell_size / 2,
                        cell[1] * self.cell_size + self.top + self.cell_size / 2),
                       groups['rows'][cell[1]])
            entity.unit(*setting)
            game_dynamic_parameters.spawn_units += 1
            game_dynamic_parameters.cash -= entity.price
            play_sound(sounds['unit_spawn'])
            return True
        except Exception:
            return False

    def spawn_mob(self, entity):
        """Спавн мобов."""
        try:
            row = randrange(0, self.height)
            setting = ((WIDTH, row * self.cell_size + self.top + self.cell_size / 2), groups['rows'][row])
            entity(*setting)
        except Exception as er:
            print(f'Произошла ошибка! "{er}"')
            pass
