from random import choice

from all_animations import ANIMATIONS
from sprite_groups import *
import pygame
from constant import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, coord, animations, grop_of_row, frame_rate, hp, atk, attack_radius=None, super_atk=None):
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
        self.kills = 0

        if super_atk:
            self.super_atk = super_atk
        if attack_radius:
            self.attack_radius = attack_radius

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

            if isinstance(self, Orc):
                if (self.mode in ['attack01', 'attack02'] and
                        abs(self.rect.x - self.current_target.rect.x) <= self.attack_radius and
                        self.frame == 3):
                    self.current_target.lose_hp(self.atk, self)

    def lose_hp(self, count, killer=None):
        if self.life:
            self.hp -= count
            if self.hp <= 0:
                self.life = False
                if killer:
                    killer.kills += 1
            self.set_mode('hurt')

    def set_target(self, new_target):
        if self.current_target is None:
            self.current_target = new_target

        if abs(self.current_target.rect.x - self.rect.x) > abs(new_target.rect.x - self.rect.x):
            self.current_target = new_target

    def update(self, *args, **kwargs):

        if self.rect.x < 0 or self.rect.left > WIDTH or self.rect.y < 0 or self.rect.top > HEIGHT:
            self.life = False
            self.kill()

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
        super().__init__(coord, ANIMATIONS['ORC'], grop_of_row, attack_radius=CELL_SIZE, hp=60, atk=20,
                         frame_rate=frame_rate)

    def update(self, *args, **kwargs):
        super().update()
        if self.life:
            if self.mode == 'hurt' and self.frame == len(self.frames) - 1:
                self.set_mode('walk')

            elif self.mode == 'walk':
                if (self.current_target is not None and
                        abs(self.rect.x - self.current_target.rect.x) <= self.attack_radius):
                    self.set_mode(choice(['attack01', 'attack02']))
                else:
                    self.rect.x -= 3

            elif self.mode in ['attack01', 'attack02'] and self.current_target and not self.current_target.life:
                self.current_target = None
                self.set_mode('walk')
