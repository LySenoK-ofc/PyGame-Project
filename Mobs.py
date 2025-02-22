from random import choice, randint, random
import pygame

import game_dynamic_parameters
from all_animations import ANIMATIONS
from sounds_manager import play_sound, sounds
from sprite_groups import groups
from constant import CELL_SIZE, HEIGHT, WIDTH


class Enemy(pygame.sprite.Sprite):
    def __init__(self, coord, animations, group_of_row, frame_rate, hp, atk, hurt_cooldown,
                 attack_radius=None, super_atk=None, armor_hp=None, armor_def=None, money=0):
        super().__init__(groups['all_sprites'], groups['mobs'], group_of_row)
        self.animations = animations
        self.frame_rate = frame_rate
        self.group_of_row = group_of_row
        self.cached_nearby_mobs = None
        self.hp = hp
        self.atk = atk
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
        self.money = money

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
            self.attack_frame_event()

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
                    if isinstance(self, Werewolf):
                        play_sound(choice([sounds['animals']['wolf_hurt'], sounds['animals']['wolf_roar']]), 0.15)
                    elif isinstance(self, Werebear):
                        play_sound(sounds['animals']['bear_roar'], 0.15)
                    elif isinstance(self, Slime):
                        play_sound(sounds['slime']['damage'], 0.15)
                    elif isinstance(self, Orc):
                        play_sound(sounds['mobs']['roar'][1], 0.15)
                    else:
                        play_sound(choice([sounds['mobs']['roar'][2], sounds['mobs']['roar'][3],
                                           sounds['mobs']['roar'][4], sounds['mobs']['roar'][5]]), 0.15)
                self.hp -= dmg
            if self.hp <= 0:
                self.life = False
                game_dynamic_parameters.cash += self.money
                game_dynamic_parameters.killed_mobs += 1

    def attack_frame_event(self):
        """Метод проверки фрейма удара. Переопределяется."""
        pass

    def set_target(self, new_target):
        if self.current_target is None:
            self.current_target = new_target
        if abs(self.current_target.rect.x - self.rect.x) > abs(new_target.rect.x - self.rect.x):
            self.current_target = new_target

    def check_target(self):
        if self.current_target.rect.x > self.rect.x or not self.current_target.life:
            self.current_target = None

    def choice_sound(self):
        return choice([sounds['sword'][1],
                       sounds['sword'][2],
                       sounds['sword'][3],
                       sounds['sword'][6],
                       sounds['sword'][8]])

    def update(self, *args, **kwargs):
        if game_dynamic_parameters.frame_count % 5 == 0:
            if self.rect.x < 0 or self.rect.left > WIDTH + 700 or self.rect.y < 0 or self.rect.top > HEIGHT:
                self.life = False
                game_dynamic_parameters.hp -= 1
                # Проверка на проигрыш
                if game_dynamic_parameters.hp <= 0:
                    game_dynamic_parameters.GAME_MODE = 'LOSE'

                self.kill()
            if self.current_target:
                self.check_target()

        self.update_animation()

        if not self.life:
            if self.mode != 'death':
                self.set_mode('death')
                if isinstance(self, Werebear):
                    play_sound(sounds['animals']['bear_death'], 0.2)
                elif isinstance(self, Orc):
                    play_sound(sounds['mobs']['death'][2], 0.2)
                elif isinstance(self, RiderOrc):
                    play_sound(sounds['mobs']['death'][1], 0.2)
                else:
                    play_sound(choice([sounds['mobs']['death'][3], sounds['mobs']['death'][4],
                                       sounds['mobs']['death'][5], sounds['mobs']['death'][6]]), 0.2)
            if self.frame == len(self.frames) - 1:
                self.kill()


class Orc(Enemy):
    def __init__(self, coord, group_of_row):
        frame_rate = {
            'walk': 250,
            'attack01': 250,
            'attack02': 250,
            'hurt': 100,
            'death': 250,
        }
        super().__init__(coord, ANIMATIONS['ORC'], group_of_row,
                         attack_radius=CELL_SIZE, hp=80, atk=20,
                         frame_rate=frame_rate, hurt_cooldown=2, money=12)

    def attack_frame_event(self):
        if self.current_target and self.mode in ['attack01', 'attack02'] and self.frame == 3:
            self.current_target.lose_hp(self.atk, armor_dmg=self.atk * 0.1)

    def update(self, *args, **kwargs):
        super().update()
        if self.life:
            if self.mode in ['hurt', 'attack01', 'attack02'] and self.frame == len(self.frames) - 1:
                self.set_mode('walk')
            elif self.mode == 'walk':
                if self.current_target and abs(self.rect.x - self.current_target.rect.x) <= self.attack_radius:
                    self.set_mode(choice(['attack01', 'attack02']))
                else:
                    self.rect.x -= 3


