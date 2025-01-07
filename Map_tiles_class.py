from load_image_func import load_image

import pygame


class Map_tile(pygame.sprite.Sprite):
    def __init__(self, group, coord, image):
        super().__init__(group)
        self.image = load_image(image)
        self.rect = self.image.get_rect()
        self.rect.x = coord[0]
        self.rect.y = coord[1]


class Animated_map_object(pygame.sprite.Sprite):
    def __init__(self, group, coord, images, reverse=False):
        super().__init__(group)
        self.image = load_image(images[0])
        self.anim = [load_image(image, reverse) for image in images]
        self.rect = self.image.get_rect()
        self.rect.x = coord[0]
        self.rect.y = coord[1]

        self.frame = 0  # текущий кадр
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 150  # как быстро кадры меняются

    def update(self, *args, **kwargs):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.anim):
                self.frame = 0
            self.image = self.anim[self.frame]
