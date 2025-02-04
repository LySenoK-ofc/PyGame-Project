from random import choice, randint

import constant
from sprite_groups import *
from constant import *
from all_animations import ANIMATIONS

import pygame


class Unit(pygame.sprite.Sprite):
    def __init__(self, coord, animations, grop_of_row, hp, atk, frame_rate, detect_range=None, attack_range=None,
                 super_atk=None,
                 area_atk=None):
        super().__init__(all_sprites, characters, grop_of_row)
        self.grop_of_row = grop_of_row
        self.hp = hp
        self.atk = atk
        self.full_hp = hp

        self.cached_nearby_mobs = []

        self.animations = animations
        self.mode = 'idle'
        self.frames = self.animations[self.mode]
        self.frame = 0
        self.life = True
        self.current_target = None
        self.kills = 0
        if super_atk:
            self.super_atk = super_atk
        if attack_range:
            self.attack_range = attack_range
        if detect_range:
            self.detect_range = detect_range

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
                if self.mode == 'attack01' and self.frame == 5:
                    self.current_target.lose_hp(self.atk, self)

                    self.area_attack(self.area_atk)

                elif self.mode == 'attack02' and self.frame in (4, 8):
                    self.current_target.lose_hp(self.atk, self)

                    self.area_attack(self.area_atk)
                elif self.mode == 'attack03' and self.frame == 8:
                    self.current_target.lose_hp(self.super_atk, self)

                    self.area_attack(self.super_atk / 1.5)
                    self.kills = 0

            elif isinstance(self, Wizard):
                if self.mode == 'attack01' and self.frame == 13:
                    self.area_attack(self.atk)

                if self.mode == 'attack02_no_fire_ball' and self.frame == len(self.frames) - 1:
                    FireBall(self, self.grop_of_row, ANIMATIONS['WIZARD']['fire_ball'])

            elif isinstance(self, Priest):
                if self.mode == 'attack01_no_aura' and self.frame == 4:
                    PriestAura(self, self.grop_of_row, ANIMATIONS['PRIEST']['aura_for_attack01'])

                elif self.mode == 'healing' and self.frame > 1 and self.heal_target.hp != self.heal_target.full_hp:
                    self.heal_target.hp += self.heal

            elif isinstance(self, Lancer):
                if self.mode == 'attack01':
                    self.rect.x += 25
                    self.area_attack(self.atk)

            elif isinstance(self, ArmoredAxeman):
                if self.mode == 'attack01' and self.frame == 5:
                    self.current_target.lose_hp(self.atk, self)

                    self.area_attack(self.area_atk)

                elif self.mode == 'attack02' and self.frame in (4, 8):
                    self.current_target.lose_hp(self.atk, self)

                    self.area_attack(self.area_atk)
                elif self.mode == 'attack03' and self.frame == 8:
                    self.current_target.lose_hp(self.super_atk, self)

                    self.area_attack(self.super_atk / 1.5)
                    self.kills = 0

            elif isinstance(self, SwordsMan):
                if self.mode == 'attack01' and self.frame == 3:
                    self.current_target.lose_hp(self.atk, self)

                    self.area_attack(self.area_atk)
                elif self.mode == 'attack02' and self.frame in (3, 6, 12):
                    self.current_target.lose_hp(self.atk, self)

                    self.area_attack(self.area_atk)
                elif self.mode == 'attack03' and self.frame in (6, 7, 9, 10):
                    self.current_target.lose_hp(self.atk, self)

                    self.area_attack(self.area_atk)


def lose_hp(self, count, killer=None):
    if self.life:
        if 'block' in self.animations and randint(1, 2) == 1:
            self.set_mode('block')
            self.hp -= count / 3
        else:
            self.set_mode('hurt')
            self.hp -= count
        if self.hp <= 0:
            self.life = False
            if killer:
                killer.kills += 1


def find_target(self):
    self.cached_nearby_mobs = list(filter(lambda nearby_mob: nearby_mob.rect.x >= self.rect.x,
                                          [mob for mob in self.grop_of_row
                                           if mob in mobs and mob.life
                                           and abs(self.rect.x - mob.rect.x) <= self.detect_range]))

    if self.cached_nearby_mobs:
        nearest_mob = min(self.cached_nearby_mobs, key=lambda x: x.rect.x)
        self.current_target = nearest_mob if abs(
            self.rect.x - nearest_mob.rect.x) <= self.attack_range else None

        for mob in set(self.cached_nearby_mobs):
            mob.set_target(self)

        if self.current_target:
            return True
    return False


