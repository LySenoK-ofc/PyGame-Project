import sys

import pygame.sprite

import demo_project
from load_image_func import load_image
from constant import FPS
from sound_tests import play_sound
from sprite_groups import update_group

from Units import *
from Mobs import *

pygame.init()

size = WIDTH, HEIGHT
screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()

font = pygame.font.Font('assets/pi-sheng.regular.otf', 64)


def terminate():
    pygame.quit()
    sys.exit()


def get_class(class_name):
    return getattr(sys.modules[__name__], class_name)


class Button(pygame.sprite.Sprite):
    button_images = {'settings': 'assets/buttons/settings_btn.png',
                     'pause': 'assets/buttons/pause_btn.png',
                     'return': 'assets/buttons/return_btn.png',
                     'sketch': 'assets/buttons/sketch_btn.png',
                     'entity_view': 'assets/buttons/entity_view_btn.png'}

    def __init__(self, x, y, type_btn, command, group=groups['buttons']):
        super().__init__(group)
        self.image = load_image(self.button_images[type_btn])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.command = command

    def update(self, *args, **kwargs):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
            groups['map_tiles'].empty()
            groups['map_objects'].empty()
            groups['animated_map_objects'].empty()
            groups['buttons'].empty()
            groups['level_doors'].empty()
            Sketch_button.texts.clear()
            groups['characters_page'].empty()
            groups['mobs_page'].empty()

            play_sound('button_click')

            if self.command == 'open_pick_level_screen':
                pick_level_screen()
                update_group()  # Временно
                pygame.display.set_caption('Уровень *')
                demo_project.game_loop()  # Временно
            if self.command == 'open_main_lobby':
                main_lobby()
            if self.command == 'quit':
                terminate()
            if self.command == 'open_dictionary_screen':
                dictionary_screen(0)
            if self.command == 'open_options_screen':
                options_screen()
            if self.command == 'open_characters_page':
                print('<_page was successfully changed_>')
                dictionary_screen(0)
            if self.command == 'open_mobs_page':
                print('<_page was successfully changed_>')
                dictionary_screen(1)


class Sketch_button(Button):
    texts = []

    def __init__(self, x, y, command, text=None, group=groups['buttons']):
        super().__init__(x, y, 'sketch', command, group)
        self.texts.append([font.render(text, True, 'black'), (x + 30, y + 15)])


class Entity_view_button(Button):
    characters_view = pygame.sprite.Group()
    mobs_view = pygame.sprite.Group()

    def __init__(self, x, y, entity=None, group=groups['buttons']):
        super().__init__(x, y, 'entity_view', None, group)
        self.entity = get_class(entity)
        if self.entity.__bases__[0] == Unit:
            self.characters_view.add(self.entity((x + 50, y + 50), groups['rows'][0]))
            self.type = 'Unit'
        else:
            self.mobs_view.add(self.entity((x + 57, y + 50), groups['rows'][1]))
            self.type = 'Mob'

    def update(self, *args, **kwargs):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
            play_sound('button_click', 0.2)
            if self.type == 'Unit':
                dictionary_screen(0, self.entity)
            else:
                dictionary_screen(1, self.entity)