class EliteOrc(Enemy):
    def __init__(self, coord, group_of_row):
        frame_rate = {
            'walk': 250,
            'attack01': 180,
            'attack02': 250,
            'attack03': 150,
            'hurt': 100,
            'death': 250,
        }
        super().__init__(coord, ANIMATIONS['ELITE_ORC'], group_of_row,
                         attack_radius=CELL_SIZE, hp=120, atk=30, super_atk=50,
                         frame_rate=frame_rate, armor_hp=20, armor_def=0.1, hurt_cooldown=3, money=16)

    def attack_frame_event(self):
        if self.current_target:
            if self.mode == 'attack01' and self.frame == 4:
                self.current_target.lose_hp(self.atk, armor_dmg=self.atk * 0.1)
            elif self.mode == 'attack02' and self.frame in (1, 5, 9):
                self.current_target.lose_hp(self.super_atk, armor_dmg=self.super_atk * 0.1)
            elif self.mode == 'attack03' and self.frame == 5:
                self.current_target.lose_hp(self.super_atk, armor_dmg=self.super_atk * 0.1)

    def update(self, *args, **kwargs):
        super().update()
        if self.life:
            if self.mode in ['hurt', 'attack01', 'attack02', 'attack03'] and self.frame == len(self.frames) - 1:
                self.set_mode('walk')
            elif self.mode == 'walk':
                if self.current_target and abs(self.rect.x - self.current_target.rect.x) <= self.attack_radius:
                    self.set_mode('attack01' if random() > 0.1 else choice(['attack02', 'attack03']))
                else:
                    self.rect.x -= 3.5


class ArmoredOrc(Enemy):
    def __init__(self, coord, group_of_row):
        frame_rate = {
            'walk': 250,
            'attack01': 150,
            'attack02': 100,
            'attack03': 90,
            'block': 100,
            'hurt': 100,
            'death': 250,
        }
        super().__init__(coord, ANIMATIONS['ARMORED_ORC'], group_of_row,
                         attack_radius=CELL_SIZE, hp=150, atk=25, super_atk=35,
                         frame_rate=frame_rate, armor_hp=30, armor_def=0.15, hurt_cooldown=4, money=24)

    def attack_frame_event(self):
        if self.current_target:
            if self.mode == 'attack01' and self.frame == 4:
                self.current_target.lose_hp(self.atk, armor_dmg=self.atk * 0.1)
            elif self.mode == 'attack02' and self.frame == 6:
                self.current_target.lose_hp(self.atk, armor_dmg=self.atk * 0.1)
            elif self.mode == 'attack03' and self.frame == 5:
                self.current_target.lose_hp(self.super_atk, armor_dmg=self.super_atk * 0.1)

    def update(self, *args, **kwargs):
        super().update()
        if self.life:
            if self.mode in ['hurt', 'block', 'attack01', 'attack02', 'attack03'] and self.frame == len(
                    self.frames) - 1:
                self.set_mode('walk')
            elif self.mode == 'walk':
                if self.current_target and abs(self.rect.x - self.current_target.rect.x) <= self.attack_radius:
                    self.set_mode(choice(['attack01', 'attack02']) if random() > 0.1 else 'attack03')
                else:
                    self.rect.x -= 3.2


class RiderOrc(Enemy):
    def __init__(self, coord, group_of_row):
        frame_rate = {
            'walk': 250,
            'attack01': 150,
            'attack02': 100,
            'attack03': 90,
            'block': 100,
            'hurt': 100,
            'death': 250,
        }
        super().__init__(coord, ANIMATIONS['RIDER_ORC'], group_of_row,
                         attack_radius=CELL_SIZE, hp=120, atk=25,
                         frame_rate=frame_rate, armor_hp=40, armor_def=0.2, hurt_cooldown=3, money=14)

    def attack_frame_event(self):
        if self.current_target:
            if self.mode == 'attack01' and self.frame == 4:
                self.current_target.lose_hp(self.atk, armor_dmg=self.atk * 0.1)
            elif self.mode == 'attack02' and self.frame == 5:
                self.current_target.lose_hp(self.atk, armor_dmg=self.atk * 0.1)
            elif self.mode == 'attack03' and self.frame in (5, 9):
                self.current_target.lose_hp(self.atk, armor_dmg=self.atk * 0.1)

    def update(self, *args, **kwargs):
        super().update()
        if self.life:
            if self.mode in ['hurt', 'block', 'attack01', 'attack02', 'attack03'] and self.frame == len(
                    self.frames) - 1:
                self.set_mode('walk')
            elif self.mode == 'walk':
                if self.current_target and abs(self.rect.x - self.current_target.rect.x) <= self.attack_radius:
                    self.set_mode(choice(['attack01', 'attack02', 'attack03']))
                else:
                    self.rect.x -= 3.8


