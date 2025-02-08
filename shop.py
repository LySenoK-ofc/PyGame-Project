import pygame

import constant
from sprite_groups import *


class Shop(pygame.sprite.Sprite):
    def __init__(self, unit_type, coord, animations, board, price=0, sale=0):
        super().__init__(all_sprites, shop_units)
        self.animations = animations
        self.mode = 'idle'
        self.frames = self.animations[self.mode]
        self.frame = 0

        self.unit = unit_type
        self.price = price
        self.sale = sale

        self.board = board
        self.drag = False

        self.coord = coord

        self.image = self.frames[self.frame]
        self.rect = self.image.get_rect(center=coord)
        self.mask = pygame.mask.from_surface(self.image)
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = {'idle': 250}

    def update(self):
        self.move()
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate[self.mode]:
            self.last_update = now
            self.frame = (self.frame + 1) % len(self.frames)
            self.image = self.frames[self.frame]

    def move(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_button = pygame.mouse.get_pressed()
        local_mouse_pos = (mouse_pos[0] - self.rect.x, mouse_pos[1] - self.rect.y)

        if 0 <= local_mouse_pos[0] < self.rect.width and 0 <= local_mouse_pos[1] < self.rect.height:
            if self.mask.get_at(local_mouse_pos):
                if len(drag_units) == 0 and mouse_button[0]:
                    drag_units.add(self)
                    self.drag = True

                if not mouse_button[0] and self.drag:
                    if constant.cash - self.price >= 0 and self.board.get_click(mouse_pos, 'Troops', self.unit):
                        constant.cash -= self.price
                    self.rect.center = self.coord
                    self.drag = False
                    drag_units.remove(self)

        if self.drag:
            self.rect.center = mouse_pos
