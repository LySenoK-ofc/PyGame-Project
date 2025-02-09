from random import choice, random

import constant
from sprite_groups import groups
from constant import CELL_SIZE, WIDTH, HEIGHT
from all_animations import ANIMATIONS

import pygame


class Unit(pygame.sprite.Sprite):
    def __init__(self, coord, animations, group, hp, atk, frame_rate,
                 detect_range=None, attack_range=None, super_atk=None, area_atk=None, armor_hp=None, armor_def=None,
                 sale=None):
        super().__init__(groups['all_sprites'], groups['characters'], *group)
        self.grop_of_row = group[0]
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
        self.armor_hp = armor_hp
        self.hits = 0

        if super_atk:
            self.super_atk = super_atk
        if attack_range:
            self.attack_range = attack_range
        if detect_range:
            self.detect_range = detect_range
        if sale:
            self.sale = sale
        if self.armor_hp:
            self.armor_def = armor_def

        self.area_atk = area_atk if area_atk is not None else self.atk / 2.5

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

            if self.current_target:
                if isinstance(self, Archer):
                    if self.mode == 'attack01' and self.frame == 6:
                        Arrow(self, 12.5, self.atk)
                    elif self.mode == 'attack02' and self.frame == 10:
                        Arrow(self, 20, self.super_atk)

                elif isinstance(self, Knight):
                    if self.mode == 'attack01' and self.frame == 5:
                        self.current_target.lose_hp(self.atk, armor_dmg=self.atk * 0.3)

                        self.area_attack(self.area_atk, armor_dmg=self.area_atk * 0.3)

                    elif self.mode == 'attack02' and self.frame in (4, 8):
                        self.current_target.lose_hp(self.atk, armor_dmg=self.atk * 0.3)

                        self.area_attack(self.area_atk, armor_dmg=self.area_atk * 0.3)
                    elif self.mode == 'attack03' and self.frame == 8:
                        self.current_target.lose_hp(self.super_atk, armor_dmg=self.super_atk * 0.3)

                        self.area_attack(self.super_atk / 1.5, armor_dmg=self.super_atk / 1.5 * 0.3)

                elif isinstance(self, Wizard):
                    if self.mode == 'attack01' and self.frame == 13:
                        self.area_attack(self.atk)

                    if self.mode == 'attack02_no_fire_ball' and self.frame == len(self.frames) - 1:
                        FireBall(self, self.grop_of_row, ANIMATIONS['WIZARD']['fire_ball'])

                elif isinstance(self, Priest):
                    if self.mode == 'attack01_no_aura' and self.frame == 4:
                        PriestAura(self, self.grop_of_row, ANIMATIONS['PRIEST']['aura_for_attack01'])

                elif isinstance(self, ArmoredAxeman):
                    if self.mode == 'attack01' and self.frame == 5:
                        self.current_target.lose_hp(self.atk, armor_dmg=self.atk * 0.3)

                        self.area_attack(self.area_atk, armor_dmg=self.area_atk * 0.3)

                    elif self.mode == 'attack02' and self.frame in (4, 8):
                        self.current_target.lose_hp(self.atk, armor_dmg=self.atk * 0.3)

                        self.area_attack(self.area_atk, armor_dmg=self.area_atk * 0.3)
                    elif self.mode == 'attack03' and self.frame == 8:
                        self.current_target.lose_hp(self.super_atk, armor_dmg=self.super_atk * 0.3)

                        self.area_attack(self.super_atk / 1.5, armor_dmg=self.super_atk / 1.5 * 0.3)

                elif isinstance(self, SwordsMan):
                    if self.mode == 'attack01' and self.frame == 3:
                        self.current_target.lose_hp(self.atk, armor_dmg=self.atk * 0.3)

                        self.area_attack(self.area_atk, armor_dmg=self.area_atk * 0.3)
                    elif self.mode == 'attack02' and self.frame in (3, 6, 12):
                        self.current_target.lose_hp(self.atk, armor_dmg=self.atk * 0.3)

                        self.area_attack(self.area_atk, armor_dmg=self.area_atk * 0.3)
                    elif self.mode == 'attack03' and self.frame in (6, 7, 9, 10):
                        self.current_target.lose_hp(self.atk, armor_dmg=self.atk * 0.3)

                        self.area_attack(self.area_atk, armor_dmg=self.area_atk * 0.3)

                elif isinstance(self, KnightTemplar):
                    if self.mode == 'attack01' and self.frame == 4:
                        self.current_target.lose_hp(self.atk, armor_dmg=self.atk * 0.3)

                        self.area_attack(self.area_atk, armor_dmg=self.area_atk * 0.3)
                    elif self.mode == 'attack02' and self.frame == 5:
                        self.current_target.lose_hp(self.atk, armor_dmg=self.atk * 0.3)

                        self.area_attack(self.area_atk, armor_dmg=self.area_atk * 0.3)
                    elif self.mode == 'attack03' and self.frame in (3, 7):
                        self.current_target.lose_hp(self.atk, armor_dmg=self.atk * 0.3)

                        self.area_attack(self.area_atk, armor_dmg=self.area_atk * 0.3)

            if isinstance(self, Lancer):
                if self.mode == 'attack01':
                    self.rect.x += 25
                    self.area_attack(self.atk)
            elif isinstance(self, Priest) and self.mode == 'healing':
                if self.frame in (3, 5) and self.heal_target.hp != self.heal_target.full_hp:
                    self.heal_target.hp += self.heal
                if self.rect.x > self.heal_target.rect.x:
                    self.image = pygame.transform.flip(self.image, True, False)

            elif isinstance(self, KnightTemplar) and self.mode == 'walk_block':
                if self.distance > self.distance_traveled:
                    self.rect.x += self.speed
                    self.distance_traveled += self.speed
                else:
                    self.distance_traveled -= self.distance
                    self.set_mode('idle')

    def lose_hp(self, dmg, armor_dmg=0):
        if self.life:
            self.hits += 1
            if 'block' in self.animations and random() < 0.30:
                self.set_mode('block')
                self.hp -= dmg / 3
            else:
                if self.hits % 2 == 0:
                    self.set_mode('hurt')
                if self.armor_hp:
                    dmg -= dmg * self.armor_def
                    self.armor_hp -= armor_dmg
                self.hp -= dmg
            if self.hp <= 0:
                self.life = False

    def find_target(self):
        self.cached_nearby_mobs = list(filter(lambda nearby_mob: nearby_mob.rect.x >= self.rect.x,
                                              [mob for mob in self.grop_of_row
                                               if mob in groups['mobs'] and mob.life
                                               and abs(self.rect.x - mob.rect.x) <= self.detect_range]))

        nearest_mob = min(self.cached_nearby_mobs, key=lambda x: x.rect.x) if self.cached_nearby_mobs else []
        self.current_target = min(self.cached_nearby_mobs, key=lambda x: x.rect.x) \
            if nearest_mob and abs(self.rect.x - nearest_mob.rect.x) <= self.attack_range else None

        for mob in set(self.cached_nearby_mobs):
            mob.set_target(self)

        return bool(self.current_target)

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
            'attack01': 170,
            'attack02': 170,
            'hurt': 100,
            'death': 250,
        }
        super().__init__(coord, ANIMATIONS['ARCHER'], [grop_of_row, groups['shop_units']],
                         detect_range=WIDTH, attack_range=WIDTH, hp=100, atk=25, super_atk=40, sale=25,
                         frame_rate=frame_rate)

    def update(self):
        super().update()
        if self.life:

            if self.mode in ('hurt', 'attack01', 'attack02') and self.frame == len(self.frames) - 1:
                self.set_mode('idle')

            elif self.mode == 'idle':
                if self.current_target:
                    self.set_mode('attack01' if random() > 0.3 else 'attack02')


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
        super().__init__(coord, ANIMATIONS['KNIGHT'], [grop_of_row, groups['shop_units']],
                         detect_range=4 * CELL_SIZE, attack_range=CELL_SIZE, hp=200, atk=30,
                         super_atk=50, sale=45,
                         frame_rate=frame_rate, armor_hp=50, armor_def=0.2)

    def area_attack(self, area_atk, armor_dmg):
        for mob in self.cached_nearby_mobs:
            if mob != self.current_target and mob.life and abs(self.rect.x - mob.rect.x) <= CELL_SIZE:
                mob.lose_hp(area_atk, armor_dmg=armor_dmg)

    def update(self):
        super().update()
        if self.life:
            if self.mode in ('hurt', 'block', 'attack01', 'attack02', 'attack03') and self.frame == len(
                    self.frames) - 1:
                self.set_mode('idle')

            elif self.mode == 'idle':
                if self.current_target:
                    self.set_mode(choice(['attack01', 'attack02']) if random() > 0.2 else 'attack03')


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
        super().__init__(coord, ANIMATIONS['LANCER'], [grop_of_row],
                         detect_range=2 * CELL_SIZE, attack_range=CELL_SIZE, hp=1000, atk=1000,
                         frame_rate=frame_rate)

    def area_attack(self, area_atk):
        for mob in self.cached_nearby_mobs:
            if mob.life and pygame.sprite.collide_mask(self, mob):
                mob.lose_hp(dmg=area_atk)

    def update(self):
        super().update()
        if self.life:
            if self.mode in ('idle', 'hurt'):
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
        super().__init__(coord, ANIMATIONS['WIZARD'], [grop_of_row, groups['shop_units']],
                         detect_range=3 * CELL_SIZE, attack_range=2 * CELL_SIZE, hp=110, atk=30, sale=42,
                         frame_rate=frame_rate)

    def area_attack(self, area_atk):
        for mob in self.cached_nearby_mobs:
            if mob.life and abs(self.rect.x - mob.rect.x) <= CELL_SIZE * 1.5:
                mob.lose_hp(area_atk)

    def update(self):
        super().update()
        if self.life:
            if self.mode in ('hurt', 'attack01', 'attack02_no_fire_ball') and self.frame == len(self.frames) - 1:
                self.set_mode('idle')

            elif self.mode == 'idle':
                if self.current_target:
                    if abs(self.rect.x - self.current_target.rect.x) <= CELL_SIZE * 1.5:
                        self.set_mode('attack01')
                    else:
                        self.set_mode('attack02_no_fire_ball')


