from Units import Knight, Archer, Wizard, Priest, ArmoredAxeman, SwordsMan, KnightTemplar, Lancer
from all_animations import ANIMATIONS
from constant import CELL_SIZE, LEFT, WIDTH_CELL, TOP, HEIGHT_CELL
from load_image_func import load_image
from shop import Shop
from sprite_groups import groups

import pygame

used_tiles = {1: 'assets/map_tiles/Tiles/FieldsTile_38.png',
              2: 'assets/map_tiles/Tiles/FieldsTile_31.png',
              3: 'assets/map_tiles/Tiles/FieldsTile_40.png',
              4: 'assets/map_tiles/Tiles/FieldsTile_43.png',
              5: 'assets/map_tiles/Tiles/FieldsTile_44.png',
              6: 'assets/map_tiles/Tiles/FieldsTile_47.png'}


def load_level(filename):
    filename = "assets/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(field):
    coords = []
    for y in range(len(field)):
        for x in range(len(field[y])):
            if field[y][x] == '.':
                MapTile(groups['map_tiles'], (x * CELL_SIZE, y * CELL_SIZE), image=used_tiles[1])
            elif field[y][x] == '#':
                MapTile(groups['map_tiles'], (x * CELL_SIZE, y * CELL_SIZE), image=used_tiles[2])
            elif field[y][x] == '=':
                MapTile(groups['map_tiles'], (x * CELL_SIZE, y * CELL_SIZE), image=used_tiles[3])
            elif field[y][x] == '(':
                MapTile(groups['map_tiles'], (x * CELL_SIZE, y * CELL_SIZE), image=used_tiles[4])
            elif field[y][x] == ')':
                MapTile(groups['map_tiles'], (x * CELL_SIZE, y * CELL_SIZE), image=used_tiles[5])
            elif field[y][x] == '@':
                MapTile(groups['map_tiles'], (x * CELL_SIZE, y * CELL_SIZE), image=used_tiles[6])
                coords.append((x * CELL_SIZE + CELL_SIZE / 2, y * CELL_SIZE + CELL_SIZE / 2))
    return coords


