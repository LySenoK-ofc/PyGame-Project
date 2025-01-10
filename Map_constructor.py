from load_image_func import load_image
from sprite_groups import map_tiles, map_objects, animated_map_objects

import pygame


class Map_constructor:
    used_tiles = {1: 'map_tiles/Tiles/FieldsTile_38.png',
                  2: 'map_tiles/Tiles/FieldsTile_31.png',
                  3: 'map_tiles/Tiles/FieldsTile_40.png',
                  4: 'map_tiles/Tiles/FieldsTile_43.png',
                  5: 'map_tiles/Tiles/FieldsTile_44.png',
                  6: 'map_tiles/Tiles/FieldsTile_47.png'}

    def __init__(self, map_width, map_height, board):
        self.map_width = map_width
        self.map_height = map_height
        self.board = board

        # Создаем карту из клеток

        for i in range(self.map_height):
            for j in range(self.map_width):
                if i >= self.map_height - 2:
                    Map_tile(map_tiles, (j * 75, i * 75), self.used_tiles[1])
                elif self.board.left // 64 < j and self.board.top // 64 <= i < self.map_height - 1:
                    Map_tile(map_tiles, (j * 75, i * 75), self.used_tiles[2])
                elif i == 2 and (j == 6 or j == 9 or j == 12 or j == 15):
                    Map_tile(map_tiles, (j * 75, i * 75), self.used_tiles[6])
                elif i >= self.map_height - 2:
                    Map_tile(map_tiles, (j * 75, i * 75), self.used_tiles[1])
                elif i == 4 and j == 5:
                    Map_tile(map_tiles, (j * 75, i * 75), self.used_tiles[4])
                elif j == 5 and i == 8:
                    Map_tile(map_tiles, (j * 75, i * 75), self.used_tiles[5])
                elif i == 1:
                    Map_tile(map_tiles, (j * 75, i * 75), self.used_tiles[1])
                elif 0 <= j < 5:
                    Map_tile(map_tiles, (j * 75, i * 75), self.used_tiles[1])
                elif i <= 3:
                    Map_tile(map_tiles, (j * 75, i * 75), self.used_tiles[1])
                elif j == 5:
                    Map_tile(map_tiles, (j * 75, i * 75), self.used_tiles[3])

        # Создаем объекты

        Map_tile(map_objects, (145, 300), 'map_tiles/Objects/camp/1.png')
        Map_tile(map_objects, (10, 250), 'map_tiles/Objects/camp/1.png', reverse=True)
        Map_tile(map_objects, (10, 550), 'map_tiles/Objects/camp/3.png', reverse=True)

        Map_tile(map_objects, (175, 425), 'map_tiles/Objects/decor/Log2.png')
        Map_tile(map_objects, (75, 500), 'map_tiles/Objects/decor/Log3.png')

        Map_tile(map_objects, (15, 455), 'map_tiles/Objects/decor/Box1.png')

        Map_tile(map_objects, (40, 333), 'map_tiles/Objects/decor/Box1.png')
        Map_tile(map_objects, (13, 335), 'map_tiles/Objects/decor/Box1.png')
        Map_tile(map_objects, (26, 313), 'map_tiles/Objects/decor/Box1.png')

        Map_tile(map_objects, (221, 566), 'map_tiles/Objects/fences/8.png', reverse=True)
        Map_tile(map_objects, (191, 589), 'map_tiles/Objects/fences/8.png', reverse=True)
        Map_tile(map_objects, (161, 612), 'map_tiles/Objects/fences/8.png', reverse=True)
        Map_tile(map_objects, (0, 630), 'map_tiles/Objects/fences/1.png')
        Map_tile(map_objects, (54, 630), 'map_tiles/Objects/fences/1.png')
        Map_tile(map_objects, (108, 630), 'map_tiles/Objects/fences/1.png')

        Map_tile(map_objects, (0, 220), 'map_tiles/Objects/fences/1.png')
        Map_tile(map_objects, (54, 220), 'map_tiles/Objects/fences/1.png')
        Map_tile(map_objects, (108, 220), 'map_tiles/Objects/fences/1.png')
        Map_tile(map_objects, (161, 220), 'map_tiles/Objects/fences/8.png')
        Map_tile(map_objects, (191, 242), 'map_tiles/Objects/fences/8.png')
        Map_tile(map_objects, (221, 264), 'map_tiles/Objects/fences/8.png')

        Map_tile(map_objects, (515, 150), 'map_tiles/Objects/shadows/5.png')
        Map_tile(map_objects, (740, 150), 'map_tiles/Objects/shadows/5.png')
        Map_tile(map_objects, (965, 150), 'map_tiles/Objects/shadows/5.png')
        Map_tile(map_objects, (1190, 150), 'map_tiles/Objects/shadows/5.png')

        Map_tile(map_objects, (500, 55), 'map_tiles/Objects/decor/Tree1.png')
        Map_tile(map_objects, (725, 55), 'map_tiles/Objects/decor/Tree1.png')
        Map_tile(map_objects, (950, 55), 'map_tiles/Objects/decor/Tree1.png')
        Map_tile(map_objects, (1175, 55), 'map_tiles/Objects/decor/Tree1.png')

        Map_tile(map_objects, (440, 680), 'map_tiles/Objects/pointers/1.png')
        Map_tile(map_objects, (1350, 215), 'map_tiles/Objects/pointers/4.png')

        Map_tile(map_objects, (1142, 725), 'map_tiles/Objects/bushes/1.png')
        Map_tile(map_objects, (345, 113), 'map_tiles/Objects/bushes/1.png')
        Map_tile(map_objects, (1335, 35), 'map_tiles/Objects/bushes/1.png')
        Map_tile(map_objects, (180, 80), 'map_tiles/Objects/bushes/2.png')
        Map_tile(map_objects, (560, 670), 'map_tiles/Objects/bushes/2.png')
        Map_tile(map_objects, (645, 85), 'map_tiles/Objects/bushes/2.png')
        Map_tile(map_objects, (25, 115), 'map_tiles/Objects/bushes/3.png')
        Map_tile(map_objects, (1100, 740), 'map_tiles/Objects/bushes/3.png')
        Map_tile(map_objects, (415, 725), 'map_tiles/Objects/bushes/3.png')
        Map_tile(map_objects, (780, 735), 'map_tiles/Objects/bushes/4.png')
        Map_tile(map_objects, (425, 245), 'map_tiles/Objects/bushes/4.png')
        Map_tile(map_objects, (170, 670), 'map_tiles/Objects/bushes/4.png', reverse=True)
        Map_tile(map_objects, (75, 725), 'map_tiles/Objects/bushes/5.png')
        Map_tile(map_objects, (1400, 665), 'map_tiles/Objects/bushes/5.png')
        Map_tile(map_objects, (75, 45), 'map_tiles/Objects/bushes/5.png')
        Map_tile(map_objects, (1400, 150), 'map_tiles/Objects/bushes/6.png')
        Map_tile(map_objects, (610, 690), 'map_tiles/Objects/bushes/6.png')
        Map_tile(map_objects, (225, 145), 'map_tiles/Objects/bushes/6.png')

        Map_tile(map_objects, (250, 125), 'map_tiles/Objects/stones/1.png')
        Map_tile(map_objects, (165, 270), 'map_tiles/Objects/stones/2.png')
        Map_tile(map_objects, (65, 185), 'map_tiles/Objects/stones/3.png')
        Map_tile(map_objects, (250, 700), 'map_tiles/Objects/stones/7.png')
        Map_tile(map_objects, (15, 780), 'map_tiles/Objects/stones/9.png')
        Map_tile(map_objects, (1395, 85), 'map_tiles/Objects/stones/10.png')
        Map_tile(map_objects, (900, 685), 'map_tiles/Objects/stones/11.png')
        Map_tile(map_objects, (1365, 765), 'map_tiles/Objects/stones/12.png')
        Map_tile(map_objects, (135, 145), 'map_tiles/Objects/stones/16.png')

        # Создаем анимированные объекты

        Animated_map_object(animated_map_objects, (70, 400),
                            ('map_tiles/Animated_Objects/campfire/active_campfire/1.png',
                             'map_tiles/Animated_Objects/campfire/active_campfire/2.png',
                             'map_tiles/Animated_Objects/campfire/active_campfire/3.png',
                             'map_tiles/Animated_Objects/campfire/active_campfire/4.png',
                             'map_tiles/Animated_Objects/campfire/active_campfire/5.png',
                             'map_tiles/Animated_Objects/campfire/active_campfire/6.png',))

        Animated_map_object(animated_map_objects, (245, 500),
                            ('map_tiles/Animated_Objects/flag/1.png',
                             'map_tiles/Animated_Objects/flag/2.png',
                             'map_tiles/Animated_Objects/flag/3.png',
                             'map_tiles/Animated_Objects/flag/4.png',
                             'map_tiles/Animated_Objects/flag/5.png',
                             'map_tiles/Animated_Objects/flag/6.png'), True)
        Animated_map_object(animated_map_objects, (245, 200),
                            ('map_tiles/Animated_Objects/flag/1.png',
                             'map_tiles/Animated_Objects/flag/2.png',
                             'map_tiles/Animated_Objects/flag/3.png',
                             'map_tiles/Animated_Objects/flag/4.png',
                             'map_tiles/Animated_Objects/flag/5.png',
                             'map_tiles/Animated_Objects/flag/6.png'), True)


class Map_tile(pygame.sprite.Sprite):
    def __init__(self, group, coord, image, reverse=False):
        super().__init__(group)
        self.image = load_image(image, reverse)
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
