from random import choice, randint, random

import constant
from Units import Lancer
from all_animations import ANIMATIONS
from sprite_groups import *
import pygame
from constant import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, coord, animations, grop_of_row, frame_rate, hp, atk,hurt_cooldown,
                 attack_radius=None, super_atk=None, armor_hp=None, armor_def=None):
        super().__init__(all_sprites, mobs, grop_of_row)
        self.animations = animations
        self.frame_rate = frame_rate
        self.grop_of_row = grop_of_row
        self.cached_nearby_mobs = None

        # Устанавливаем характеристики
        self.hp = hp
        self.atk = atk

        # Начальный режим
        self.mode = 'walk'
        self.frames = self.animations[self.mode]
        self.frame = 0
        self.life = True
        self.current_target = None
        self.image = self.frames[self.frame]
        self.rect = self.image.get_rect(center=coord)
        self.mask = pygame.mask.from_surface(self.image)
        self.last_update = pygame.time.get_ticks()
        self.armor_hp = armor_hp
        self.hurt_cooldown = hurt_cooldown
        self.hits = 0

        if super_atk:
            self.super_atk = super_atk
        if attack_radius:
            self.attack_radius = attack_radius
        if self.armor_hp:
            self.armor_def = armor_def

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

            if self.current_target:
                if isinstance(self, Orc):
                    if self.mode in ['attack01', 'attack02'] and self.frame == 3:
                        self.current_target.lose_hp(self.atk, armor_dmg=self.atk * 0.1)

                elif isinstance(self, EliteOrc):
                    if self.mode == 'attack01' and self.frame == 4:
                        self.current_target.lose_hp(self.atk, armor_dmg=self.atk * 0.1)
                    elif self.mode == 'attack02' and self.frame in (1, 5, 9):
                        self.current_target.lose_hp(self.super_atk, armor_dmg=self.super_atk * 0.1)
                    elif self.mode == 'attack03' and self.frame == 5:
                        self.current_target.lose_hp(self.super_atk, armor_dmg=self.super_atk * 0.1)

                elif isinstance(self, ArmoredOrc):
                    if self.mode == 'attack01' and self.frame == 4:
                        self.current_target.lose_hp(self.atk, armor_dmg=self.atk * 0.1)
                    elif self.mode == 'attack02' and self.frame == 6:
                        self.current_target.lose_hp(self.atk, armor_dmg=self.atk * 0.1)
                    elif self.mode == 'attack03' and self.frame == 5:
                        self.current_target.lose_hp(self.super_atk, armor_dmg=self.super_atk * 0.1)

                elif isinstance(self, RiderOrc):
                    if self.mode == 'attack01' and self.frame == 4:
                        self.current_target.lose_hp(self.atk, armor_dmg=self.atk * 0.1)
                    elif self.mode == 'attack02' and self.frame == 5:
                        self.current_target.lose_hp(self.atk, armor_dmg=self.atk * 0.1)
                    elif self.mode == 'attack03' and self.frame in (5, 9):
                        self.current_target.lose_hp(self.atk, armor_dmg=self.atk * 0.1)

                elif isinstance(self, Skeleton):
                    if self.mode in ['attack01', 'attack02'] and self.frame == 3:
                        self.current_target.lose_hp(self.atk, armor_dmg=self.atk * 0.1)

                elif isinstance(self, GreateswordSkeleton):
                    if self.mode == 'attack01' and self.frame == 5:
                        self.current_target.lose_hp(self.atk, armor_dmg=self.atk * 0.1)
                    elif self.mode == 'attack02' and self.frame == 7:
                        self.current_target.lose_hp(self.atk, armor_dmg=self.atk * 0.1)
                    elif self.mode == 'attack03' and self.frame == 4:
                        self.current_target.lose_hp(self.atk, armor_dmg=self.atk * 0.1)

                elif isinstance(self, ArmoredSkeleton):
                    if self.mode == 'attack01' and self.frame == 5:
                        self.current_target.lose_hp(self.atk, armor_dmg=self.atk * 0.1)
                    elif self.mode == 'attack02' and self.frame in (1, 4, 7, 9):
                        self.current_target.lose_hp(self.atk, armor_dmg=self.atk * 0.1)

                elif isinstance(self, Slime):
                    if self.mode == 'attack01' and self.frame == 3:
                        self.current_target.lose_hp(self.atk, armor_dmg=self.atk * 0.1)
                    elif self.mode == 'attack02' and self.frame == 8:
                        self.current_target.lose_hp(self.super_atk, armor_dmg=self.super_atk * 0.1)

                elif isinstance(self, Werebear):
                    if self.mode == 'attack01' and self.frame == 5:
                        self.current_target.lose_hp(self.atk, armor_dmg=self.atk * 0.1)
                    elif self.mode == 'attack02' and self.frame in (4, 9):
                        self.current_target.lose_hp(self.atk, armor_dmg=self.atk * 0.1)
                    elif self.mode == 'attack03' and self.frame == 5:
                        self.current_target.lose_hp(self.super_atk, armor_dmg=self.super_atk * 0.1)

                elif isinstance(self, Werewolf):
                    if self.mode == 'attack01' and self.frame == 5:
                        self.current_target.lose_hp(self.atk, armor_dmg=self.atk * 0.1)
                    elif self.mode == 'attack02':
                        if self.frame in (8, 11):
                            self.current_target.lose_hp(self.atk, armor_dmg=self.atk * 0.1)
                        elif self.frame == 6:
                            self.rect.x -= 1.3 * CELL_SIZE

    def lose_hp(self, dmg, armor_dmg=0):
        if self.life:
            self.hits += 1
            if 'block' in self.animations and randint(1, 5) == 1:
                self.set_mode('block')
                self.hp -= dmg / 3
            else:
                if self.hits % 2 == 0:
                    self.set_mode('hurt')
                if self.armor_hp and self.armor_hp > 0:
                    dmg -= dmg * self.armor_def
                    self.armor_hp -= armor_dmg
                self.hp -= dmg
            if self.hp <= 0:
                self.life = False
    def set_target(self, new_target):
        if self.current_target is None:
            self.current_target = new_target

        if abs(self.current_target.rect.x - self.rect.x) > abs(new_target.rect.x - self.rect.x):
            self.current_target = new_target

    def check_target(self):
        if self.current_target.rect.x > self.rect.x or not self.current_target.life:
            self.current_target = None

    def update(self, *args, **kwargs):
        if constant.frame_count % 5 == 0:
            if self.rect.x < 0 or self.rect.left > WIDTH or self.rect.y < 0 or self.rect.top > HEIGHT:
                self.life = False
                self.kill()

            if self.current_target:
                self.check_target()

        self.update_animation()

        if not self.life:
            self.set_mode('death')
            if self.frame == len(self.frames) - 1:
                self.kill()


