import sys

import pygame.sprite

import Game
from load_image_func import load_image
from sounds_manager import play_background_music
from sprite_groups import update_group
from animated_objects import AnimatedMapObject
from Units import *
from Mobs import *

from constant import FPS, WIDTH, HEIGHT
import pygame.freetype

pygame.init()

size = WIDTH, HEIGHT
screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()

font = pygame.font.Font('assets/data/font/pi-sheng.regular.otf', 64)
font2 = pygame.font.Font('assets/data/font/Adbnorm.ttf', 32)


def terminate():
    pygame.quit()
    sys.exit()


class View_entity(pygame.sprite.Sprite):
    def __init__(self, coord, animations, type_entity, frame_rate, group):
        super().__init__(group)
        self.animations = animations
        self.mode = 'idle'
        self.frames = self.animations[self.mode]
        self.frame = 0
        self.image = self.frames[self.frame]
        self.rect = self.image.get_rect(center=coord)
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = frame_rate
        self.type_entity = type_entity

    def update(self, *args, **kwargs):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate and self.type_entity == 'view':
            self.last_update = now
            self.frame = (self.frame + 1) % len(self.frames)
            self.image = self.frames[self.frame]


class Button(pygame.sprite.Sprite):
    button_images = {'settings': 'assets/buttons/settings_btn.png',
                     'pause': 'assets/buttons/pause_btn.png',
                     'return': 'assets/buttons/return_btn.png',
                     'replay': 'assets/buttons/replay_btn.png',
                     'continue': 'assets/buttons/continue_btn.png',
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
            update_group()
            Sketch_button.texts.clear()
            play_sound(sounds['button_click'])
            if not pygame.mixer.music.get_busy():
                play_background_music('assets/sounds/background_sounds/lobby/lobby_sound.mp3')

            if self.command == 'open_pick_level_screen':
                pick_level_screen()
                rulers_screen()
                terminate()
            if self.command == 'open_main_lobby':
                main_lobby()
            if self.command == 'quit':
                terminate()
            if self.command == 'open_dictionary_screen':
                dictionary_screen(0)
            if self.command == 'open_options_screen':
                options_screen()
            if self.command == 'open_characters_page':
                dictionary_screen(0, entity='Knight')
            if self.command == 'open_mobs_page':
                dictionary_screen(1, entity='Orc')
            if self.command == 'replay':
                Game.game_loop()
            if self.command == 'next_level':
                Game.game_loop()


class Sketch_button(Button):
    texts = []

    def __init__(self, x, y, command, text=None, group=groups['buttons']):
        super().__init__(x, y, 'sketch', command, group)
        self.texts.append([font.render(text, True, 'black'), (x + 30, y + 15)])


class Entity_view_button(Button):
    characters_view = pygame.sprite.Group()
    mobs_view = pygame.sprite.Group()

    def __init__(self, x, y, entity=None, entity_type=None, group=groups['buttons']):
        super().__init__(x, y, 'entity_view', None, group)
        self.entity = entity
        self.entity_type = entity_type
        if self.entity_type == 'Unit':
            View_entity((x + 50, y + 50), ANIMATIONS[entity.upper()], None, 250, self.characters_view)
        else:
            View_entity((x + 57, y + 50), ANIMATIONS[entity.upper()], None, 250, self.mobs_view)

    def update(self, *args, **kwargs):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
            groups['buttons'].empty()
            Sketch_button.texts.clear()
            play_sound(sounds['button_click'], 0.2)
            if self.entity_type == 'Unit':
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
        self.click = 0
        if lock:
            self.lock = Door_lock(x + 110, y + 150)
        else:
            self.lock = None

    def update(self, *args, **kwargs):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
            if self.lock:
                play_sound(sounds['door_close'], 1)
            else:
                self.image = load_image('assets/doors/open_door.png')
                self.click += 1
                if self.click == 1:
                    play_sound(sounds['open_door'], 1)
                if self.check():
                    groups['buttons'].empty()

    def check(self):
        if self.click >= 2:
            return True
        return False


def main_lobby(restart_music=False):
    background = load_image('assets/backgrounds/main_background.png')
    pygame.display.set_icon(load_image('assets/icon.png'))

    if restart_music:
        play_background_music('assets/sounds/background_sounds/lobby/lobby_sound.mp3')

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


def dictionary_screen(page=0, entity='Knight'):
    pygame.display.set_caption('Бестиарий')
    background = load_image('assets/backgrounds/levels_background.png')

    Entity_view_button.characters_view.empty()
    Entity_view_button.mobs_view.empty()

    Button(1300, 650, 'return', 'open_main_lobby')
    Sketch_button(300, 60, 'open_characters_page', 'Characters')
    Sketch_button(800, 60, 'open_mobs_page', 'Mobs')

    Entity_view_button(600, 200, 'Knight', 'Unit', groups['characters_page'])
    Entity_view_button(600, 320, 'Archer', 'Unit', groups['characters_page'])
    Entity_view_button(600, 440, 'Wizard', 'Unit', groups['characters_page'])
    Entity_view_button(600, 560, 'Armored_Axeman', 'Unit', groups['characters_page'])
    Entity_view_button(740, 200, 'SwordsMan', 'Unit', groups['characters_page'])
    Entity_view_button(740, 320, 'Priest', 'Unit', groups['characters_page'])
    Entity_view_button(740, 440, 'Knight_Templar', 'Unit', groups['characters_page'])
    Entity_view_button(740, 560, 'Lancer', 'Unit', groups['characters_page'])

    Entity_view_button(970, 200, 'Orc', 'Mob', groups['mobs_page'])
    Entity_view_button(970, 320, 'Armored_Orc', 'Mob', groups['mobs_page'])
    Entity_view_button(970, 440, 'Elite_Orc', 'Mob', groups['mobs_page'])
    Entity_view_button(970, 560, 'Skeleton', 'Mob', groups['mobs_page'])
    Entity_view_button(1100, 200, 'Armored_Skeleton', 'Mob', groups['mobs_page'])
    Entity_view_button(1100, 320, 'Greatsword_Skeleton', 'Mob', groups['mobs_page'])
    Entity_view_button(1100, 440, 'Slime', 'Mob', groups['mobs_page'])
    Entity_view_button(1100, 560, 'Werewolf', 'Mob', groups['mobs_page'])
    Entity_view_button(1230, 200, 'Werebear', 'Mob', groups['mobs_page'])
    Entity_view_button(1230, 320, 'Rider_Orc', 'Mob', groups['mobs_page'])

    if page:
        groups['characters_page'].empty()
    else:
        groups['mobs_page'].empty()

    dictionary_field = load_image('assets/other_textures/dictionary_field.png')
    current_entity = pygame.sprite.Group()
    entity = View_entity((375, 450), ANIMATIONS[entity.upper()], 'view', 250, current_entity)

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
                        if type(door) == Level_door:
                            if door.check():
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


def rulers_screen():
    pygame.display.set_caption('Правила')
    rulers_map = load_image('assets/other_textures/rulers_screen_map.png')
    dialog = load_image('assets/other_textures/dialog.png')

    AnimatedMapObject((600, 300), 'BIG_CAMP_FIRE')

    continue_text = font2.render('Нажмите ПРОБЕЛ, чтобы продолжить', True, 'white')
    rulers_text = (('Приветствую! Ваша задча - защитить этот лагерь',
                    'от монстров, для этого вам было выделено войско.',
                    'Но помните - никто не работает за бесплатно,',
                    'поэтому для усиления боевой мощи вам придется',
                    ' зарабатывать деньги, убивая врагов.'),
                   ('На ваш счет сразу будет начислен стартовый',
                    'капитал, а также на поле битвы будут находиться',
                    '5 всадников, способных спасти вас в критической',
                    'ситуации. Желаю удачи!'),
                   ('<Помощь в управлении>',
                    'Для размещения воина на поле боя, необходимо',
                    'перетащить его из магазина на место, куда вы',
                    'хотите его разместить. При зажатой клавише SHIFT',
                    'вы можете узнать информацию о воине(здровье',
                    'броню и урон, если он находиться на поле боя,'),
                   ('стоимость размещения и продажи - если в магазине).',
                    'ПКМ, чтобы продать воина. Также в игре присут-',
                    'ствует возможность быстрого размещения войска,',
                    'для этого небходимо зажать цифру на ',
                    'клавиатуре и кликнуть по нужной клетке',
                    '(1-Лучник, 2-Рыцарь, 3-Маг, 4-Жрица,',
                    '5-Дровосек, 6-Мастер Меча, 7-Королевский страж)'))
    dialog_page = 0

    Dialog_Knight()
    play_sound(sounds['mumble'])

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    if dialog_page + 1 == len(rulers_text):
                        return
                    else:
                        dialog_page += 1
                        if not pygame.mixer.Channel(1).get_busy():
                            pygame.mixer.Channel(1).play(sounds['mumble'])
                if keys[pygame.K_LEFT]:
                    if dialog_page > 0:
                        dialog_page -= 1

        screen.fill('black')
        screen.blit(rulers_map, (0, 0))
        groups['map_tiles'].draw(screen)
        groups['map_objects'].draw(screen)
        groups['animated_map_objects'].draw(screen)
        groups['animated_map_objects'].update()
        groups['shop_units'].draw(screen)
        groups['shop_units'].update()

        screen.blit(dialog, (240, 400))
        screen.blit(continue_text, (385, 20))
        for i in range(len(rulers_text[dialog_page])):
            screen.blit(font2.render(rulers_text[dialog_page][i], True, 'black'), (410, 540 + i * 30))

        pygame.display.flip()
        clock.tick(FPS)


def pause_screen():
    def unpause_music():
        pygame.mixer.music.unpause()
        pygame.mixer.unpause()
        pygame.display.set_caption('Игра')

    pygame.display.set_caption('Пауза')
    pygame.mixer.music.pause()
    pygame.mixer.pause()
    menu = load_image('assets/other_textures/game_menu.png')
    close_btn_coord = ((1110, 115), (1170, 180))

    Button(420, 275, 'replay', 'replay')
    Button(420, 425, 'return', 'open_pick_level_screen')

    Sketch_button(550, 280, 'replay', 'Replay')
    Sketch_button(550, 440, 'open_pick_level_screen', 'Back to lobby')

    pause_text = load_image('assets/other_textures/pause.png')

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]:
                    unpause_music()
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = event.pos
                    if close_btn_coord[0][0] < pos[0] < close_btn_coord[1][0] \
                            and close_btn_coord[0][1] < pos[1] < close_btn_coord[1][1]:
                        unpause_music()
                        play_sound(sounds['button_click'])
                        return
                    groups['buttons'].update(event)
        groups['all_sprites'].draw(screen)
        screen.blit(menu, (284, 97))
        screen.blit(pause_text, (537, 115))
        groups['buttons'].draw(screen)
        for txt in Sketch_button.texts:
            screen.blit(txt[0], txt[1])
        pygame.display.flip()
        clock.tick(FPS)


