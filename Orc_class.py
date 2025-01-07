from random import choice, randrange
from load_image_func import load_image
from sprite_groups import characters

import pygame


class Orc(pygame.sprite.Sprite):
    hp = 50
    atk = 10

    def __init__(self, group):
        super().__init__(group)
        # Словарь анимаций
        self.animations = {
            'walk': [load_image(f'animations/Orc/Orc-Walk/{i}.png', reverse=True) for i in range(1, 9)],
            'attack': {
                'attack1': [load_image(f'animations/Orc/Orc-Attack01/{i}.png', reverse=True) for i in range(1, 7)],
                'attack2': [load_image(f'animations/Orc/Orc-Attack02/{i}.png', reverse=True) for i in range(1, 7)]},
            'hurt': [load_image(f'animations/Orc/Orc-Hurt/{i}.png', reverse=True) for i in range(1, 5)],
            'death': [load_image(f'animations/Orc/Orc-Death/{i}.png', reverse=True) for i in range(1, 5)],
        }
        self.mode = 'walk'
        self.frames = self.animations[self.mode]
        self.frame = 0
        self.current_target = None
        self.hurt = False
        self.life = True

        self.image = self.animations[self.mode][self.frame]

        # Создаём маску сразу, так как во время удара орк поднимает топор и залезает на другую дорожку
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect.x = 800
        self.rect.y = randrange(2, 7) * 64

        self.last_update = pygame.time.get_ticks()
        self.frame_rate = {
            'walk': 250,
            'attack': 250,
            'hurt': 35,
            'death': 250,
        }

        self.check = True

    def set_mode(self, mode):
        if mode == 'attack':
            self.mode = mode
            self.frames = self.animations[self.mode][choice(['attack1', 'attack2'])]
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

            # особые проверки для атаки
            if self.mode == 'attack':
                # Обновление анимации удара
                if self.frame == len(self.frames) - 1:
                    self.set_mode('attack')

                # Удар в нужный кадр
                if self.frame == 4:
                    self.current_target.lose_hp(Orc.atk)

                # Проверка на смерть лучника
                if not self.current_target.life:
                    self.set_mode('walk')
                    self.current_target = None

    def update(self, *args, **kwargs):
        if self.life:
            if self.hurt:
                self.set_mode('hurt')
                self.update_animation()
                if self.frame == len(self.frames) - 1:
                    if self.current_target:
                        self.set_mode('attack')
                    else:
                        self.set_mode('walk')
                    self.hurt = False

            elif self.mode == 'walk':
                self.update_animation()
                self.rect.x -= 3
                for soldier in characters:
                    if pygame.sprite.collide_mask(self, soldier):
                        self.current_target = soldier
                        self.set_mode('attack')

            elif self.mode == 'attack':
                self.update_animation()

        else:
            self.set_mode('death')
            self.update_animation()
            if self.frame == len(self.animations['death']) - 1:
                self.kill()

    def lose_hp(self, count):
        if self.life:
            self.hp -= count
            if self.hp <= 0:
                self.life = False
            self.hurt = True
