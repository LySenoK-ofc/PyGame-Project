import sys

import pygame.sprite

from load_image_func import load_image
from constant import FPS, HEIGHT, WIDTH, CELL_SIZE
from sprite_groups import *

from Board_class import Board
from Map_constructor import generate_level, load_level, Map_constructor, Map_tile

from Units import *

pygame.init()

size = WIDTH, HEIGHT
screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()

font = pygame.font.Font('assets/pi-sheng.regular.otf', 64)


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
            if self.command == 'open_characters_page':
                print('<_page was successfully changed_>')
                dictionary_screen(0)
            if self.command == 'open_mobs_page':
                print('<_page was successfully changed_>')
                dictionary_screen(1)
            if self.command == 'show_soldier':
                pass
            if self.command == 'show_knight':
                pass


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


def dictionary_screen(page=0):
    def characters_dictionary():
        soldier_btn = Button(570, 200, 'sketch', 'show_soldier')
        knight_btn = Button(570, 320, 'sketch', 'show_knight')
        archer_btn = Button(570, 440, 'sketch', 'show_archer')
        lancer_btn = Button(570, 560, 'sketch', 'show_lancer')

        text_soldier_btn = font.render('Soldier', True, 'black')
        text_knight_btn = font.render('Knight', True, 'black')
        text_archer_btn = font.render('Archer', True, 'black')
        text_lancer_btn = font.render('Lancer', True, 'black')

        screen.blit(text_soldier_btn, (600, 220))
        screen.blit(text_knight_btn, (600, 340))
        screen.blit(text_archer_btn, (600, 460))
        screen.blit(text_lancer_btn, (600, 580))

    def mobs_dictionary():
        pass

    pygame.display.set_caption('Бестиарий')
    background = load_image('assets/backgrounds/levels_background.png')

    return_btn = Button(1300, 650, 'return', 'open_main_lobby')
    change_page_btn1 = Button(300, 60, 'sketch', 'open_characters_page')
    change_page_btn2 = Button(800, 60, 'sketch', 'open_mobs_page')

    text_change_page_btn1 = font.render('Characters', True, 'black')
    text_change_page_btn2 = font.render('Mobs', True, 'black')

    for i in range(5):
        for j in range(6):
            Map_tile(map_tiles, (i * 75 + 182, j * 75 + 207), 'assets/map_tiles/Tiles/FieldsTile_38.png')
            if i == 2 and j == 3:
                Map_tile(map_tiles, (i * 75 + 182, j * 75 + 207), 'assets/map_tiles/Tiles/FieldsTile_20.png')
            elif i == 1 and j == 2:
                Map_tile(map_tiles, (i * 75 + 182, j * 75 + 207), 'assets/map_tiles/Tiles/FieldsTile_10.png')
            elif i == 3 and j == 2:
                Map_tile(map_tiles, (i * 75 + 182, j * 75 + 207), 'assets/map_tiles/Tiles/FieldsTile_12.png')
            elif i == 1 and j == 4:
                Map_tile(map_tiles, (i * 75 + 182, j * 75 + 207), 'assets/map_tiles/Tiles/FieldsTile_26.png')
            elif i == 3 and j == 4:
                Map_tile(map_tiles, (i * 75 + 182, j * 75 + 207), 'assets/map_tiles/Tiles/FieldsTile_28.png')
            elif i == 1 and j == 3:
                Map_tile(map_tiles, (i * 75 + 182, j * 75 + 207), 'assets/map_tiles/Tiles/FieldsTile_13.png')
            elif i == 3 and j == 3:
                Map_tile(map_tiles, (i * 75 + 182, j * 75 + 207), 'assets/map_tiles/Tiles/FieldsTile_09.png')
            elif i == 2 and j == 4:
                Map_tile(map_tiles, (i * 75 + 182, j * 75 + 207), 'assets/map_tiles/Tiles/FieldsTile_03.png')
            elif i == 2 and j == 2:
                Map_tile(map_tiles, (i * 75 + 182, j * 75 + 207), 'assets/map_tiles/Tiles/FieldsTile_34.png')

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    buttons.update(event)

        screen.blit(background, (0, 0))
        buttons.draw(screen)
        screen.blit(text_change_page_btn1, (325, 75))
        screen.blit(text_change_page_btn2, (885, 75))

        pygame.draw.rect(screen, 'black', (175, 200, 389, 464), 7)
        map_tiles.draw(screen)

        if page == 0:
            characters_dictionary()
        else:
            mobs_dictionary()

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