def win_screen(lvl=None):
    pygame.mixer.music.stop()
    pygame.mixer.stop()
    pygame.display.set_caption('Победа!')

    menu = load_image('assets/other_textures/game_menu.png')
    victory_text = load_image('assets/other_textures/victory.png')
    close_btn_coord = ((1110, 115), (1170, 180))

    Button(420, 275, 'replay', 'replay')
    Button(420, 425, 'return', 'open_pick_level_screen')
    Button(420, 575, 'continue', 'next_level')

    Sketch_button(550, 280, 'replay', 'Replay')
    Sketch_button(550, 440, 'open_main_lobby', 'Back to lobby')
    Sketch_button(550, 600, 'next_level', 'Next level')

    play_sound(sounds['game_win'])

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]:
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = event.pos
                    if close_btn_coord[0][0] < pos[0] < close_btn_coord[1][0] \
                            and close_btn_coord[0][1] < pos[1] < close_btn_coord[1][1]:
                        play_sound('button_click')
                        play_background_music('assets/sounds/background_sounds/lobby/lobby_sound.mp3')
                        groups['buttons'].empty()
                        pick_level_screen()
                    groups['buttons'].update(event)
        groups['all_sprites'].draw(screen)
        screen.blit(menu, (284, 97))
        screen.blit(victory_text, (549, 100))
        groups['buttons'].draw(screen)
        for txt in Sketch_button.texts:
            screen.blit(txt[0], txt[1])
        pygame.display.flip()
        clock.tick(FPS)


