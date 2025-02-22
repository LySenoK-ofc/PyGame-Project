import pygame
from sprite_groups import groups


class Shop(pygame.sprite.Sprite):
    def __init__(self, unit_type, coord, animations, board, price=0, sale=0):
        """Юнит, которого можно купить, перетащив его на поле, а так же продать."""
        super().__init__(groups['all_sprites'], groups['shop_units'])
        self.animations = animations
        self.mode = 'idle'
        self.frames = self.animations[self.mode]
        self.frame = 0

        self.unit = unit_type
        self.price = price
        self.sale = sale
        self.board = board
        self.coord = coord

        self.image = self.frames[self.frame]
        self.rect = self.image.get_rect(center=coord)
        self.mask = pygame.mask.from_surface(self.image)
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = {'idle': 250}

        self.info = f'Стоимость:{self.price}\nПродажа:{self.sale}'

    def update(self):
        """Обновляет анимацию и положение."""
        self.move()
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate[self.mode]:
            self.last_update = now
            self.frame = (self.frame + 1) % len(self.frames)
            self.image = self.frames[self.frame]

    def move(self):
        """Обрабатывает перемещение юнита."""
        mouse_pos = pygame.mouse.get_pos()
        mouse_button = pygame.mouse.get_pressed()
        local_mouse_pos = (mouse_pos[0] - self.rect.x, mouse_pos[1] - self.rect.y)

        if 0 <= local_mouse_pos[0] < self.rect.width and 0 <= local_mouse_pos[1] < self.rect.height:
            if self.mask.get_at(local_mouse_pos):
                if len(groups['drag_units']) == 0 and mouse_button[0]:
                    # Начинаем перетаскивание юнита
                    groups['drag_units'].add(self)

                if not mouse_button[0] and self in groups['drag_units']:
                    self.spawn_unit(mouse_pos)

            if self in groups['drag_units']:
                # Тащим юнита за мышкой
                self.rect.center = mouse_pos

    def spawn_unit(self, mouse_pos):
        """Покупаем и/или перемещаем юнита в магазин."""
        self.rect.center = self.coord
        groups['drag_units'].remove(self)
        self.board.get_click(mouse_pos, self)
