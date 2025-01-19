from load_image_func import load_image
from random import choice
from sprite_groups import shells, mobs, all_sprites, characters
from constant import CELL_SIZE, HEIGHT_CELL, WIDTH_CELL
from load_animations import load_anim

import pygame


class Archer(pygame.sprite.Sprite):
    # Базовое хп солдата
    hp = 50
    # Урон
    atk = 10
    super_atk = 30

    def __init__(self, coord):
        super().__init__(all_sprites, characters)
        # Словарь анимаций для солдата
        self.animations = load_anim("assets/animations/Troops/archer/Archer.png", 'troops', 'archer')
        # Устанавливаем начальный режим - "ожидание"
        self.mode = 'idle'

        self.frames = self.animations[self.mode]
        self.frame = 0
        self.life = True
        self.current_target = None
        self.kills = 0

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
            'attack01': 140,
            'attack02': 140,
            'bow_attack': 115,
            'hurt': 100,
            'death': 250,
        }

    def set_mode(self, mode):
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
            if self.mode == 'attack01' and self.frame == 6:
                Arrow([self.rect.x, self.rect.y], self.current_target, 12.5)
            elif self.mode == 'attack02' and self.frame == 10:
                Arrow([self.rect.x, self.rect.y], self.current_target, 15)

            # # Если режим "атака" и определённый кадр
            # if self.mode in ['attack01', 'attack02'] and self.frame == 4:
            #     self.current_target.lose_hp(Archer.atk)

    def update(self):
        self.update_animation()  # Обновляем кадр
        # Если солдат жив
        if self.life:
            if self.mode == 'hurt' and self.frame == len(self.frames) - 1:
                self.set_mode('idle')  # Возвращаемся в режим "ожидание"

            elif self.mode == 'idle':  # Если режим "ожидание"
                mode = None
                mobs_on_row = []
                for mob in mobs:
                    # if pygame.sprite.collide_mask(self, mob):
                    #     self.current_target = mob  # Устанавливаем цель
                    #     mode = choice(['attack01', 'attack02'])  # Выбираем случайную атаку
                    #     break
                    if ((mob.rect.y - HEIGHT_CELL) // CELL_SIZE ==
                            (self.rect.y - HEIGHT_CELL) // CELL_SIZE):
                        mode = 'bow_attack'
                        mobs_on_row.append((mob, (mob.rect.x - WIDTH_CELL) // CELL_SIZE))

                # if mode in ['attack01', 'attack02']:
                #     self.set_mode(mode)

                if mode == 'bow_attack':
                    sorted(mobs_on_row, key=lambda x: x[1])
                    self.current_target = mobs_on_row[0][0]
                    if self.kills < 6:
                        self.set_mode('attack01')
                    # Супер удар по достижению 6 убийств лучником
                    else:
                        self.kills = 0
                        self.set_mode('attack02')

            if self.mode in ('attack01', 'attack02') and not self.current_target.life:
                self.kills += 1
                self.set_mode('idle')

        else:  # Если солдат мёртв
            self.set_mode('death')  # Переходим в режим "смерть"
            if self.frame == len(self.frames) - 1:
                self.kill()

    def lose_hp(self, count):
        if self.life:
            self.hp -= count
            if self.hp <= 0:  # Если здоровье меньше или равно 0
                self.life = False  # Солдат умирает
            if self.mode != 'hurt':
                self.set_mode('hurt')  # Переходим в режим "получение урона"


class Arrow(pygame.sprite.Sprite):
    def __init__(self, coord, target, v):
        super().__init__(all_sprites, shells)
        # Устанавливаем изображение и маску стрелы
        self.image = load_image(name='assets/animations/Arrow01(100x100).png')
        self.mask = pygame.mask.from_surface(self.image)
        self.target = target  # Цель для стрелы
        self.v = v

        # Устанавливаем начальную позицию стрелы
        self.rect = self.image.get_rect()
        self.rect.x = coord[0] + 50
        self.rect.y = coord[1]

    def update(self, *args, **kwargs):
        # Проверяем столкновение стрелы с целью
        if pygame.sprite.collide_mask(self, self.target):
            # Выбор удара
            if self.v <= 12.5:
                self.target.lose_hp(Archer.atk)  # Наносим урон цели
            else:
                self.target.lose_hp(Archer.super_atk)  # Наносим урон цели
            self.kill()  # Удаляем стрелу
        else:
            self.rect.x += self.v  # Перемещаем стрелу вправо
