import sys

import pygame.sprite

from constant import FPS, HEIGHT, WIDTH, CELL_SIZE
from sprite_groups import *

from Board_class import Board
from Map_constructor import Map_constructor, Map_tile

from sound_tests import play_sound

from Units import *

pygame.init()

size = WIDTH, HEIGHT
screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()

font = pygame.font.Font('assets/pi-sheng.regular.otf', 64)
texts = []


def terminate():
    pygame.quit()
    sys.exit()


class Button(pygame.sprite.Sprite):
    button_images = {'settings': 'assets/buttons/settings_btn.png',
                     'pause': 'assets/buttons/pause_btn.png',
                     'return': 'assets/buttons/return_btn.png',
                     'sketch': 'assets/buttons/sketch_btn.png'}

    def __init__(self, x, y, type_btn, command, text=None, group=None):
        if not group:
            group = buttons
        super().__init__(group)
        self.image = load_image(self.button_images[type_btn])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.command = command
        if text:
            texts.append([font.render(text, True, 'black'),  (x + 30, y + 15)])

    def update(self, *args, **kwargs):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
            map_tiles.empty()
            map_objects.empty()
            animated_map_objects.empty()
            buttons.empty()
            level_doors.empty()
            texts.clear()

            play_sound('button_click')

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
            if self.command == 'open_characters_page':
                print('<_page was successfully changed_>')
                dictionary_screen(0)
            if self.command == 'open_mobs_page':
                print('<_page was successfully changed_>')
                dictionary_screen(1)
            if self.command == 'show_soldier':
                dictionary_screen(0)
            if self.command == 'show_knight':
                dictionary_screen(0)


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
    background = load_image('assets/backgrounds/main_background.png')
    pygame.display.set_icon(load_image('assets/icon.png'))

    Button(900, 300, 'sketch', 'open_pick_level_screen', 'Continue')
    Button(900, 425, 'sketch', 'open_dictionary_screen', 'Dictionary')
    Button(900, 550, 'sketch', 'open_options_screen', 'Options')
    Button(900, 675, 'sketch', 'quit', 'Quit')

    pygame.display.set_caption('Главное Лобби')

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                buttons.update(event)

        screen.blit(background, (0, 0))
        buttons.draw(screen)
        for txt in texts:
            screen.blit(txt[0], txt[1])

        pygame.display.flip()
        clock.tick(FPS)


def dictionary_screen(page=0):
    def characters_dictionary():
        characters_page.draw(screen)

    def mobs_dictionary():
        mobs_page.draw(screen)

    pygame.display.set_caption('Бестиарий')
    background = load_image('assets/backgrounds/levels_background.png')

    Button(1300, 650, 'return', 'open_main_lobby')
    Button(300, 60, 'sketch', 'open_characters_page', 'Characters')
    Button(800, 60, 'sketch', 'open_mobs_page', 'Mobs')

    Button(570, 200, 'sketch', 'show_soldier', 'Soldier', characters_page)
    Button(570, 320, 'sketch', 'show_knight', 'Knight', characters_page)
    Button(570, 440, 'sketch', 'show_archer', 'Archer', characters_page)
    Button(570, 560, 'sketch', 'show_lancer', 'Lancer', characters_page)

    dictionary_field = load_image('assets/dictionary_field.png')

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    buttons.update(event)

        screen.blit(background, (0, 0))
        buttons.draw(screen)

        screen.blit(dictionary_field, (175, 200))

        if not page:
            characters_dictionary()
        else:
            mobs_dictionary()
        for txt in texts:
            screen.blit(txt[0], txt[1])

        pygame.display.flip()


def options_screen():
    pygame.display.set_caption('Настройки')

    Button(1300, 650, 'return', 'open_main_lobby')

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
    background = load_image('assets/backgrounds/levels_background.png')

    pygame.display.set_caption('Выбор уровня')

    Level_door(174, 120, False)
    Level_door(606, 120)
    Level_door(1038, 120)
    Level_door(375, 470)
    Level_door(825, 470)

    text_level1 = font.render('Level 1', True, 'black')
    text_level2 = font.render('Level 2', True, 'black')
    text_level3 = font.render('Level 3', True, 'black')
    text_level4 = font.render('Level 4', True, 'black')
    text_level5 = font.render('Level 5', True, 'black')

    Button(1200, 500, 'return', 'open_main_lobby')

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
                            play_sound('open_door', 1)
                            game_screen()
                    buttons.update(event)

        screen.blit(background, (0, 0))

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
    Map_constructor(WIDTH, HEIGHT, board)
    board.render('assets/map_tiles/Tiles/FieldsTile_47.png')

    Button(1350, 10, 'return', 'open_pick_level_screen')

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