class Orc(Enemy):
    def __init__(self, coord, grop_of_row):
        frame_rate = {
            'walk': 250,
            'attack01': 250,
            'attack02': 250,
            'hurt': 100,
            'death': 250,
        }
        super().__init__(coord, ANIMATIONS['ORC'], grop_of_row,
                         attack_radius=CELL_SIZE, hp=80, atk=20,
                         frame_rate=frame_rate, hurt_cooldown=2)

    def update(self, *args, **kwargs):
        super().update()
        if self.life:
            if self.mode == 'hurt' and self.frame == len(self.frames) - 1:
                self.set_mode('walk')

            elif self.mode == 'walk':
                if self.current_target and abs(self.rect.x - self.current_target.rect.x) <= self.attack_radius:
                    self.set_mode(choice(['attack01', 'attack02']))
                else:
                    self.rect.x -= 3

            elif self.mode in ['attack01', 'attack02']:
                if self.frame == len(self.frames) - 1:
                    self.set_mode('walk')


class EliteOrc(Enemy):
    def __init__(self, coord, grop_of_row):
        frame_rate = {
            'walk': 250,
            'attack01': 180,
            'attack02': 250,
            'attack03': 150,
            'hurt': 100,
            'death': 250,
        }
        super().__init__(coord, ANIMATIONS['ELITE_ORC'], grop_of_row,
                         attack_radius=CELL_SIZE, hp=120, atk=30, super_atk=50,
                         frame_rate=frame_rate, armor_hp=20, armor_def=0.1, hurt_cooldown=3)

    def update(self, *args, **kwargs):
        super().update()
        if self.life:
            if self.mode == 'hurt' and self.frame == len(self.frames) - 1:
                self.set_mode('walk')

            elif self.mode == 'walk':
                if self.current_target and abs(self.rect.x - self.current_target.rect.x) <= self.attack_radius:
                    self.set_mode('attack01' if random() > 0.20 else choice(['attack02', 'attack03']))
                else:
                    self.rect.x -= 3

            elif self.mode in ['attack01', 'attack02', 'attack03']:
                if self.frame == len(self.frames) - 1:
                    self.set_mode('walk')


