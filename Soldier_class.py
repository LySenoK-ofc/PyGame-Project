from load_image_func import load_image
from random import choice
from sprite_groups import shells, killed_entities, characters, mobs
from demo_project import board

import pygame

IDLE = 'Idle'
WALK = 'Walk'
ATTACK = 'Attack'
BOW_ATTACK = 'Bow_attack'


class Soldier(pygame.sprite.Sprite):
    hp = 50
    atk = 10

    def __init__(self, group, coord):
        super().__init__(group)
        self.mode = IDLE
        # Словарь анимаций
        self.animations = {
            'idle': [load_image(f'animations/Soldier/Soldier-Idle/idle{i}.png') for i in range(1, 7)],
            'attack': {
                'attack1': [load_image(f'animations/Soldier/Soldier-Attack01/attack{i}.png') for i in range(1, 7)],
                'attack2': [load_image(f'animations/Soldier/Soldier-Attack02/attack{i}.png') for i in range(1, 7)],
                'bow_attack': [load_image(f'animations/Soldier/Soldier-Attack03/attack{i}.png') for i in range(1, 10)],
            },
            'hurt': [load_image(f'animations/Soldier/Soldier-Hurt/hurt{i}.png') for i in range(1, 5)],
            'death': [load_image(f'animations/Soldier/Soldier-Death/death{i}.png') for i in range(1, 5)],
        }
        self.mode = 'idle'
        self.frames = self.animations[self.mode]
        self.frame = 0
        self.hurt = False
        self.life = True

        self.current_target = None

        self.image = self.frames[self.frame]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = coord

        self.mask = pygame.mask.from_surface(self.image)

        self.last_update = pygame.time.get_ticks()

        # Скорость смены кадров
        self.frame_rate = {
            'idle': 250,
            'attack': 115,
            'hurt': 150,
            'death': 250,
        }

    def set_mode(self, mode):
        if mode in ['attack', 'bow_attack']:
            self.mode = mode
            if mode == 'attack':
                self.frames = self.animations[self.mode][choice(['attack1', 'attack2'])]
            else:
                self.frames = self.animations['attack']['bow_attack']
            self.frame = 0
        else:
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

            if self.mode == 'bow_attack' and self.frame == 7:
                Arrow(shells, [self.rect.x, self.rect.y])

    def update(self):
        if self.life:
            if self.hurt:
                self.set_mode('hurt')
                self.update_animation()
                if self.frame == len(self.frames) - 1:
                    self.set_mode('idle')
                    self.hurt = False
            else:
                if self.mode == 'idle':
                    self.update_animation()
                    # mode = None
                    # for mob in mobs:
                    #     if pygame.sprite.collide_mask(self, mob):
                    #         self.current_target = mob
                    #         mode = 'attack'
                    #         break
                    #     elif ((mob.rect.y - board.top) // board.cell_size ==
                    #           (self.rect.y - board.top) // board.cell_size):
                    #         self.current_target = mob
                    #         mode = 'bow_attack'
                    # if mode:
                    #     self.set_mode(mode)

        else:
            self.set_mode('death')
            self.update_animation()
            if self.frame == len(self.frames) - 1:
                self.kill()

    def lose_hp(self, count):
        if self.life:
            self.hp -= count
            if self.hp <= 0:
                self.life = False
            self.hurt = True


class Arrow(pygame.sprite.Sprite):
    def __init__(self, group, coord):
        super().__init__(group)
        self.image = load_image('animations/Arrow01(100x100).png')
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = coord[0] + 50
        self.rect.y = coord[1] + 25

    def update(self, *args, **kwargs):
        for mob in mobs:
            if pygame.sprite.collide_mask(self, mob):
                mob.lose_hp(Soldier.atk)
                self.remove(shells)
        else:
            self.rect.x += 12.5
