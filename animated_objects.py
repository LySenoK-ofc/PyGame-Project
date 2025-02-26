import pygame

from sprite_groups import groups


class AnimatedMapObject(pygame.sprite.Sprite):
    def __init__(self, coord, anim):
        super().__init__(groups['animated_map_objects'], groups['all_sprites'])
        self.frames = anim
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = coord

        self.frame = 0  # текущий кадр
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 250  # как быстро кадры меняются

    def update(self, *args, **kwargs):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame = (self.frame + 1) % len(self.frames)
            self.image = self.frames[self.frame]
