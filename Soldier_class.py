from load_image_func import load_image
from random import choice
from sprite_groups import shells, killed_entities, characters, mobs

import pygame

IDLE = 'Idle'
WALK = 'Walk'
DEATH = 'Death'
ATTACK1 = 'Attack01'
ATTACK2 = 'Attack02'
BOW_ATTACK = 'Bow_attack'


class Soldier(pygame.sprite.Sprite):
    hp = 50
    atk = 10

    def __init__(self, group, coord):
        super().__init__(group)
        self.mode = IDLE
        self.anim_idle = [load_image('animations/Soldier/Soldier-Idle/idle1.png'),
                          load_image('animations/Soldier/Soldier-Idle/idle2.png'),
                          load_image('animations/Soldier/Soldier-Idle/idle3.png'),
                          load_image('animations/Soldier/Soldier-Idle/idle4.png'),
                          load_image('animations/Soldier/Soldier-Idle/idle5.png'),
                          load_image('animations/Soldier/Soldier-Idle/idle6.png')]
        self.anim_attack1 = [load_image('animations/Soldier/Soldier-Attack01/attack1.png'),
                             load_image('animations/Soldier/Soldier-Attack01/attack2.png'),
                             load_image('animations/Soldier/Soldier-Attack01/attack3.png'),
                             load_image('animations/Soldier/Soldier-Attack01/attack4.png'),
                             load_image('animations/Soldier/Soldier-Attack01/attack5.png'),
                             load_image('animations/Soldier/Soldier-Attack01/attack6.png')]
        self.anim_attack2 = [load_image('animations/Soldier/Soldier-Attack02/attack1.png'),
                             load_image('animations/Soldier/Soldier-Attack02/attack2.png'),
                             load_image('animations/Soldier/Soldier-Attack02/attack3.png'),
                             load_image('animations/Soldier/Soldier-Attack02/attack4.png'),
                             load_image('animations/Soldier/Soldier-Attack02/attack5.png'),
                             load_image('animations/Soldier/Soldier-Attack02/attack6.png')]
        self.anim_bow_attack = [load_image('animations/Soldier/Soldier-Attack03/attack1.png'),
                                load_image('animations/Soldier/Soldier-Attack03/attack2.png'),
                                load_image('animations/Soldier/Soldier-Attack03/attack3.png'),
                                load_image('animations/Soldier/Soldier-Attack03/attack4.png'),
                                load_image('animations/Soldier/Soldier-Attack03/attack5.png'),
                                load_image('animations/Soldier/Soldier-Attack03/attack6.png'),
                                load_image('animations/Soldier/Soldier-Attack03/attack7.png'),
                                load_image('animations/Soldier/Soldier-Attack03/attack8.png'),
                                load_image('animations/Soldier/Soldier-Attack03/attack9.png')]
        self.anim_death = [load_image('animations/Soldier/Soldier-Death/death1.png'),
                           load_image('animations/Soldier/Soldier-Death/death2.png'),
                           load_image('animations/Soldier/Soldier-Death/death3.png'),
                           load_image('animations/Soldier/Soldier-Death/death4.png'), ]
        self.image = self.anim_idle[0]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = coord[0]
        self.rect.y = coord[1]

        self.frame = 0  # текущий кадр
        self.last_update = pygame.time.get_ticks()
        self.frame_rate_idle = 250  # как быстро кадры меняются
        self.frame_rate_attack = 115
        self.frame_rate_death = 250

    def update(self, attack_n=None):
        self.mask = pygame.mask.from_surface(self.image)
        now = pygame.time.get_ticks()
        if self.mode == IDLE:
            if now - self.last_update > self.frame_rate_idle:
                self.last_update = now
                self.frame += 1
                if self.frame == len(self.anim_idle):
                    self.frame = 0
                self.image = self.anim_idle[self.frame]
        elif self.mode == 'Attack':
            if self.frame == 0:
                self.attack_number = choice([ATTACK1, ATTACK2])
            if now - self.last_update > self.frame_rate_attack:
                self.last_update = now
                self.frame += 1
                if self.frame == len(self.anim_attack1):
                    self.frame = 0

                if self.attack_number == ATTACK1:
                    self.image = self.anim_attack1[self.frame]
                else:
                    self.image = self.anim_attack2[self.frame]
        elif self.mode == BOW_ATTACK:
            if now - self.last_update > self.frame_rate_attack:
                self.last_update = now
                self.frame += 1
                if self.frame == 7:
                    Arrow(shells, [self.rect.x, self.rect.y])
                if self.frame == len(self.anim_bow_attack):
                    self.frame = 0
                self.image = self.anim_bow_attack[self.frame]
        elif self.mode == DEATH:
            if now - self.last_update > self.frame_rate_death:
                self.last_update = now
                self.frame += 1
                if self.frame == len(self.anim_death):
                    self.remove(killed_entities)
                    self.frame = 0
                self.image = self.anim_death[self.frame]

    def lose_hp(self, count):
        self.hp -= count
        if self.hp <= 0:
            self.mode = DEATH
            self.frame = 0
            self.add(killed_entities)
            self.remove(characters)
            return True
        self.image = load_image('animations/Soldier/Soldier-Hurt/hurt2.png')
        return False

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