class Skeleton(Enemy):
    def __init__(self, coord, group_of_row):
        frame_rate = {
            'walk': 250,
            'attack01': 150,
            'attack02': 100,
            'attack03': 90,
            'block': 100,
            'hurt': 100,
            'death': 250,
        }
        super().__init__(coord, ANIMATIONS['SKELETON'], group_of_row,
                         attack_radius=CELL_SIZE, hp=70, atk=25,
                         frame_rate=frame_rate, hurt_cooldown=2, money=12)

    def attack_frame_event(self):
        if self.current_target and self.mode in ['attack01', 'attack02'] and self.frame == 3:
            self.current_target.lose_hp(self.atk, armor_dmg=self.atk * 0.1)

    def update(self, *args, **kwargs):
        super().update()
        if self.life:
            if self.mode in ['hurt', 'block', 'attack01', 'attack02'] and self.frame == len(self.frames) - 1:
                self.set_mode('walk')
            elif self.mode == 'walk':
                if self.current_target and abs(self.rect.x - self.current_target.rect.x) <= self.attack_radius:
                    self.set_mode(choice(['attack01', 'attack02']))
                else:
                    self.rect.x -= 3


class GreateswordSkeleton(Enemy):
    def __init__(self, coord, group_of_row):
        frame_rate = {
            'walk': 250,
            'attack01': 120,
            'attack02': 120,
            'attack03': 120,
            'hurt': 100,
            'death': 250,
        }
        super().__init__(coord, ANIMATIONS['GREATSWORD_SKELETON'], group_of_row,
                         attack_radius=CELL_SIZE, hp=80, atk=30,
                         frame_rate=frame_rate, armor_hp=45, armor_def=0.2, hurt_cooldown=3, money=14)

    def attack_frame_event(self):
        if self.current_target:
            if self.mode == 'attack01' and self.frame == 5:
                self.current_target.lose_hp(self.atk, armor_dmg=self.atk * 0.1)
            elif self.mode == 'attack02' and self.frame == 7:
                self.current_target.lose_hp(self.atk, armor_dmg=self.atk * 0.1)
            elif self.mode == 'attack03' and self.frame == 4:
                self.current_target.lose_hp(self.atk, armor_dmg=self.atk * 0.1)

    def update(self, *args, **kwargs):
        super().update()
        if self.life:
            if self.mode in ['hurt', 'attack01', 'attack02', 'attack03'] and self.frame == len(self.frames) - 1:
                self.set_mode('walk')
            elif self.mode == 'walk':
                if self.current_target and abs(self.rect.x - self.current_target.rect.x) <= self.attack_radius:
                    self.set_mode(choice(['attack01', 'attack02', 'attack03']))
                else:
                    self.rect.x -= 3.4


class ArmoredSkeleton(Enemy):
    def __init__(self, coord, group_of_row):
        frame_rate = {
            'walk': 250,
            'attack01': 120,
            'attack02': 120,
            'hurt': 100,
            'death': 250,
        }
        super().__init__(coord, ANIMATIONS['ARMORED_SKELETON'], group_of_row,
                         attack_radius=CELL_SIZE, hp=120, atk=25,
                         frame_rate=frame_rate, armor_hp=50, armor_def=0.25, hurt_cooldown=4, money=18)

    def attack_frame_event(self):
        if self.current_target:
            if self.mode == 'attack01' and self.frame == 5:
                self.current_target.lose_hp(self.atk, armor_dmg=self.atk * 0.1)

    def update(self, *args, **kwargs):
        super().update()
        if self.life:
            if self.mode in ['hurt', 'attack01', 'attack02'] and self.frame == len(self.frames) - 1:
                self.set_mode('walk')
            elif self.mode == 'walk':
                if self.current_target and abs(self.rect.x - self.current_target.rect.x) <= self.attack_radius:
                    self.set_mode('attack01' if random() > 0.1 else 'attack02')
                else:
                    self.rect.x -= 3.2