def update(self):
    if constant.frame_count % 3 == 0:
        if self.rect.right < 0 or self.rect.left > WIDTH or self.rect.bottom < 0 or self.rect.top > HEIGHT:
            self.life = False
            self.kill()

        self.find_target()

    self.update_animation()

    if not self.life:
        self.set_mode('death')
        if self.frame == len(self.frames) - 1:
            self.kill()


class Archer(Unit):
    def __init__(self, coord, grop_of_row):
        frame_rate = {
            'idle': 250,
            'attack01': 140,
            'attack02': 140,
            'hurt': 100,
            'death': 250,
        }
        super().__init__(coord, ANIMATIONS['ARCHER'], grop_of_row,
                         detect_range=WIDTH, attack_range=WIDTH, hp=60, atk=10, super_atk=30,
                         frame_rate=frame_rate)

    def update(self):
        super().update()
        if self.life:

            if self.mode == 'hurt' and self.frame == len(self.frames) - 1:
                self.set_mode('idle')

            elif self.mode == 'idle':
                if self.current_target is not None:
                    self.set_mode('attack01' if self.kills < 4 else 'attack02')

            elif self.mode in ('attack01', 'attack02') and self.current_target and not self.current_target.life:
                self.current_target = None
                self.set_mode('idle')


class Knight(Unit):
    def __init__(self, coord, grop_of_row):
        frame_rate = {
            'idle': 250,
            'attack01': 135,
            'attack02': 135,
            'attack03': 115,
            'block': 60,
            'hurt': 60,
            'death': 250,
        }
        super().__init__(coord, ANIMATIONS['KNIGHT'], grop_of_row,
                         detect_range=4 * CELL_SIZE, attack_range=CELL_SIZE, hp=80, atk=20, super_atk=40,
                         frame_rate=frame_rate)

    def area_attack(self, area_atk):
        for mob in self.cached_nearby_mobs:
            if mob != self.current_target and mob.life and abs(self.rect.x - mob.rect.x) <= CELL_SIZE:
                mob.lose_hp(area_atk, self)

    def update(self):
        super().update()
        if self.life:
            if self.mode in ['hurt', 'block'] and self.frame == len(self.frames) - 1:
                self.set_mode('idle')

            elif self.mode == 'idle':
                if self.current_target:
                    self.set_mode(choice(['attack01', 'attack02'] if self.kills < 4 else ['attack03']))

            elif (self.mode in ('attack01', 'attack02', 'attack03')
                  and self.current_target and not self.current_target.life):
                self.current_target = None
                self.set_mode('idle')


class Lancer(Unit):
    def __init__(self, coord, grop_of_row):
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
        super().__init__(coord, ANIMATIONS['LANCER'], grop_of_row,
                         detect_range=2 * CELL_SIZE, attack_range=CELL_SIZE, hp=100, atk=1000,
                         frame_rate=frame_rate)

    def area_attack(self, area_atk):
        for mob in self.cached_nearby_mobs:
            if mob.life and pygame.sprite.collide_mask(self, mob):
                mob.lose_hp(area_atk, self)

    def update(self):
        super().update()
        if self.life:
            if self.mode == 'idle':
                if self.current_target:
                    self.set_mode('attack01')


class Wizard(Unit):
    def __init__(self, coord, grop_of_row):
        frame_rate = {
            'idle': 250,
            'attack01': 90,
            'attack02_no_fire_ball': 250,
            'hurt': 100,
            'death': 250,
        }
        super().__init__(coord, ANIMATIONS['WIZARD'], grop_of_row,
                         detect_range=3 * CELL_SIZE, attack_range=2 * CELL_SIZE, hp=60, atk=35,
                         frame_rate=frame_rate)

    def area_attack(self, area_atk):
        for mob in self.cached_nearby_mobs:
            if mob.life and abs(self.rect.x - mob.rect.x) <= CELL_SIZE * 1.5:
                mob.lose_hp(area_atk, self)

    def update(self):
        super().update()
        if self.life:
            if self.mode == 'hurt' and self.frame == len(self.frames) - 1:
                self.set_mode('idle')

            elif self.mode == 'idle':
                if self.current_target:
                    if abs(self.rect.x - self.current_target.rect.x) <= CELL_SIZE * 1.5:
                        self.set_mode('attack01')
                    else:
                        self.set_mode('attack02_no_fire_ball')

            elif (self.mode in ('attack01', 'attack02_no_fire_ball') and
                  self.current_target and not self.current_target.life):
                self.current_target = None
                self.set_mode('idle')


