from random import randrange

import pygame

import constant
import game_dynamic_parameters
from Mobs import Slime, Skeleton, Orc, ArmoredOrc, EliteOrc, RiderOrc, ArmoredSkeleton, GreateswordSkeleton, Werewolf, \
    Werebear
from constant import WIDTH, WAVES
from sounds_manager import sounds
from sprite_groups import groups


class WaveManager:
    def __init__(self, board):
        self.wave = 0  # Текущая волна

        try:
            self.waves = WAVES[constant.CURRENT_LVL]
        except KeyError:
            self.waves = []

        self.enemies = pygame.sprite.Group()  # Группа спрайтов для мобов волны
        self.last_spawn_time = pygame.time.get_ticks()
        self.spawn_index = 0  # Индекс текущего моба в волне
        self.current_wave_done = False  # Флаг окончания волны
        self.wave_running = False  # Флаг проигрывания волны
        self.mobs = {'Slime': Slime, 'Skeleton': Skeleton, 'Orc': Orc,
                     'ArmoredOrc': ArmoredOrc, 'EliteOrc': EliteOrc, 'RiderOrc': RiderOrc,
                     'ArmoredSkeleton': ArmoredSkeleton, 'GreateswordSkeleton': GreateswordSkeleton,
                     'Werewolf': Werewolf, 'Werebear': Werebear}

        self.board = board

    def start_wave(self):
        """Проверяет состояние текущей волны и переходит к следующей. Запускает новую волну."""
        if self.current_wave_done and len(self.enemies) == 0:
            game_dynamic_parameters.cash += 150  # Награда за волну
            self.wave += 1
            self.current_wave_done = False
            self.wave_running = False
        else:
            if not self.wave_running:
                if self.wave < len(self.waves):
                    self.spawn_index = 0
                    self.wave_running = True
                    pygame.mixer.Channel(1).play(sounds['wave_start'])
                else:
                    game_dynamic_parameters.GAME_MODE = 'WIN'

    def spawn_enemy(self):
        """Создаёт мобов текущей волны."""
        if self.wave >= len(self.waves) or not self.wave_running:
            return  # Все волны пройдены

        now = pygame.time.get_ticks()
        wave_data = self.waves[self.wave]

        if now - self.last_spawn_time >= wave_data['interval']:  # Спавним разные типы мобов с интервалом
            self.last_spawn_time = now

            try:
                if self.spawn_index < len(wave_data['enemies']):
                    enemy_class = self.mobs[wave_data['enemies'][self.spawn_index][0]]
                    count = wave_data['enemies'][self.spawn_index][1]

                    for _ in range(count):  # Спавним мобов
                        self.spawn_mob(enemy_class)

                    self.spawn_index += 1  # Переходим к следующему типу мобов в волне

                if self.spawn_index >= len(wave_data['enemies']):
                    self.current_wave_done = True  # Все мобы из волны заспавнены
            except Exception:
                pass

    def spawn_mob(self, enemy_class):
        row = randrange(0, self.board.height)
        setting = (
            (WIDTH + randrange(100, 250), row * self.board.cell_size + self.board.top + self.board.cell_size / 2),
            groups['rows'][row])
        enemy = enemy_class(*setting)
        self.enemies.add(enemy)
