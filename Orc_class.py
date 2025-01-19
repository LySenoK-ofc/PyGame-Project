from random import choice
from sprite_groups import *
import pygame
from load_animations import load_anim


class Orc(pygame.sprite.Sprite):
    # Базовое хп
    hp = 50
    # Урон
    atk = 10

    def __init__(self, coord):
        super().__init__(all_sprites, mobs)

        # Словарь анимаций орка
        self.animations = load_anim("assets/animations/Orcs/orc/Orc.png", 'orcs', 'orc', True)
        print(self.animations)

        # Начальный режим - "ходьба"
        self.mode = 'walk'

        self.frames = self.animations[self.mode]
        self.frame = 0
        self.current_target = None
        self.hurt = False
        self.life = True

        self.image = self.animations[self.mode][self.frame]

        # Создаём маску
        self.mask = pygame.mask.from_surface(self.image)

        # Устанавливаем начальную позицию орка
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = coord

        # Время последнего обновления анимации
        self.last_update = pygame.time.get_ticks()

        # Скорость смены кадров для каждого режима
        self.frame_rate = {
            'walk': 250,
            'attack01': 250,
            'attack02': 250,
            'hurt': 10,
            'death': 250,
        }

        self.check = True  # Вспомогательная переменная для проверок

    def set_mode(self, mode):
        # Устанавливаем новый режим и загружаем соответствующие кадры
        if mode in ['attack01', 'attack02']:
            self.mode = mode
            self.frames = self.animations[self.mode]
            self.frame = 0  # Сбрасываем текущий кадр
        else:
            # Если режим изменился
            if self.mode != mode:
                self.mode = mode
                self.frames = self.animations[self.mode]
                self.frame = 0  # Сбрасываем текущий кадр

    def update_animation(self):
        now = pygame.time.get_ticks()
        # Проверяем, прошло ли достаточно времени для обновления кадра
        if now - self.last_update > self.frame_rate[self.mode]:
            self.last_update = now  # Обновляем время последнего кадра
            # Переход к следующему кадру
            self.frame = (self.frame + 1) % len(self.frames)
            # Обновляем изображение
            self.image = self.frames[self.frame]

            # Особая логика для режима "атака"
            if self.mode in ['attack01', 'attack02']:
                # Если кадры закончились, выбираем случайную атаку
                if self.frame == len(self.frames) - 1:
                    self.set_mode(choice(['attack01', 'attack02']))

                # Удар по цели на определённом кадре
                if self.frame == 3:
                    self.current_target.lose_hp(Orc.atk)

                # Если цель мертва, возвращаемся в режим "ходьба"
                if not self.current_target.life:
                    self.set_mode('walk')
                    self.current_target = None

    def update(self, *args, **kwargs):
        self.update_animation()  # Обновляем анимацию
        # Если орк жив
        if self.life:

            if self.mode == 'hurt':  # Если орк получил урон
                # После завершения анимации "получение урона"
                if self.frame == len(self.frames) - 1:
                    # Возвращаемся в режим "атака" или "ходьба"
                    if self.current_target:
                        self.set_mode(choice(['attack01', 'attack02']))
                    else:
                        self.set_mode('walk')

            elif self.mode == 'walk':  # Если орк в режиме "ходьба"
                self.rect.x -= 3  # Двигаем орка влево
                # Проверяем столкновения с солдатами
                for soldier in characters:
                    if pygame.sprite.collide_mask(self, soldier):
                        self.current_target = soldier  # Устанавливаем цель
                        self.set_mode(choice(['attack01', 'attack02']))  # Переходим в режим "атака"

        else:  # Если орк мёртв
            self.set_mode('death')  # Переходим в режим "смерть"
            # Удаляем орка после завершения анимации смерти
            if self.frame == len(self.animations['death']) - 1:
                self.kill()

    def lose_hp(self, count):
        # Уменьшаем здоровье орка при получении урона
        if self.life:
            self.hp -= count
            # Если здоровье орка меньше или равно 0
            if self.hp <= 0:
                self.life = False  # Орк умирает
            if self.mode != 'hurt':
                self.set_mode('hurt')
