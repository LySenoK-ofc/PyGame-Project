from random import choice, randrange
from load_image_func import load_image
from sprite_groups import characters, killed_entities, mobs

import pygame

IDLE = 'Idle'
WALK = 'Walk'
DEATH = 'Death'
ATTACK1 = 'Attack01'
ATTACK2 = 'Attack02'

class Orc(pygame.sprite.Sprite):
    hp = 50
    atk = 10

    def __init__(self, group):
        super().__init__(group)
        self.anim_walk = [load_image('animations/Orc/Orc-Walk/1.png', reverse=True),
                          load_image('animations/Orc/Orc-Walk/2.png', reverse=True),
                          load_image('animations/Orc/Orc-Walk/3.png', reverse=True),
                          load_image('animations/Orc/Orc-Walk/4.png', reverse=True),
                          load_image('animations/Orc/Orc-Walk/5.png', reverse=True),
                          load_image('animations/Orc/Orc-Walk/6.png', reverse=True),
                          load_image('animations/Orc/Orc-Walk/7.png', reverse=True),
                          load_image('animations/Orc/Orc-Walk/8.png', reverse=True)]
        self.anim_death = [load_image('animations/Orc/Orc-Death/1.png', reverse=True),
                           load_image('animations/Orc/Orc-Death/2.png', reverse=True),
                           load_image('animations/Orc/Orc-Death/3.png', reverse=True),
                           load_image('animations/Orc/Orc-Death/4.png', reverse=True)]
        self.anim_attack1 = [load_image('animations/Orc/Orc-Attack01/1.png', reverse=True),
                             load_image('animations/Orc/Orc-Attack01/2.png', reverse=True),
                             load_image('animations/Orc/Orc-Attack01/3.png', reverse=True),
                             load_image('animations/Orc/Orc-Attack01/4.png', reverse=True),
                             load_image('animations/Orc/Orc-Attack01/5.png', reverse=True),
                             load_image('animations/Orc/Orc-Attack01/6.png', reverse=True)]
        self.anim_attack2 = [load_image('animations/Orc/Orc-Attack02/1.png', reverse=True),
                             load_image('animations/Orc/Orc-Attack02/2.png', reverse=True),
                             load_image('animations/Orc/Orc-Attack02/3.png', reverse=True),
                             load_image('animations/Orc/Orc-Attack02/4.png', reverse=True),
                             load_image('animations/Orc/Orc-Attack02/5.png', reverse=True),
                             load_image('animations/Orc/Orc-Attack02/6.png', reverse=True)]
        self.mode = WALK
        self.image = self.anim_walk[0]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = 1200
        self.rect.y = randrange(2, 7) * 75 + 32

        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate_walk = 250
        self.frame_rate_attack = 250
        self.frame_rate_death = 250

        self.check = True

    def update(self, *args, **kwargs):
        self.mask = pygame.mask.from_surface(self.image)
        if self.check:
            for soldier in characters:
                if pygame.sprite.collide_mask(self, soldier):
                    self.mode = 'Attack'
                    self.frame = 0
                    self.check = False

        now = pygame.time.get_ticks()
        if self.mode == WALK:
            if now - self.last_update > self.frame_rate_walk:
                self.last_update = now
                self.frame += 1
                if self.frame == len(self.anim_walk):
                    self.frame = 0
                self.image = self.anim_walk[self.frame]
            self.rect.x -= 3

        if self.mode == DEATH:
            if now - self.last_update > self.frame_rate_death:
                self.last_update = now
                self.frame += 1
                if self.frame == len(self.anim_death):
                    self.remove(killed_entities)
                    self.frame = 0
                self.image = self.anim_death[self.frame]

        if self.mode == 'Attack':
            if self.frame == 0:
                self.attack_number = choice([ATTACK1, ATTACK2])
            if now - self.last_update > self.frame_rate_attack:
                self.last_update = now
                self.frame += 1

            if self.attack_number == ATTACK1:
                self.image = self.anim_attack1[self.frame]
            else:
                self.image = self.anim_attack2[self.frame]

            if self.frame == len(self.anim_attack1):
                self.frame = 0

            if self.frame == 4:
                for soldier in characters:
                    if pygame.sprite.collide_mask(self, soldier):
                        soldier.lose_hp(Orc.atk)
                else:
                    self.mode = WALK
                    self.check = True

    def lose_hp(self, count):
        self.hp -= count
        if self.hp <= 0:
            self.mode = DEATH
            self.frame = 0
            self.add(killed_entities)
            self.remove(mobs)