class ArmoredOrc(Enemy):
    def __init__(self, coord, grop_of_row):
        frame_rate = {
            'walk': 250,
            'attack01': 150,
            'attack02': 100,
            'attack03': 90,
            'block': 100,
            'hurt': 100,
            'death': 250,
        }
        super().__init__(coord, ANIMATIONS['ARMORED_ORC'], grop_of_row,
                         attack_radius=CELL_SIZE, hp=150, atk=25, super_atk=35,
                         frame_rate=frame_rate, armor_hp=30, armor_def=0.15, hurt_cooldown=4)

    def update(self, *args, **kwargs):
        super().update()
        if self.life:
            if self.mode in ['hurt', 'block'] and self.frame == len(self.frames) - 1:
                self.set_mode('walk')

            elif self.mode == 'walk':
                if self.current_target and abs(self.rect.x - self.current_target.rect.x) <= self.attack_radius:
                    self.set_mode(choice(['attack01', 'attack02']) if random() > 0.2 else 'attack03')
                else:
                    self.rect.x -= 5

            elif self.mode in ['attack01', 'attack02', 'attack03']:
                if self.frame == len(self.frames) - 1:
                    self.set_mode('walk')


class RiderOrc(Enemy):
    def __init__(self, coord, grop_of_row):
        frame_rate = {
            'walk': 250,
            'attack01': 150,
            'attack02': 100,
            'attack03': 90,
            'block': 100,
            'hurt': 100,
            'death': 250,
        }
        super().__init__(coord, ANIMATIONS['RIDER_ORC'], grop_of_row,
                         attack_radius=CELL_SIZE, hp=120, atk=25,
                         frame_rate=frame_rate, armor_hp=40, armor_def=0.2, hurt_cooldown=3)

    def update(self, *args, **kwargs):
        super().update()
        if self.life:
            if self.mode in ['hurt', 'block'] and self.frame == len(self.frames) - 1:
                self.set_mode('walk')

            elif self.mode == 'walk':
                if self.current_target and abs(self.rect.x - self.current_target.rect.x) <= self.attack_radius:
                    self.set_mode(choice(['attack01', 'attack02', 'attack03']))
                else:
                    self.rect.x -= 5

            elif self.mode in ['attack01', 'attack02', 'attack03']:
                if self.frame == len(self.frames) - 1:
                    self.set_mode('walk')


class Skeleton(Enemy):
    def __init__(self, coord, grop_of_row):
        frame_rate = {
            'walk': 250,
            'attack01': 150,
            'attack02': 100,
            'attack03': 90,
            'block': 100,
            'hurt': 100,
            'death': 250,
        }
        super().__init__(coord, ANIMATIONS['SKELETON'], grop_of_row,
                         attack_radius=CELL_SIZE, hp=70, atk=25,
                         frame_rate=frame_rate, hurt_cooldown=2)

    def update(self, *args, **kwargs):
        super().update()
        if self.life:
            if self.mode in ['hurt', 'block'] and self.frame == len(self.frames) - 1:
                self.set_mode('walk')

            elif self.mode == 'walk':
                if self.current_target and abs(self.rect.x - self.current_target.rect.x) <= self.attack_radius:
                    self.set_mode(choice(['attack01', 'attack02']))
                else:
                    self.rect.x -= 5

            elif self.mode in ['attack01', 'attack02']:
                if self.frame == len(self.frames) - 1:
                    self.set_mode('walk')


class GreateswordSkeleton(Enemy):
    def __init__(self, coord, grop_of_row):
        frame_rate = {
            'walk': 250,
            'attack01': 120,
            'attack02': 120,
            'attack03': 120,
            'hurt': 100,
            'death': 250,
        }
        super().__init__(coord, ANIMATIONS['GREATSWORD_SKELETON'], grop_of_row,
                         attack_radius=CELL_SIZE, hp=80, atk=30,
                         frame_rate=frame_rate, armor_hp=45, armor_def=0.2, hurt_cooldown=3)

    def update(self, *args, **kwargs):
        super().update()
        if self.life:
            if self.mode == 'hurt' and self.frame == len(self.frames) - 1:
                self.set_mode('walk')

            elif self.mode == 'walk':
                if self.current_target and abs(self.rect.x - self.current_target.rect.x) <= self.attack_radius:
                    self.set_mode(choice(['attack01', 'attack02', 'attack03']))
                else:
                    self.rect.x -= 5

            elif self.mode in ['attack01', 'attack02', 'attack03']:
                if self.frame == len(self.frames) - 1:
                    self.set_mode('walk')