class Priest(Unit):
    def __init__(self, coord, grop_of_row):
        frame_rate = {
            'idle': 250,
            'attack01_no_aura': 180,
            'healing': 200,
            'hurt': 100,
            'death': 250,
        }
        super().__init__(coord, ANIMATIONS['PRIEST'], [grop_of_row, groups['shop_units']],
                         detect_range=3 * CELL_SIZE, attack_range=2 * CELL_SIZE, hp=120, atk=20, sale=40,
                         frame_rate=frame_rate)

        self.heal_range = CELL_SIZE
        self.heal_target = None
        self.heal = 15
        self.heal_cooldown_start = pygame.time.get_ticks()

    def check_healing(self):
        for unit in self.grop_of_row:
            if (unit in groups['characters']
                    and CELL_SIZE <= abs(self.rect.x - unit.rect.x) <= self.heal_range
                    and unit.hp < unit.full_hp):
                self.set_mode('healing')
                self.heal_target = unit
                break

    def update(self):
        super().update()
        if self.life:
            if self.mode in ('hurt', 'healing', 'attack01_no_aura') and self.frame == len(self.frames) - 1:
                self.set_mode('idle')

            elif self.mode == 'idle':
                if self.current_target:
                    self.set_mode('attack01_no_aura')
                    if random() < 0.1:
                        self.heal_cooldown_start -= 5000
                else:
                    now = pygame.time.get_ticks()
                    if now - self.heal_cooldown_start > 10000:
                        self.heal_cooldown_start = now
                        self.check_healing()


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
        super().__init__(coord, ANIMATIONS['ARMORED_AXEMAN'], [grop_of_row, groups['shop_units']],
                         detect_range=4 * CELL_SIZE, attack_range=CELL_SIZE, hp=150, atk=35, super_atk=60, sale=35,
                         frame_rate=frame_rate, armor_hp=70, armor_def=0.35)

    def area_attack(self, area_atk, armor_dmg):
        for mob in self.cached_nearby_mobs:
            if mob != self.current_target and mob.life and abs(self.rect.x - mob.rect.x) <= self.attack_range:
                mob.lose_hp(area_atk, armor_dmg=armor_dmg)

    def update(self):
        super().update()
        if self.life:
            if self.mode in ('hurt', 'attack01', 'attack02', 'attack03') and self.frame == len(self.frames) - 1:
                self.set_mode('idle')

            elif self.mode == 'idle':
                if self.current_target:
                    self.set_mode(choice(['attack01', 'attack02']) if random() > 0.3 else 'attack03')


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
        super().__init__(coord, ANIMATIONS['SWORDSMAN'], [grop_of_row, groups['shop_units']],
                         detect_range=4 * CELL_SIZE, attack_range=CELL_SIZE, hp=150, atk=30, sale=40,
                         frame_rate=frame_rate, armor_hp=30, armor_def=0.2)

    def area_attack(self, area_atk, armor_dmg):
        for mob in self.cached_nearby_mobs:
            if mob != self.current_target and mob.life and abs(self.rect.x - mob.rect.x) <= self.attack_range:
                mob.lose_hp(area_atk, armor_dmg=armor_dmg)

    def update(self):
        super().update()
        if self.life:
            if self.mode in ('hurt', 'attack01', 'attack02', 'attack03') and self.frame == len(self.frames) - 1:
                self.set_mode('idle')

            elif self.mode == 'idle':
                if self.current_target:
                    self.set_mode(choice(['attack01', 'attack02', 'attack03']))


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
        super().__init__(coord, ANIMATIONS['KNIGHT_TEMPLAR'], [grop_of_row, groups['shop_units']],
                         detect_range=4 * CELL_SIZE, attack_range=CELL_SIZE, hp=200, atk=30, sale=40,
                         frame_rate=frame_rate, armor_hp=60, armor_def=0.25)

        self.speed = 4
        self.distance = CELL_SIZE / 2
        self.distance_traveled = 0
        self.last_walk = pygame.time.get_ticks()

    def area_attack(self, area_atk, armor_dmg):
        for mob in self.cached_nearby_mobs:
            if mob != self.current_target and mob.life and abs(self.rect.x - mob.rect.x) <= self.attack_range:
                mob.lose_hp(area_atk, armor_dmg=armor_dmg)

    def update(self):
        super().update()
        if self.life:
            if self.mode in ('hurt', 'block', 'attack01', 'attack02', 'attack03') and self.frame == len(
                    self.frames) - 1:
                self.set_mode('idle')

            elif self.mode == 'idle':
                if self.current_target:
                    self.set_mode(choice(['attack01', 'attack02', 'attack03']))
                else:
                    now = pygame.time.get_ticks()
                    if now - self.last_walk > 25000 and not self.cached_nearby_mobs and self.rect.x < WIDTH - 500:
                        self.last_walk = now
                        self.set_mode('walk_block')


