import sys

import pygame.sprite

from load_image_func import load_image
from constant import FPS, HEIGHT, WIDTH, CELL_SIZE
from sprite_groups import *

from Board_class import Board
from Map_constructor import generate_level, load_level, Map_constructor

pygame.init()

size = WIDTH, HEIGHT
screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()


def terminate():
    pygame.quit()
    sys.exit()


class Button(pygame.sprite.Sprite):
    button_images = {'settings': 'assets/buttons/settings_btn.png',
                     'pause': 'assets/buttons/pause_btn.png',
                     'return': 'assets/buttons/return_btn.png',
                     'sketch': 'assets/buttons/sketch_btn.png'}

    def __init__(self, x, y, type_btn, command):
        super().__init__(buttons)
        self.image = load_image(self.button_images[type_btn])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.command = command

    def update(self, *args, **kwargs):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
            map_tiles.empty()
            map_objects.empty()
            animated_map_objects.empty()
            buttons.empty()
            level_doors.empty()
            if self.command == 'open_pick_level_screen':
                pick_level_screen()
            if self.command == 'open_main_lobby':
                main_lobby()
            if self.command == 'quit':
                terminate()
            if self.command == 'open_dictionary_screen':
                dictionary_screen()
            if self.command == 'open_options_screen':
                options_screen()


class Door_lock(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(level_doors)
        self.image = load_image('assets/doors/lock.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Level_door(pygame.sprite.Sprite):
    def __init__(self, x, y, lock=True):
        super().__init__(level_doors)
        self.image = load_image('assets/doors/close_door.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.lock = lock
        self.open = False
        if lock:
            self.lock = Door_lock(x + 110, y + 150)

    def update(self, *args, **kwargs):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos) and not self.lock:
            self.image = load_image('assets/doors/open_door.png')
            self.open = True

    def check(self):
        if self.open:
            return True
        return False


def main_lobby():
    font = pygame.font.Font('assets/pi-sheng.regular.otf', 64)
    background = load_image('assets/backgrounds/main_background.png')

    start_game_btn = Button(900, 300, 'sketch', 'open_pick_level_screen')
    dictionary_btn = Button(900, 425, 'sketch', 'open_dictionary_screen')
    options_btn = Button(900, 550, 'sketch', 'open_options_screen')
    quit_btn = Button(900, 675, 'sketch', 'quit')

    start_game_text = font.render('Continue', True, 'black')
    dictionary_text = font.render('Dictionary', True, 'black')
    options_text = font.render('Options', True, 'black')
    quit_text = font.render('Quit', True, 'black')

    pygame.display.set_caption('Главное Лобби')

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                buttons.update(event)

        screen.blit(background, (0, 0))
        buttons.draw(screen)
        screen.blit(start_game_text, (930, 315))
        screen.blit(dictionary_text, (930, 440))
        screen.blit(options_text, (930, 565))
        screen.blit(quit_text, (930, 690))

        pygame.display.flip()
        clock.tick(FPS)


def dictionary_screen():
    pygame.display.set_caption('Бестинарий')

    return_btn = Button(1300, 650, 'return', 'open_main_lobby')

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    buttons.update(event)
        screen.fill('black')
        buttons.draw(screen)

        pygame.display.flip()


def options_screen():
    pygame.display.set_caption('Бестинарий')

    return_btn = Button(1300, 650, 'return', 'open_main_lobby')

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    buttons.update(event)
        screen.fill('black')
        buttons.draw(screen)

        pygame.display.flip()


def pick_level_screen():
    font = pygame.font.Font('assets/pi-sheng.regular.otf', 64)
    background = load_image('assets/backgrounds/levels_background.png')

    pygame.display.set_caption('Выбор уровня')

    door1 = Level_door(174, 120, False)
    door2 = Level_door(606, 120)
    door3 = Level_door(1038, 120)
    door4 = Level_door(375, 470)
    door5 = Level_door(825, 470)

    text_level1 = font.render('Level 1', False, 'black')
    text_level2 = font.render('Level 2', True, 'black')
    text_level3 = font.render('Level 3', True, 'black')
    text_level4 = font.render('Level 4', True, 'black')
    text_level5 = font.render('Level 5', True, 'black')

    return_btn = Button(1200, 500, 'return', 'open_main_lobby')

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    level_doors.update(event)
                    for door in level_doors:
                        if type(door) == Level_door and door.check():
                            buttons.empty()
                            game_screen()
                    buttons.update(event)

        screen.blit(background, (0, 3))

        level_doors.draw(screen)
        buttons.draw(screen)

        screen.blit(text_level1, (220, 60))
        screen.blit(text_level2, (650, 60))
        screen.blit(text_level3, (1100, 60))
        screen.blit(text_level4, (420, 415))
        screen.blit(text_level5, (870, 415))

        pygame.display.flip()
        clock.tick(FPS)


def game_screen():
    board = Board(6, 5, (75 * 6), (75 * 4), CELL_SIZE)

    generate_level(load_level('map.txt'))
    Map_constructor(WIDTH, HEIGHT, board)
    board.render('assets/map_tiles/Tiles/FieldsTile_47.png')

    return_btn = Button(1350, 10, 'return', 'open_pick_level_screen')

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    buttons.update(event)
        map_tiles.draw(screen)
        map_objects.draw(screen)
        animated_map_objects.update()
        animated_map_objects.draw(screen)
        buttons.draw(screen)
        pygame.display.flip()

        print(map_tiles, map_objects, animated_map_objects)
        clock.tick(FPS)
