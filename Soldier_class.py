from load_image_func import load_image
from random import choice
from sprite_groups import shells, mobs
from constant import CELL_SIZE, HEIGHT_CELL, WIDTH_CELL

import pygame

class Soldier(pygame.sprite.Sprite):
    # Базовое хп солдата
    hp = 50
    # Урон
    atk = 10

    def __init__(self, group, coord):
        super().__init__(group)
        # Словарь анимаций для солдата
        self.animations = {
            'idle': [load_image(f'animations/Soldier/Soldier-Idle/idle{i}.png') for i in range(1, 7)],
            'attack': {
                'attack1': [load_image(f'animations/Soldier/Soldier-Attack01/attack{i}.png') for i in range(1, 7)],
                'attack2': [load_image(f'animations/Soldier/Soldier-Attack02/attack{i}.png') for i in range(1, 7)]},
            'bow_attack': [load_image(f'animations/Soldier/Soldier-Attack03/attack{i}.png') for i in range(1, 10)],
            'hurt': [load_image(f'animations/Soldier/Soldier-Hurt/hurt{i}.png') for i in range(1, 5)],
            'death': [load_image(f'animations/Soldier/Soldier-Death/death{i}.png') for i in range(1, 5)],
        }
        # Устанавливаем начальный режим - "ожидание"
        self.mode = 'idle'

        self.frames = self.animations[self.mode]
        self.frame = 0
        self.life = True
        self.current_target = None

        # Устанавливаем изображение и координаты
        self.image = self.frames[self.frame]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = coord

        # Создаём маску
        self.mask = pygame.mask.from_surface(self.image)

        # Время последнего обновления анимации
        self.last_update = pygame.time.get_ticks()

        # Скорость смены кадров для каждого режима
        self.frame_rate = {
            'idle': 250,
            'attack': 140,
            'bow_attack': 115,
            'hurt': 100,
            'death': 250,
        }

    def set_mode(self, mode):
        # Устанавливаем новый режим
        if mode in ['attack']:
            self.mode = mode
            if mode == 'attack':
                # Выбор случайной атаки
                self.frames = self.animations[self.mode][choice(['attack1', 'attack2'])]
            self.frame = 0  # Сбрасываем текущий кадр
        else:
            # Если режим изменился
            if self.mode != mode:
                self.mode = mode
                self.frames = self.animations[self.mode]
                self.frame = 0  # Сбрасываем текущий кадр

    def update_animation(self):
        # Проверяем, прошло ли достаточно времени для обновления кадра
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate[self.mode]:
            self.last_update = now  # Обновляем время последнего кадра
            # Переход к следующему кадру
            self.frame = (self.frame + 1) % len(self.frames)
            self.image = self.frames[self.frame]  # Обновляем изображение

            # Если режим "стрельба из лука" и определённый кадр
            if self.mode == 'bow_attack' and self.frame == 7:
                Arrow(shells, [self.rect.x, self.rect.y], self.current_target)

            # Если режим "атака" и определённый кадр
            if self.mode == 'attack' and self.frame == 4:
                self.current_target.lose_hp(Soldier.atk)

    def update(self):
        self.update_animation() # Обновляем кадр
        # Если солдат жив
        if self.life:
            # Если режим "получение урона" и завершён последний кадр
            if self.mode == 'hurt' and self.frame == len(self.frames) - 1:
                self.set_mode('idle')  # Возвращаемся в режим "ожидание"

            elif self.mode == 'idle':  # Если режим "ожидание"
                mode = None
                mobs_on_row = []
                # Проверяем мобов в зоне видимости
                for mob in mobs:
                    if pygame.sprite.collide_mask(self, mob):
                        self.current_target = mob  # Устанавливаем цель
                        mode = 'attack'  # Переходим в режим "атака"
                        break
                    elif ((mob.rect.y - HEIGHT_CELL) // CELL_SIZE ==
                          (self.rect.y - HEIGHT_CELL) // CELL_SIZE - 1):
                        mode = 'bow_attack'  # Переходим в режим "стрельба из лука"
                        mobs_on_row.append((mob, (mob.rect.x - WIDTH_CELL) // CELL_SIZE))

                if mode == 'attack':
                    self.set_mode(mode)
                elif mode == 'bow_attack':
                    # Сортируем мобов и устанавливаем ближайшего как цель
                    sorted(mobs_on_row, key=lambda x: x[1])
                    self.current_target = mobs_on_row[0][0]
                    self.set_mode(mode)

            # Если цель мертва, возвращаемся в режим "ожидание"
            if self.mode in ('bow_attack', 'attack') and not self.current_target.life:
                self.set_mode('idle')

        else:  # Если солдат мёртв
            self.set_mode('death')  # Переходим в режим "смерть"
            # Удаляем солдата после завершения анимации смерти
            if self.frame == len(self.frames) - 1:
                self.kill()

    def lose_hp(self, count):
        # Уменьшаем здоровье солдата при получении урона
        if self.life:
            self.hp -= count
            if self.hp <= 0: # Если здоровье меньше или равно 0
                self.life = False  # Солдат умирает
            if self.mode != 'hurt':
                self.set_mode('hurt')  # Переходим в режим "получение урона"


class Arrow(pygame.sprite.Sprite):
    def __init__(self, group, coord, target):
        super().__init__(group)
        # Устанавливаем изображение и маску стрелы
        self.image = load_image('animations/Arrow01(100x100).png')
        self.mask = pygame.mask.from_surface(self.image)
        self.target = target  # Цель для стрелы

        # Устанавливаем начальную позицию стрелы
        self.rect = self.image.get_rect()
        self.rect.x = coord[0] + 50
        self.rect.y = coord[1] + 25

    def update(self, *args, **kwargs):
        # Проверяем столкновение стрелы с целью
        if pygame.sprite.collide_mask(self, self.target):
            self.target.lose_hp(Soldier.atk)  # Наносим урон цели
            self.kill()  # Удаляем стрелу
        else:
            self.rect.x += 12.5  # Перемещаем стрелу вправо