class MapConstructor:
    def __init__(self, map_width, map_height, board, shop_unit_coord):
        self.map_width = map_width
        self.map_height = map_height
        self.board = board

        generate_level(load_level('map.txt'))

        MapTile(groups['map_objects'], (145, 300), 'assets/map_tiles/Objects/camp/1.png')
        MapTile(groups['map_objects'], (10, 250), 'assets/map_tiles/Objects/camp/1.png', reverse=True)
        MapTile(groups['map_objects'], (10, 550), 'assets/map_tiles/Objects/camp/3.png', reverse=True)

        MapTile(groups['map_objects'], (175, 425), 'assets/map_tiles/Objects/decor/Log2.png')
        MapTile(groups['map_objects'], (75, 500), 'assets/map_tiles/Objects/decor/Log3.png')

        MapTile(groups['map_objects'], (15, 455), 'assets/map_tiles/Objects/decor/Box1.png')

        MapTile(groups['map_objects'], (40, 333), 'assets/map_tiles/Objects/decor/Box1.png')
        MapTile(groups['map_objects'], (13, 335), 'assets/map_tiles/Objects/decor/Box1.png')
        MapTile(groups['map_objects'], (26, 313), 'assets/map_tiles/Objects/decor/Box1.png')

        MapTile(groups['map_objects'], (221, 566), 'assets/map_tiles/Objects/fences/8.png', reverse=True)
        MapTile(groups['map_objects'], (191, 589), 'assets/map_tiles/Objects/fences/8.png', reverse=True)
        MapTile(groups['map_objects'], (161, 612), 'assets/map_tiles/Objects/fences/8.png', reverse=True)
        MapTile(groups['map_objects'], (0, 630), 'assets/map_tiles/Objects/fences/1.png')
        MapTile(groups['map_objects'], (54, 630), 'assets/map_tiles/Objects/fences/1.png')
        MapTile(groups['map_objects'], (108, 630), 'assets/map_tiles/Objects/fences/1.png')

        MapTile(groups['map_objects'], (0, 220), 'assets/map_tiles/Objects/fences/1.png')
        MapTile(groups['map_objects'], (54, 220), 'assets/map_tiles/Objects/fences/1.png')
        MapTile(groups['map_objects'], (108, 220), 'assets/map_tiles/Objects/fences/1.png')
        MapTile(groups['map_objects'], (161, 220), 'assets/map_tiles/Objects/fences/8.png')
        MapTile(groups['map_objects'], (191, 242), 'assets/map_tiles/Objects/fences/8.png')
        MapTile(groups['map_objects'], (221, 264), 'assets/map_tiles/Objects/fences/8.png')

        MapTile(groups['map_objects'], (540, 150), 'assets/map_tiles/Objects/shadows/5.png')
        MapTile(groups['map_objects'], (765, 150), 'assets/map_tiles/Objects/shadows/5.png')
        MapTile(groups['map_objects'], (990, 150), 'assets/map_tiles/Objects/shadows/5.png')
        MapTile(groups['map_objects'], (1215, 150), 'assets/map_tiles/Objects/shadows/5.png')

        MapTile(groups['map_objects'], (525, 55), 'assets/map_tiles/Objects/decor/Tree1.png')
        MapTile(groups['map_objects'], (750, 55), 'assets/map_tiles/Objects/decor/Tree1.png')
        MapTile(groups['map_objects'], (975, 55), 'assets/map_tiles/Objects/decor/Tree1.png')
        MapTile(groups['map_objects'], (1200, 55), 'assets/map_tiles/Objects/decor/Tree1.png')

        MapTile(groups['map_objects'], (440, 680), 'assets/map_tiles/Objects/pointers/1.png')
        MapTile(groups['map_objects'], (1350, 215), 'assets/map_tiles/Objects/pointers/4.png')

        MapTile(groups['map_objects'], (1142, 725), 'assets/map_tiles/Objects/bushes/1.png')
        MapTile(groups['map_objects'], (345, 113), 'assets/map_tiles/Objects/bushes/1.png')
        MapTile(groups['map_objects'], (1335, 35), 'assets/map_tiles/Objects/bushes/1.png')
        MapTile(groups['map_objects'], (180, 80), 'assets/map_tiles/Objects/bushes/2.png')
        MapTile(groups['map_objects'], (560, 670), 'assets/map_tiles/Objects/bushes/2.png')
        MapTile(groups['map_objects'], (615, 250), 'assets/map_tiles/Objects/bushes/2.png')
        MapTile(groups['map_objects'], (25, 115), 'assets/map_tiles/Objects/bushes/3.png')
        MapTile(groups['map_objects'], (1100, 740), 'assets/map_tiles/Objects/bushes/3.png')
        MapTile(groups['map_objects'], (415, 725), 'assets/map_tiles/Objects/bushes/3.png')
        MapTile(groups['map_objects'], (780, 735), 'assets/map_tiles/Objects/bushes/4.png')
        MapTile(groups['map_objects'], (425, 245), 'assets/map_tiles/Objects/bushes/4.png')
        MapTile(groups['map_objects'], (170, 670), 'assets/map_tiles/Objects/bushes/4.png', reverse=True)
        MapTile(groups['map_objects'], (75, 725), 'assets/map_tiles/Objects/bushes/5.png')
        MapTile(groups['map_objects'], (1400, 665), 'assets/map_tiles/Objects/bushes/5.png')
        MapTile(groups['map_objects'], (75, 45), 'assets/map_tiles/Objects/bushes/5.png')
        MapTile(groups['map_objects'], (1400, 150), 'assets/map_tiles/Objects/bushes/6.png')
        MapTile(groups['map_objects'], (610, 690), 'assets/map_tiles/Objects/bushes/6.png')
        MapTile(groups['map_objects'], (225, 145), 'assets/map_tiles/Objects/bushes/6.png')

        MapTile(groups['map_objects'], (250, 125), 'assets/map_tiles/Objects/stones/1.png')
        MapTile(groups['map_objects'], (165, 270), 'assets/map_tiles/Objects/stones/2.png')
        MapTile(groups['map_objects'], (65, 185), 'assets/map_tiles/Objects/stones/3.png')
        MapTile(groups['map_objects'], (250, 700), 'assets/map_tiles/Objects/stones/7.png')
        MapTile(groups['map_objects'], (15, 780), 'assets/map_tiles/Objects/stones/9.png')
        MapTile(groups['map_objects'], (1395, 85), 'assets/map_tiles/Objects/stones/10.png')
        MapTile(groups['map_objects'], (900, 685), 'assets/map_tiles/Objects/stones/11.png')
        MapTile(groups['map_objects'], (1365, 765), 'assets/map_tiles/Objects/stones/12.png')
        MapTile(groups['map_objects'], (135, 145), 'assets/map_tiles/Objects/stones/16.png')

        # Создаем анимированные объекты

        AnimatedMapObject(groups['animated_map_objects'], (70, 400),
                          ('assets/map_tiles/Animated_Objects/campfire/active_campfire/1.png',
                           'assets/map_tiles/Animated_Objects/campfire/active_campfire/2.png',
                           'assets/map_tiles/Animated_Objects/campfire/active_campfire/3.png',
                           'assets/map_tiles/Animated_Objects/campfire/active_campfire/4.png',
                           'assets/map_tiles/Animated_Objects/campfire/active_campfire/5.png',
                           'assets/map_tiles/Animated_Objects/campfire/active_campfire/6.png',))

        AnimatedMapObject(groups['animated_map_objects'], (245, 500),
                          ('assets/map_tiles/Animated_Objects/flag/1.png',
                           'assets/map_tiles/Animated_Objects/flag/2.png',
                           'assets/map_tiles/Animated_Objects/flag/3.png',
                           'assets/map_tiles/Animated_Objects/flag/4.png',
                           'assets/map_tiles/Animated_Objects/flag/5.png',
                           'assets/map_tiles/Animated_Objects/flag/6.png'), True)
        AnimatedMapObject(groups['animated_map_objects'], (245, 200),
                          ('assets/map_tiles/Animated_Objects/flag/1.png',
                           'assets/map_tiles/Animated_Objects/flag/2.png',
                           'assets/map_tiles/Animated_Objects/flag/3.png',
                           'assets/map_tiles/Animated_Objects/flag/4.png',
                           'assets/map_tiles/Animated_Objects/flag/5.png',
                           'assets/map_tiles/Animated_Objects/flag/6.png'), True)

        # Рисуем клетки
        for i in range(HEIGHT_CELL):
            for j in range(WIDTH_CELL):
                x = LEFT + j * CELL_SIZE
                y = TOP + i * CELL_SIZE
                MapTile(groups['map_tiles'], [x, y], 'assets/map_tiles/Tiles/FieldsTile_47.png')

        # Ставим конницу
        for i in range(1, WIDTH_CELL):
            Lancer((LEFT - CELL_SIZE / 2, i * CELL_SIZE + TOP - CELL_SIZE / 2), group_of_row=groups['rows'][i - 1])

        # Ставим юнитов в магазин
        units = [(Knight, shop_unit_coord[0], ANIMATIONS['KNIGHT'], 90, 45),
                 (Archer, shop_unit_coord[1], ANIMATIONS['ARCHER'], 50, 25),
                 (Wizard, shop_unit_coord[2], ANIMATIONS['WIZARD'], 85, 42),
                 (Priest, shop_unit_coord[3], ANIMATIONS['PRIEST'], 80, 40),
                 (ArmoredAxeman, shop_unit_coord[4], ANIMATIONS['ARMORED_AXEMAN'], 70, 35),
                 (SwordsMan, shop_unit_coord[5], ANIMATIONS['SWORDSMAN'], 80, 40),
                 (KnightTemplar, shop_unit_coord[6], ANIMATIONS['KNIGHT_TEMPLAR'], 100, 40)]

        for unit, coord, anim, price, sale in units:
            Shop(unit, coord, anim, board,
                 price=price, sale=sale)


class MapTile(pygame.sprite.Sprite):
    def __init__(self, group, coord, image, reverse=False):
        super().__init__(group, groups['all_sprites'])
        self.image = load_image(file=image, reverse=reverse)
        self.rect = self.image.get_rect()
        self.rect.x = coord[0]
        self.rect.y = coord[1]


class AnimatedMapObject(pygame.sprite.Sprite):
    def __init__(self, group, coord, images, reverse=False):
        super().__init__(group, groups['all_sprites'])
        self.image = load_image(images[0])
        self.frames = [load_image(file=image, reverse=reverse) for image in images]
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
            self.frame = (self.frame + 1) % len(self.frames)
            self.image = self.frames[self.frame]
