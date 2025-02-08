from random import randrange

from Mobs import *
from constant import WIDTH, CELL_SIZE, TOP, CURRENT_LVL, WAVES
from sprite_groups import row0, row1, row2, row3, row4, row5


class WaveManager:
    def __init__(self):
        self.wave = 0  # Текущая волна
        self.waves = WAVES[CURRENT_LVL]
        self.enemies = pygame.sprite.Group()  # Группа спрайтов для мобов волны
        self.last_spawn_time = pygame.time.get_ticks()
        self.spawn_index = 0  # Индекс текущего моба в волне
        self.current_wave_done = False  # Флаг окончания волны
        self.wave_run = False
        self.rows = {'row0': row0, 'row1': row1, 'row2': row2, 'row3': row3, 'row4': row4, 'row5': row5}

    def start_wave(self):
        """Проверяет состояние текущей волны и переходит к следующей. Запускает новую волну."""
        if self.current_wave_done:
            if len(self.enemies) == 0:
                print(f"Волна {self.wave + 1} завершена")
                self.wave += 1
                self.current_wave_done = False
        else:
            if not self.wave_run:
                if self.wave < len(self.waves):
                    self.spawn_index = 0
                    self.wave_run = True
                    print(f"Началась волна {self.wave + 1}")
                else:
                    print("Все волны пройдены!")

    def spawn_enemy(self):
        """Создаёт мобов в рамках текущей волны."""
        if self.wave >= len(self.waves) or not self.wave_run:
            return  # Все волны пройдены

        now = pygame.time.get_ticks()
        wave_data = self.waves[self.wave]

        if now - self.last_spawn_time >= wave_data['interval']:  # Спавним разные типы мобов с интервалом
            self.last_spawn_time = now

            if self.spawn_index < len(wave_data['enemies']):
                enemy_class, count = wave_data['enemies'][self.spawn_index]

                for _ in range(count):  # Спавним мобов
                    row = randrange(0, 5)
                    setting = (
                        (WIDTH + randrange(100, 250), row * CELL_SIZE + TOP + CELL_SIZE / 2), self.rows[f'row{row}'])
                    enemy = globals()[enemy_class](*setting)
                    print(enemy)
                    self.enemies.add(enemy)

                self.spawn_index += 1  # Переходим к следующему типу мобов в волне

            if self.spawn_index >= len(wave_data['enemies']):
                self.current_wave_done = True  # Все мобы из волны заспавнены
                self.wave_run = False