class ArmoredSkeleton(Enemy):
    def __init__(self, coord, grop_of_row):
        frame_rate = {
            'walk': 250,
            'attack01': 120,
            'attack02': 120,
            'hurt': 100,
            'death': 250,
        }
        super().__init__(coord, ANIMATIONS['ARMORED_SCELETON'], grop_of_row,
                         attack_radius=CELL_SIZE, hp=120, atk=25,
                         frame_rate=frame_rate, armor_hp=50, armor_def=0.25, hurt_cooldown=4)

    def update(self, *args, **kwargs):
        super().update()
        if self.life:
            if self.mode == 'hurt' and self.frame == len(self.frames) - 1:
                self.set_mode('walk')

            elif self.mode == 'walk':
                if self.current_target and abs(self.rect.x - self.current_target.rect.x) <= self.attack_radius:
                    self.set_mode('attack01' if random() > 0.2 else 'attack02')
                else:
                    self.rect.x -= 5

            elif self.mode in ['attack01', 'attack02']:
                if self.frame == len(self.frames) - 1:
                    self.set_mode('walk')


class Slime(Enemy):
    def __init__(self, coord, grop_of_row):
        frame_rate = {
            'walk': 250,
            'attack01': 120,
            'attack02': 100,
            'hurt': 100,
            'death': 250,
        }
        super().__init__(coord, ANIMATIONS['SLIME'], grop_of_row,
                         attack_radius=CELL_SIZE, hp=100, atk=15, super_atk=30,
                         frame_rate=frame_rate, hurt_cooldown=2)

    def update(self, *args, **kwargs):
        super().update()
        if self.life:
            if self.mode == 'hurt' and self.frame == len(self.frames) - 1:
                self.set_mode('walk')

            elif self.mode == 'walk':
                if self.current_target and abs(self.rect.x - self.current_target.rect.x) <= self.attack_radius:
                    self.set_mode(choice(['attack01', 'attack02']))
                else:
                    self.rect.x -= 5

            elif self.mode in ['attack01', 'attack02']:
                if self.frame == len(self.frames) - 1:
                    self.set_mode('walk')


class Werebear(Enemy):
    def __init__(self, coord, grop_of_row):
        frame_rate = {
            'walk': 250,
            'attack01': 120,
            'attack02': 120,
            'attack03': 120,
            'hurt': 100,
            'death': 250,
        }
        super().__init__(coord, ANIMATIONS['WEREBEAR'], grop_of_row,
                         attack_radius=CELL_SIZE, hp=150, atk=35, super_atk=40,
                         frame_rate=frame_rate, hurt_cooldown=3)

    def update(self, *args, **kwargs):
        super().update()
        if self.life:
            if self.mode == 'hurt' and self.frame == len(self.frames) - 1:
                self.set_mode('walk')

            elif self.mode == 'walk':
                if self.current_target and abs(self.rect.x - self.current_target.rect.x) <= self.attack_radius:
                    self.set_mode(choice(['attack01', 'attack02']) if random() > 0.2 else 'attack03')
                else:
                    self.rect.x -= 5

            elif self.mode in ['attack01', 'attack02', 'attack03']:
                if self.frame == len(self.frames) - 1:
                    self.set_mode('walk')

class Werewolf(Enemy):
    def __init__(self, coord, grop_of_row):
        frame_rate = {
            'walk': 250,
            'attack01': 120,
            'attack02': 80,
            'hurt': 100,
            'death': 250,
        }
        super().__init__(coord, ANIMATIONS['WEREWOLF'], grop_of_row,
                         attack_radius=CELL_SIZE, hp=70, atk=25,
                         frame_rate=frame_rate, hurt_cooldown=2)

    def update(self, *args, **kwargs):
        super().update()
        if self.life:
            if self.mode == 'hurt' and self.frame == len(self.frames) - 1:
                self.set_mode('walk')

            elif self.mode == 'walk':
                if self.current_target and abs(self.rect.x - self.current_target.rect.x) <= self.attack_radius:
                    self.set_mode('attack01' if random() > 0.15 else 'attack02')
                else:
                    self.rect.x -= 5

            elif self.mode in ['attack01', 'attack02']:
                if self.frame == len(self.frames) - 1:
                    self.set_mode('walk')