class AttackEntity(pygame.sprite.Sprite):
    def __init__(self, owner, grop_of_row, anim_start, damage, x, frames):
        super().__init__(groups['all_sprites'], groups['shells'])
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
                                                      if mob in groups['mobs'] and mob.life
                                                      and abs(self.rect.x - mob.rect.x) <= CELL_SIZE]))

                    for mob in cached_nearby_mobs:
                        if pygame.sprite.collide_mask(self, mob):
                            mob.lose_hp(dmg=self.damage)
                            self.target_mobs = True
                elif self.frame == len(self.frames) - 1:
                    self.kill()


class Arrow(AttackEntity):
    def __init__(self, archer, v, damage):
        super().__init__(archer, archer.grop_of_row, ANIMATIONS['ARROW01']['idle'][0], damage, 5, None)
        self.v = v

    def update(self, *args, **kwargs):
        if self.rect.x < 0 or self.rect.left > WIDTH or self.rect.y < 0 or self.rect.top > HEIGHT:
            self.kill()

        mobs_or_row = [mob for mob in self.grop_of_row
                       if mob in groups['mobs'] and abs(self.rect.x - mob.rect.x) <= 30]
        for mob in mobs_or_row:
            if mob.life and pygame.sprite.collide_mask(self, mob):
                mob.lose_hp(dmg=self.damage, armor_dmg=self.damage * 0.3)
                self.kill()  # Удаляем стрелу
        else:
            self.rect.x += self.v


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
                                                  if mob in groups['mobs'] and mob.life
                                                  and abs(self.rect.x - mob.rect.x) <= CELL_SIZE]))

                for mob in cached_nearby_mobs:
                    if pygame.sprite.collide_mask(self, mob):
                        mob.lose_hp(dmg=self.damage)
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
