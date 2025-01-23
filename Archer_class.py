from random import choice

from load_image_func import load_image
from sprite_groups import shells, mobs, all_sprites, characters
from constant import CELL_SIZE, HEIGHT_CELL, WIDTH_CELL
from load_animations import load_anim

import pygame


class Unit(pygame.sprite.Sprite):
    def __init__(self, coord, animations, hp, atk, super_atk, frame_rate):
        super().__init__(all_sprites, characters)
        self.hp = hp
        self.atk = atk
        self.super_atk = super_atk
        self.animations = animations
        self.mode = 'idle'
        self.frames = self.animations[self.mode]
        self.frame = 0
        self.life = True
        self.current_target = None
        self.kills = 0
        self.image = self.frames[self.frame]
        self.rect = self.image.get_rect(center=coord)
        self.mask = pygame.mask.from_surface(self.image)
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = frame_rate

    def set_mode(self, mode):
        if self.mode != mode:
            self.mode = mode
            self.frames = self.animations[self.mode]
            self.frame = 0

    def update_animation(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate[self.mode]:
            self.last_update = now
            self.frame = (self.frame + 1) % len(self.frames)
            self.image = self.frames[self.frame]

            if isinstance(self, Archer):
                if self.mode == 'attack01' and self.frame == 6:
                    Arrow(self, 12.5, self.atk)
                elif self.mode == 'attack02' and self.frame == 10:
                    Arrow(self, 20, self.super_atk)
                    self.kills = 0
            if isinstance(self, Knight):
                if self.mode == 'attack01' and self.frame == 5:
                    self.current_target.lose_hp(self.atk, self)
                elif self.mode == 'attack02' and self.frame in (4, 8):
                    self.current_target.lose_hp(self.atk, self)
                elif self.mode == 'attack03' and self.frame == 8:
                    self.current_target.lose_hp(self.super_atk, self)
                    self.kills = 0

    def lose_hp(self, count):
        if self.life:
            self.hp -= count
            if self.hp <= 0:
                self.life = False
            if self.mode != 'hurt':
                self.set_mode('hurt')

    def update(self):
        self.update_animation()
        if not self.life:
            self.set_mode('death')
            if self.frame == len(self.frames) - 1:
                self.kill()


class Archer(Unit):
    def __init__(self, coord):
        animations = load_anim("assets/animations/Troops/archer/Archer.png", 'troops', 'archer')
        frame_rate = {
            'idle': 250,
            'attack01': 140,
            'attack02': 140,
            'bow_attack': 115,
            'hurt': 100,
            'death': 250,
        }
        super().__init__(coord, animations, hp=50, atk=10, super_atk=30, frame_rate=frame_rate)

    def update(self):
        super().update()
        # Уникальная логика лучника
        if self.life:
            if self.mode == 'hurt' and self.frame == len(self.frames) - 1:
                self.set_mode('idle')

            if self.mode == 'idle':
                if not self.current_target:
                    mobs_on_row = []
                    for mob in mobs:
                        if ((mob.rect.y - HEIGHT_CELL) // CELL_SIZE ==
                                (self.rect.y - HEIGHT_CELL) // CELL_SIZE):
                            mobs_on_row.append((mob, (mob.rect.x - WIDTH_CELL) // CELL_SIZE))
                    if mobs_on_row:
                        mobs_on_row.sort(key=lambda x: x[1])
                        self.current_target = mobs_on_row[0][0]
                else:
                    self.set_mode('attack01' if self.kills < 6 else 'attack02')

            if self.mode in ('attack01', 'attack02') and not self.current_target.life:
                self.current_target = None
                self.set_mode('idle')


class Knight(Unit):
    def __init__(self, coord):
        animations = load_anim("assets/animations/Troops/knight/Knight.png", 'troops', 'knight')
        frame_rate = {
            'idle': 250,
            'attack01': 135,
            'attack02': 135,
            'attack03': 135,
            'block': 200,
            'hurt': 100,
            'death': 250,
        }
        super().__init__(coord, animations, hp=80, atk=20, super_atk=40, frame_rate=frame_rate)

    def update(self):
        super().update()
        if self.life:
            if self.mode == 'hurt' and self.frame == len(self.frames) - 1:
                self.set_mode('idle')

            if self.mode == 'idle':
                if not self.current_target:
                    for mob in mobs:
                        if pygame.sprite.collide_mask(self, mob):
                            self.current_target = mob
                            break
                else:
                    self.set_mode(choice(['attack01', 'attack02'] if self.kills < 8 else 'attack03'))

            if self.mode in ('attack01', 'attack02', 'attack03') and not self.current_target.life:
                self.current_target = None
                self.set_mode('idle')


class Arrow(pygame.sprite.Sprite):
    def __init__(self, archer, v, damage):
        super().__init__(all_sprites, shells)
        # Устанавливаем изображение и маску стрелы
        self.image = load_image(file='assets/animations/Troops/arrows/Arrow01(100x100).png', scale=(250, 250))
        self.mask = pygame.mask.from_surface(self.image)
        self.target = archer.current_target  # Цель для стрелы
        self.v = v
        self.damage = damage
        self.archer = archer

        # Устанавливаем начальную позицию стрелы
        self.rect = self.image.get_rect(center=archer.rect.center)
        self.rect.x += 5

    def update(self, *args, **kwargs):
        # Проверяем столкновение стрелы с целью
        if pygame.sprite.collide_mask(self, self.target):
            self.target.lose_hp(self.damage, self.archer)  # Наносим урон цели
            self.kill()  # Удаляем стрелу
        else:
            self.rect.x += self.v  # Перемещаем стрелу вправо