class Priest(Unit):
    def __init__(self, coord, grop_of_row):
        frame_rate = {
            'idle': 250,
            'attack01_no_aura': 180,
            'healing': 200,
            'hurt': 100,
            'death': 250,
        }
        super().__init__(coord, ANIMATIONS['PRIEST'], grop_of_row,
                         detect_range=3 * CELL_SIZE, attack_range=2 * CELL_SIZE, hp=60, atk=35,
                         frame_rate=frame_rate)

        self.heal_range = CELL_SIZE
        self.heal_target = None
        self.heal = 5
        self.heal_cooldown_start = pygame.time.get_ticks()

    def check_healing(self):
        for unit in self.grop_of_row:
            if (unit in characters
                    and self.rect.x < unit.rect.x
                    and abs(self.rect.x - unit.rect.x) <= self.heal_range
                    and unit.hp < unit.full_hp):
                self.set_mode('healing')
                self.heal_target = unit
                break

    def update(self):
        super().update()
        if self.life:
            if self.mode == 'hurt' or self.mode == 'healing' and self.frame == len(self.frames) - 1:
                self.set_mode('idle')

            elif self.mode == 'idle':
                if self.current_target:
                    self.set_mode('attack01_no_aura')
                else:
                    now = pygame.time.get_ticks()
                    if now - self.heal_cooldown_start > 10000:
                        self.heal_cooldown_start = now
                        self.check_healing()

            elif self.mode in 'attack01_no_aura' and self.current_target and not self.current_target.life:
                self.current_target = None
                self.set_mode('idle')


class ArmoredAxeman(Unit):
    def __init__(self, coord, grop_of_row):
        frame_rate = {
            'idle': 250,
            'attack01': 135,
            'attack02': 135,
            'attack03': 115,
            'hurt': 60,
            'death': 250,
        }
        super().__init__(coord, ANIMATIONS['ARMORED_AXEMAN'], grop_of_row,
                         detect_range=4 * CELL_SIZE, attack_range=CELL_SIZE, hp=80, atk=20, super_atk=40,
                         frame_rate=frame_rate)

    def area_attack(self, area_atk):
        for mob in self.cached_nearby_mobs:
            if mob != self.current_target and mob.life and abs(self.rect.x - mob.rect.x) <= self.attack_range:
                mob.lose_hp(area_atk, self)

    def update(self):
        super().update()
        if self.life:
            if self.mode == 'hurt' and self.frame == len(self.frames) - 1:
                self.set_mode('idle')

            elif self.mode == 'idle':
                if self.current_target:
                    self.set_mode(choice(['attack01', 'attack02'] if self.kills < 4 else ['attack03']))

            elif (self.mode in ('attack01', 'attack02', 'attack03')
                  and self.current_target and not self.current_target.life):
                self.current_target = None
                self.set_mode('idle')


class SwordsMan(Unit):
    def __init__(self, coord, grop_of_row):
        frame_rate = {
            'idle': 250,
            'attack01': 135,
            'attack02': 135,
            'attack03': 115,
            'hurt': 60,
            'death': 250,
        }
        super().__init__(coord, ANIMATIONS['SWORDSMAN'], grop_of_row,
                         detect_range=4 * CELL_SIZE, attack_range=CELL_SIZE, hp=80, atk=20, super_atk=40,
                         frame_rate=frame_rate)

    def area_attack(self, area_atk):
        for mob in self.cached_nearby_mobs:
            if mob != self.current_target and mob.life and abs(self.rect.x - mob.rect.x) <= self.attack_range:
                mob.lose_hp(area_atk, self)

    def update(self):
        super().update()
        if self.life:
            if self.mode == 'hurt' and self.frame == len(self.frames) - 1:
                self.set_mode('idle')

            elif self.mode == 'idle':
                if self.current_target:
                    self.set_mode(choice(['attack01', 'attack02', 'attack03']))

            elif (self.mode in ('attack01', 'attack02', 'attack03')
                  and self.current_target and not self.current_target.life):
                self.current_target = None
                self.set_mode('idle')


class KnightTemplar(Unit):
    def __init__(self, coord, grop_of_row):
        frame_rate = {
            'idle': 250,
            'walk_block': 250,
            'attack01': 135,
            'attack02': 135,
            'attack03': 115,
            'block': 60,
            'hurt': 60,
            'death': 250,
        }
        super().__init__(coord, ANIMATIONS['KNIGHT_TEMPLAR'], grop_of_row,
                         detect_range=4 * CELL_SIZE, attack_range=CELL_SIZE, hp=80, atk=20, super_atk=40,
                         frame_rate=frame_rate)

    def area_attack(self, area_atk):
        for mob in self.cached_nearby_mobs:
            if mob != self.current_target and mob.life and abs(self.rect.x - mob.rect.x) <= self.attack_range:
                mob.lose_hp(area_atk, self)

    def update(self):
        super().update()
        if self.life:
            if self.mode in ('hurt','block') and self.frame == len(self.frames) - 1:
                self.set_mode('idle')

            elif self.mode == 'idle':
                if self.current_target:
                    self.set_mode(choice(['attack01', 'attack02', 'attack03']))

            elif (self.mode in ('attack01', 'attack02', 'attack03')
                  and self.current_target and not self.current_target.life):
                self.current_target = None
                self.set_mode('idle')