class Slime(Enemy):
    def __init__(self, coord, group_of_row):
        frame_rate = {
            'walk': 250,
            'attack01': 120,
            'attack02': 100,
            'hurt': 100,
            'death': 250,
        }
        super().__init__(coord, ANIMATIONS['SLIME'], group_of_row,
                         attack_radius=CELL_SIZE, hp=100, atk=15, super_atk=30,
                         frame_rate=frame_rate, hurt_cooldown=2, money=9)

    def attack_frame_event(self):
        if self.current_target:
            if self.mode == 'attack01' and self.frame == 3:
                self.current_target.lose_hp(self.atk, armor_dmg=self.atk * 0.1)
            elif self.mode == 'attack02' and self.frame == 8:
                self.current_target.lose_hp(self.super_atk, armor_dmg=self.super_atk * 0.1)

    def update(self, *args, **kwargs):
        super().update()
        if self.life:
            if self.mode in ['hurt', 'attack01', 'attack02'] and self.frame == len(self.frames) - 1:
                self.set_mode('walk')
            elif self.mode == 'walk':
                if self.current_target and abs(self.rect.x - self.current_target.rect.x) <= self.attack_radius:
                    self.set_mode(choice(['attack01', 'attack02']))
                else:
                    self.rect.x -= 2.5


class Werebear(Enemy):
    def __init__(self, coord, group_of_row):
        frame_rate = {
            'walk': 250,
            'attack01': 120,
            'attack02': 120,
            'attack03': 120,
            'hurt': 100,
            'death': 250,
        }
        super().__init__(coord, ANIMATIONS['WEREBEAR'], group_of_row,
                         attack_radius=CELL_SIZE, hp=150, atk=35, super_atk=40,
                         frame_rate=frame_rate, hurt_cooldown=3, money=15)

    def attack_frame_event(self):
        if self.current_target:
            if self.mode == 'attack01' and self.frame == 5:
                self.current_target.lose_hp(self.atk, armor_dmg=self.atk * 0.1)
            elif self.mode == 'attack02' and self.frame in (4, 9):
                self.current_target.lose_hp(self.atk, armor_dmg=self.atk * 0.1)
            elif self.mode == 'attack03' and self.frame == 5:
                self.current_target.lose_hp(self.super_atk, armor_dmg=self.super_atk * 0.1)

    def update(self, *args, **kwargs):
        super().update()
        if self.life:
            if self.mode in ['hurt', 'attack01', 'attack02', 'attack03'] and self.frame == len(self.frames) - 1:
                self.set_mode('walk')
            elif self.mode == 'walk':
                if self.current_target and abs(self.rect.x - self.current_target.rect.x) <= self.attack_radius:
                    self.set_mode(choice(['attack01', 'attack02']) if random() > 0.1 else 'attack03')
                else:
                    self.rect.x -= 3.6


class Werewolf(Enemy):
    def __init__(self, coord, group_of_row):
        frame_rate = {
            'walk': 250,
            'attack01': 120,
            'attack02': 80,
            'hurt': 100,
            'death': 250,
        }
        super().__init__(coord, ANIMATIONS['WEREWOLF'], group_of_row,
                         attack_radius=CELL_SIZE, hp=70, atk=25,
                         frame_rate=frame_rate, hurt_cooldown=2, money=15)

    def attack_frame_event(self):
        if self.current_target:
            if self.mode == 'attack01' and self.frame == 5:
                self.current_target.lose_hp(self.atk, armor_dmg=self.atk * 0.1)
            elif self.mode == 'attack02':
                if self.frame in (8, 11):
                    self.current_target.lose_hp(self.atk, armor_dmg=self.atk * 0.1)
                elif self.frame == 6:
                    self.rect.x -= 1.3 * CELL_SIZE

    def update(self, *args, **kwargs):
        super().update()
        if self.life:
            if self.mode in ['hurt', 'attack01', 'attack02'] and self.frame == len(self.frames) - 1:
                self.set_mode('walk')
            elif self.mode == 'walk':
                if self.current_target and abs(self.rect.x - self.current_target.rect.x) <= self.attack_radius:
                    self.set_mode('attack01' if random() > 0.1 else 'attack02')
                else:
                    self.rect.x -= 4