def lose_screen():
    pygame.mixer.music.stop()
    pygame.mixer.stop()
    pygame.display.set_caption('Поражение...')

    menu = load_image('assets/other_textures/game_menu.png')
    defeat_text = load_image('assets/other_textures/defeat.png')
    close_btn_coord = ((1110, 115), (1170, 180))

    Button(420, 275, 'replay', 'replay')
    Button(420, 425, 'return', 'open_pick_level_screen')

    Sketch_button(550, 280, 'replay', 'Replay')
    Sketch_button(550, 440, 'open_main_lobby', 'Back to lobby')

    play_sound(sounds['game_lose'])

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]:
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = event.pos
                    if close_btn_coord[0][0] < pos[0] < close_btn_coord[1][0] \
                            and close_btn_coord[0][1] < pos[1] < close_btn_coord[1][1]:
                        play_sound('button_click')
                        play_background_music('assets/sounds/background_sounds/lobby/lobby_sound.mp3')
                        groups['buttons'].empty()
                        pick_level_screen()
                    groups['buttons'].update(event)
        groups['all_sprites'].draw(screen)
        screen.blit(menu, (284, 97))
        screen.blit(defeat_text, (549, 100))
        groups['buttons'].draw(screen)
        for txt in Sketch_button.texts:
            screen.blit(txt[0], txt[1])
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    play_background_music('assets/sounds/background_sounds/lobby/lobby_sound.mp3')
    main_lobby()