class Arrow(pygame.sprite.Sprite):
    def __init__(self, archer, v, damage):
        super().__init__(all_sprites, shells)
        # Устанавливаем изображение и маску стрелы
        self.image = ANIMATIONS['ARROW01']['idle'][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.archer = archer
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

        mobs_or_row = [mob for mob in self.archer.grop_of_row
                       if mob in mobs and abs(self.rect.x - mob.rect.x) <= 30]
        for mob in mobs_or_row:
            if mob.life and pygame.sprite.collide_mask(self, mob):
                mob.lose_hp(self.damage, self.archer)
                self.kill()  # Удаляем стрелу
        else:
            self.rect.x += self.v  # Перемещаем стрелу вправо


class AttackEntity(pygame.sprite.Sprite):
    def __init__(self, owner, grop_of_row, anim_start, damage, x, frames):
        super().__init__(all_sprites, shells)
        self.image = anim_start
        self.mask = pygame.mask.from_surface(self.image)

        self.damage = damage
        self.owner = owner
        self.grop_of_row = grop_of_row
        self.target_mobs = False
        self.attack_range = 60

        self.last_update = pygame.time.get_ticks()
        self.frame = 0
        self.frames = frames

        self.rect = self.image.get_rect(center=owner.rect.center)
        self.rect.x += x

    def update_animation(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 130:
            self.last_update = now
            self.frame = (self.frame + 1) % len(self.frames)
            self.image = self.frames[self.frame]

            if isinstance(self, FireBall):
                if self.mode == 'boom' and self.frame == len(self.frames) - 1:
                    self.kill()  # Удаляем шар

            if isinstance(self, PriestAura):
                if self.frame == 2:
                    cached_nearby_mobs = list(filter(lambda nearby_mob: nearby_mob.rect.x >= self.rect.x,
                                                     [mob for mob in self.grop_of_row
                                                      if mob in mobs and mob.life
                                                      and abs(self.rect.x - mob.rect.x) <= CELL_SIZE]))

                    for mob in cached_nearby_mobs:
                        if pygame.sprite.collide_mask(self, mob):
                            mob.lose_hp(self.damage, self.owner)
                            self.target_mobs = True
                elif self.frame == len(self.frames) - 1:
                    self.kill()


class FireBall(AttackEntity):
    def __init__(self, wizard, grop_of_row, anim):
        super().__init__(wizard, grop_of_row, anim[0], 35, 5, anim[:4])
        self.moving = anim[:4]
        self.boom = anim[4:]

        self.v = 10

        self.frames = self.moving
        self.mode = 'moving'

    def update(self, *args, **kwargs):
        self.update_animation()

        if self.mode == 'moving':
            # Проверяем столкновение шара с целью
            if self.rect.x < 0 or self.rect.left > WIDTH or self.rect.y < 0 or self.rect.top > HEIGHT:
                self.kill()

            if constant.frame_count % 3 == 0:
                cached_nearby_mobs = list(filter(lambda nearby_mob: nearby_mob.rect.x >= self.rect.x,
                                                 [mob for mob in self.grop_of_row
                                                  if mob in mobs and mob.life
                                                  and abs(self.rect.x - mob.rect.x) <= CELL_SIZE]))

                for mob in cached_nearby_mobs:
                    if pygame.sprite.collide_mask(self, mob):
                        mob.lose_hp(self.damage, self.owner)
                        self.target_mobs = True

            if self.target_mobs:
                self.mode = 'boom'
                self.frames = self.boom
                self.rect.x += CELL_SIZE / 2
            else:
                if self.owner.rect.x + 2 * CELL_SIZE >= self.rect.x:
                    self.rect.x += self.v  # Перемещаем шар вправо
                else:
                    self.mode = 'boom'


class PriestAura(AttackEntity):
    def __init__(self, priest, grop_of_row, anim):
        super().__init__(priest, grop_of_row, anim[0], 35, (priest.current_target.rect.x - priest.rect.x), anim)

    def update(self, *args, **kwargs):
        self.update_animation()
