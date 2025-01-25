from random import choice

from load_image_func import load_image
from sprite_groups import *
from constant import *
from load_animation_func import load_anim

import pygame


class Unit(pygame.sprite.Sprite):
    def __init__(self, coord, animations, grop_of_row, hp, atk, frame_rate, super_atk=None, area_atk=None):
        super().__init__(all_sprites, characters, grop_of_row)
        self.grop_of_row = grop_of_row
        self.hp = hp
        self.atk = atk

        self.animations = animations
        self.mode = 'idle'
        self.frames = self.animations[self.mode]
        self.frame = 0
        self.life = True
        self.current_target = None
        self.kills = 0
        if super_atk:
            self.super_atk = super_atk
        self.area_atk = area_atk if area_atk else self.atk / 2.5

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

            elif isinstance(self, Knight):
                if self.mode in ['attack01', 'attack02', 'attack03']:

                    area_mob = set()
                    for mob in set(self.grop_of_row):
                        if mob in mobs and mob.life:
                            if pygame.sprite.collide_mask(self, mob):
                                area_mob.add(mob)

                    if self.mode == 'attack01' and self.frame == 5:
                        self.current_target.lose_hp(self.atk, self)

                        for mob in area_mob:
                            mob.lose_hp(self.area_atk, self)

                    elif self.mode == 'attack02' and self.frame in (4, 8):
                        self.current_target.lose_hp(self.atk, self)

                        for mob in area_mob:
                            mob.lose_hp(self.area_atk, self)

                    elif self.mode == 'attack03' and self.frame == 8:
                        self.current_target.lose_hp(self.super_atk, self)

                        for mob in area_mob:
                            mob.lose_hp(self.super_atk / 1.5, self)

                        self.kills = 0

            elif isinstance(self, Wizard):
                if self.mode == 'attack01' and self.frame == 13:
                    for mob in set(self.grop_of_row):
                        if mob in mobs and mob.life:
                            if pygame.sprite.collide_mask(self, mob):
                                mob.lose_hp(self.atk, self)

                if self.mode == 'attack02' and self.frame == 10:
                    for mob in set(self.grop_of_row):
                        if mob in mobs and mob.life:
                            if ((mob.rect.y - HEIGHT_CELL) // CELL_SIZE ==
                             (self.rect.y - HEIGHT_CELL) // CELL_SIZE and
                             (mob.rect.x - WIDTH_CELL) // CELL_SIZE ==
                             (self.rect.x - WIDTH_CELL + 2 * CELL_SIZE) // CELL_SIZE):
                                mob.lose_hp(self.atk, self)

            elif isinstance(self, Lancer):
                if self.mode == 'attack01':
                    self.rect.x += 20
                    for mob in set(self.grop_of_row):
                        if mob in mobs and mob.life and pygame.sprite.collide_mask(self, mob):
                            mob.lose_hp(self.atk, self)

    def lose_hp(self, count, killer=None):
        if self.life:
            self.hp -= count
            if self.hp <= 0:
                self.life = False
                if killer:
                    killer.kills += 1
            self.set_mode('hurt')

    def update(self):

        if self.rect.x < 0 or self.rect.left > WIDTH or self.rect.y < 0 or self.rect.top > HEIGHT:
            self.life = False
            self.kill()

        self.update_animation()
        if not self.life:
            self.set_mode('death')
            if self.frame == len(self.frames) - 1:
                self.kill()


class Archer(Unit):
    def __init__(self, coord, grop_of_row):
        animations = load_anim("assets/animations/Troops/archer/Archer.png", 'troops', 'archer')
        frame_rate = {
            'idle': 250,
            'attack01': 140,
            'attack02': 140,
            'hurt': 100,
            'death': 250,
        }
        super().__init__(coord, animations, grop_of_row, hp=50, atk=10, super_atk=30, frame_rate=frame_rate)

    def update(self):
        super().update()
        if self.life:
            if self.mode == 'hurt' and self.frame == len(self.frames) - 1:
                self.set_mode('idle')

            elif self.mode == 'idle':
                mobs_on_row = []
                for mob in set(self.grop_of_row):
                    if mob in set(mobs) and mob.life and ((mob.rect.y - HEIGHT_CELL) // CELL_SIZE ==
                                                          (self.rect.y - HEIGHT_CELL) // CELL_SIZE):
                        mobs_on_row.append((mob, (mob.rect.x - WIDTH_CELL) // CELL_SIZE))
                if mobs_on_row:
                    mobs_on_row.sort(key=lambda x: x[1])
                    self.current_target = mobs_on_row[0][0]
                    self.set_mode('attack01' if self.kills < 4 else 'attack02')

            elif self.mode in ('attack01', 'attack02') and self.current_target and not self.current_target.life:
                self.current_target = None
                self.set_mode('idle')


class Knight(Unit):
    def __init__(self, coord, grop_of_row):
        animations = load_anim("assets/animations/Troops/knight/Knight.png", 'troops', 'knight')
        frame_rate = {
            'idle': 250,
            'attack01': 135,
            'attack02': 135,
            'attack03': 115,
            'block': 200,
            'hurt': 60,
            'death': 250,
        }
        super().__init__(coord, animations, grop_of_row, hp=80, atk=20, super_atk=40, frame_rate=frame_rate)

    def update(self):
        super().update()
        if self.life:
            if self.mode == 'hurt' and self.frame == len(self.frames) - 1:
                self.set_mode('idle')

            elif self.mode == 'idle':
                for mob in set(self.grop_of_row):
                    if mob in mobs and mob.life and pygame.sprite.collide_mask(self, mob):
                        self.current_target = mob
                        self.set_mode(choice(['attack01', 'attack02'] if self.kills < 4 else ['attack03']))
                        break

            elif self.mode in ('attack01', 'attack02', 'attack03') and self.current_target and not self.current_target.life:
                self.current_target = None
                self.set_mode('idle')


class Lancer(Unit):
    def __init__(self, coord, grop_of_row):
        animations = load_anim("assets/animations/Troops/lancer/Lancer.png", 'troops', 'lancer', scale=(230, 230))
        frame_rate = {
            'idle': 250,
            'attack01': 60,
            'attack02': 135,
            'attack03': 135,
            'attack04': 135,
            'block': 200,
            'hurt': 60,
            'death': 250,
        }
        super().__init__(coord, animations, grop_of_row, hp=100, atk=1000, frame_rate=frame_rate)

    def update(self):
        super().update()
        if self.life:
            if self.mode == 'idle':
                for mob in set(self.grop_of_row):
                    if mob in mobs and mob.life and pygame.sprite.collide_mask(self, mob):
                        self.set_mode('attack01')
                        break


class Wizard(Unit):
    def __init__(self, coord, grop_of_row):
        animations = load_anim("assets/animations/Troops/wizard/Wizard.png", 'troops', 'wizard')
        frame_rate = {
            'idle': 250,
            'attack01': 80,
            'attack02': 120,
            'hurt': 100,
            'death': 250,
        }
        super().__init__(coord, animations, grop_of_row, hp=60, atk=35, frame_rate=frame_rate)

    def update(self):
        super().update()
        if self.life:
            if self.mode == 'hurt' and self.frame == len(self.frames) - 1:
                self.set_mode('idle')

            elif self.mode == 'idle':
                for mob in set(self.grop_of_row):
                    if mob in set(mobs) and mob.life:
                        if pygame.sprite.collide_mask(self, mob):
                            self.current_target = mob
                            self.set_mode('attack01')
                            break
                        if ((mob.rect.y - HEIGHT_CELL) // CELL_SIZE ==
                                (self.rect.y - HEIGHT_CELL) // CELL_SIZE and
                                (mob.rect.x - WIDTH_CELL) // CELL_SIZE ==
                                (self.rect.x - WIDTH_CELL + 2 * CELL_SIZE) // CELL_SIZE):
                            self.current_target = mob
                            self.set_mode('attack02')
                            break

            elif self.mode in ('attack01', 'attack02') and self.current_target and not self.current_target.life:
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
        if self.rect.x < 0 or self.rect.left > WIDTH or self.rect.y < 0 or self.rect.top > HEIGHT:
            self.kill()
        if pygame.sprite.collide_mask(self, self.target):
            self.target.lose_hp(self.damage, self.archer)  # Наносим урон цели
            self.kill()  # Удаляем стрелу
        else:
            self.rect.x += self.v  # Перемещаем стрелу вправо

class FireBall(pygame.sprite.Sprite):
    def __init__(self, archer, v, damage):
        super().__init__(all_sprites, shells)
        pass