class Door_lock(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(groups['level_doors'])
        self.image = load_image('assets/doors/lock.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Level_door(pygame.sprite.Sprite):
    def __init__(self, x, y, lock=True):
        super().__init__(groups['level_doors'])
        self.image = load_image('assets/doors/close_door.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.open = False
        if lock:
            self.lock = Door_lock(x + 110, y + 150)
        else:
            self.lock = None

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

    Sketch_button(900, 300, 'open_pick_level_screen', 'Continue')
    Sketch_button(900, 425, 'open_dictionary_screen', 'Dictionary')
    Sketch_button(900, 550, 'open_options_screen', 'Options')
    Sketch_button(900, 675, 'quit', 'Quit')

    pygame.display.set_caption('Главное Лобби')

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                groups['buttons'].update(event)

        screen.blit(background, (0, 0))
        groups['buttons'].draw(screen)
        for txt in Sketch_button.texts:
            screen.blit(txt[0], txt[1])

        pygame.display.flip()
        clock.tick(FPS)


def dictionary_screen(page=0, entity=get_class('Knight')):
    pygame.display.set_caption('Бестиарий')
    background = load_image('assets/backgrounds/levels_background.png')

    Entity_view_button.characters_view.empty()
    Entity_view_button.mobs_view.empty()

    Button(1300, 650, 'return', 'open_main_lobby')
    Sketch_button(300, 60, 'open_characters_page', 'Characters')
    Sketch_button(800, 60, 'open_mobs_page', 'Mobs')

    Entity_view_button(600, 200, 'Knight', groups['characters_page'])
    Entity_view_button(600, 320, 'Archer', groups['characters_page'])
    Entity_view_button(600, 440, 'Wizard', groups['characters_page'])
    Entity_view_button(600, 560, 'ArmoredAxeman', groups['characters_page'])
    Entity_view_button(740, 200, 'SwordsMan', groups['characters_page'])
    Entity_view_button(740, 320, 'Priest', groups['characters_page'])
    Entity_view_button(740, 440, 'KnightTemplar', groups['characters_page'])
    Entity_view_button(740, 560, 'Lancer', groups['characters_page'])

    Entity_view_button(970, 200, 'Orc', groups['mobs_page'])
    Entity_view_button(970, 320, 'ArmoredOrc', groups['mobs_page'])
    Entity_view_button(970, 440, 'EliteOrc', groups['mobs_page'])
    Entity_view_button(970, 560, 'Skeleton', groups['mobs_page'])
    Entity_view_button(1100, 200, 'ArmoredSkeleton', groups['mobs_page'])
    Entity_view_button(1100, 320, 'GreateswordSkeleton', groups['mobs_page'])
    Entity_view_button(1100, 440, 'Slime', groups['mobs_page'])
    Entity_view_button(1100, 560, 'Werewolf', groups['mobs_page'])
    Entity_view_button(1230, 200, 'Werebear', groups['mobs_page'])
    Entity_view_button(1230, 320, 'RiderOrc', groups['mobs_page'])

    dictionary_field = load_image('assets/dictionary_field.png')
    current_entity = pygame.sprite.Group()
    current_entity.add(entity((375, 450), groups['rows'][2]))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    groups['buttons'].update(event)
                    groups['characters_page'].update(event)
                    groups['mobs_page'].update(event)

        screen.blit(background, (0, 0))
        groups['buttons'].draw(screen)

        screen.blit(dictionary_field, (175, 200))

        if page:
            groups['mobs_page'].draw(screen)
            Entity_view_button.mobs_view.draw(screen)
            pygame.draw.rect(screen, 'black', pygame.Rect(
                590, 200, 370, 470), 0, 35)
        else:
            groups['characters_page'].draw(screen)
            Entity_view_button.characters_view.draw(screen)
            pygame.draw.rect(screen, 'black', pygame.Rect(
                870, 200, 420, 470), 0, 35)

        for txt in Sketch_button.texts:
            screen.blit(txt[0], txt[1])

        current_entity.update()
        current_entity.draw(screen)

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
                    groups['buttons'].update(event)
        screen.fill('black')
        groups['buttons'].draw(screen)

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
                    groups['level_doors'].update(event)
                    for door in groups['level_doors']:
                        if type(door) == Level_door and door.check():
                            groups['buttons'].empty()
                            play_sound('open_door', 1)
                            return
                    groups['buttons'].update(event)

        screen.blit(background, (0, 0))

        groups['level_doors'].draw(screen)
        groups['buttons'].draw(screen)

        screen.blit(text_level1, (220, 60))
        screen.blit(text_level2, (650, 60))
        screen.blit(text_level3, (1100, 60))
        screen.blit(text_level4, (420, 415))
        screen.blit(text_level5, (870, 415))

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    main_lobby()
