from random import choice

import constant
import game_dynamic_parameters
import save_statistics
import screens
import pytmx

from animated_objects import AnimatedMapObject
from Mobs import Slime, Skeleton, Orc, ArmoredOrc, EliteOrc, RiderOrc, ArmoredSkeleton, GreateswordSkeleton, Werewolf, \
    Werebear
from Units import Archer, Knight, Wizard, Priest, ArmoredAxeman, SwordsMan, KnightTemplar, Lancer
from Waves_manager import WaveManager
from constant import FPS, WIDTH, HEIGHT, CELL_SIZE
from Board import Board
from map_creator import draw_map, get_objects
from sale_func import sale_unit
from shop_units import Shop
from show_unit_info import show_info
from sounds_manager import play_background_music, play_sound, sounds
from sprite_groups import groups, update_group
import pygame
import pygame.freetype
from all_animations import ANIMATIONS

pygame.init()
size = WIDTH, HEIGHT
screen = pygame.display.set_mode(size)
background = pygame.Surface((WIDTH, HEIGHT))

pygame.display.set_caption('demo_project')


def alpha_convert():
    """Конвертирует изображение в альфу"""
    try:
        for key, val in ANIMATIONS.items():
            convert_val = {}
            for key1 in val.keys():
                convert_val[key1] = [frame.convert_alpha() if bool(frame.get_flags() & pygame.SRCALPHA) else frame
                                     for frame in val[key1]]
            ANIMATIONS[key] = convert_val
    except Exception as er:
        print(f'Произошла ошибка! "{er}"')


def step_sound_func():
    """Запускает звуки ходьбы"""
    try:
        if not pygame.mixer.Channel(2).get_busy():
            if len(groups['mobs']) > 0:
                sound = choice([pygame.mixer.Sound('assets/sounds/entities_sounds/step.wav'),
                                pygame.mixer.Sound('assets/sounds/entities_sounds/step1.wav')])
                pygame.mixer.Channel(2).play(sound)
                pygame.mixer.Channel(2).set_volume(0.1)
        else:
            if len(groups['mobs']) == 0:
                pygame.mixer.Channel(2).stop()
    except Exception as er:
        print(f'Произошла ошибка! "{er}"')


def info_drawer(info_text, info_font, x, y, line_spacing):
    """Рисуем инфу по юниту"""
    for line in info_text:
        text_surface, text_rect = info_font.render(line, (100, 255, 100))
        text_rect.x, text_rect.y = x, y
        screen.blit(text_surface, text_rect)
        y += text_rect.height + line_spacing


def system_info_drawer(money_font, hp_font):
    """Рисуем Монеты и Хп Игрока"""
    text_surface, text_rect = money_font.render(f"Деньги:{game_dynamic_parameters.cash}", (100, 255, 100))  # Деньги
    text_rect.x, text_rect.y = 10, 10
    screen.blit(text_surface, text_rect)

    text_surface, text_rect = hp_font.render(f"Хп:{game_dynamic_parameters.hp}", (100, 255, 100))  # Хп
    text_rect.x, text_rect.y = 10, text_rect.height * 2
    screen.blit(text_surface, text_rect)


def entity_drawer():
    """Рисуем динамические спрйты"""
    groups['characters'].draw(screen)
    groups['mobs'].draw(screen)
    groups['shells'].draw(screen)
    groups['shop_units'].draw(screen)
    groups['drag_units'].draw(screen)
    groups['animated_map_objects'].draw(screen)


def spawn_shop_unit(shop_unit_coord, board):
    """Ставим юнитов в магазин"""
    units = [(pygame.K_1, Knight, ANIMATIONS['KNIGHT'], 90, 45),
             (pygame.K_2, Archer, ANIMATIONS['ARCHER'], 50, 25),
             (pygame.K_3, Wizard, ANIMATIONS['WIZARD'], 85, 42),
             (pygame.K_4, Priest, ANIMATIONS['PRIEST'], 80, 40),
             (pygame.K_5, ArmoredAxeman, ANIMATIONS['ARMORED_AXEMAN'], 70, 35),
             (pygame.K_6, SwordsMan, ANIMATIONS['SWORDSMAN'], 80, 40),
             (pygame.K_7, KnightTemplar, ANIMATIONS['KNIGHT_TEMPLAR'], 100, 40)]

    units_dict = {
        pygame.K_1: None,
        pygame.K_2: None,
        pygame.K_3: None,
        pygame.K_4: None,
        pygame.K_5: None,
        pygame.K_6: None,
        pygame.K_7: None
    }

    for i, arg in enumerate(units):
        key, unit, anim, price, sale = arg
        units_dict[key] = Shop(unit, (shop_unit_coord[i][0] + CELL_SIZE / 2, shop_unit_coord[i][1] + CELL_SIZE / 2),
                               anim, board, price=price, sale=sale)

    return units_dict


def spawn_lancers(board):
    """Спавнит конницу"""
    for i in range(1, board.height + 1):
        Lancer((board.left - CELL_SIZE / 2, i * CELL_SIZE + board.top - CELL_SIZE / 2),
               group_of_row=groups['rows'][i - 1])


def spaw_anim_object(anim_objects):
    """Устанавливаем анимированные объекты."""
    for obj in anim_objects:
        try:
            AnimatedMapObject((obj[0], obj[1]), ANIMATIONS[f'{obj[2].upper()}']['idle'])
        except Exception as er:
            print(f'Произошла ошибка! "{er}"')


def game_loop():
    """Основной игровой цикл"""
    # Сбрасываем изменяющиеся параметры и всех юнитов
    game_dynamic_parameters.reset_dynamic_param()
    update_group()

    try:
        tmx_data = pytmx.load_pygame(f"assets/maps/{constant.CURRENT_LVL}map.tmx")
    except Exception as er:
        print(f'Произошла ошибка! "{er}"')
        return

    # Музыка уровня
    play_background_music(f'assets/sounds/background_sounds/lvl/{constant.CURRENT_LVL}_sound.mp3')
    # Звук запуска уровня
    play_sound(sounds['game_start'])

    # Конвертируем в альфу
    alpha_convert()

    # Парсим tmx файл(карту)
    static_background = draw_map(tmx_data)
    user_cells_coord, shop_unit_coord, anim_objects = get_objects(tmx_data)

    # Поле для расстановки юнитов
    board = Board(75, user_cells_coord)

    # Ставим объекты на метки
    units_dict = spawn_shop_unit(shop_unit_coord, board)
    spawn_lancers(board)
    spaw_anim_object(anim_objects)

    # Темный фильтр
    dark_filter = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    dark_filter.fill((0, 0, 0, 70))

    # Менеджер волн
    wave_manager = WaveManager(board)

    clock = pygame.time.Clock()

    SPAWN_WAVE_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWN_WAVE_EVENT, 1500)

    money_font = pygame.freetype.Font('assets/data/font/ofont.ru_Driagwa.ttf', size=50)  # Деньги
    info_font = pygame.freetype.Font('assets/data/font/ofont.ru_Driagwa.ttf', size=25)  # Поле для информации об юните
    hp_font = pygame.freetype.Font('assets/data/font/ofont.ru_Driagwa.ttf', size=50)  # Хп

    # Настройки текста информации
    info_text = ''
    line_spacing = 10  # Расстояние между строками
    x, y, coord_info_text = None, None, None

    running = True
    while running:
        game_dynamic_parameters.frame_count += 1
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LSHIFT]:
            info_text, coord_info_text = show_info(pygame.mouse.get_pos())
            x, y = coord_info_text

        if keys[pygame.K_e]:
            board.spawn_mob(choice(
                [Slime, Skeleton, Orc, ArmoredOrc, EliteOrc, RiderOrc, ArmoredSkeleton, GreateswordSkeleton,
                 Werebear, Werewolf]))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                screens.terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    sale_unit(pygame.mouse.get_pos())
                else:
                    for key_code, unit_class in units_dict.items():
                        if keys[key_code]:
                            board.get_click(pygame.mouse.get_pos(), unit_class)
                            break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    screens.pause_screen()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LSHIFT:
                    info_text, coord_info_text = '', []
            if event.type == SPAWN_WAVE_EVENT:
                wave_manager.start_wave()

        step_sound_func()

        screen.blit(static_background, (0, 0))
        entity_drawer()

        # Если необходимо, то используем фильтр
        if constant.LVL_PARAMS[constant.CURRENT_LVL]['dark_filter']:
            screen.blit(dark_filter, (0, 0))

        # Спавн мобов волны
        wave_manager.spawn_enemy()

        # Если необходимо вывести информацию о юните
        if info_text:
            info_drawer(info_text, info_font, x, y, line_spacing)
            x, y = coord_info_text

        # Монеты/жизни
        system_info_drawer(money_font, hp_font)

        # Выигрыш/проигрыш
        if game_dynamic_parameters.GAME_MODE == 'WIN':
            pygame.mixer.Channel(1).play(sounds['game_win'])
            pygame.mixer.Channel(2).stop()
            save_statistics.save()
            screens.win_screen()
        elif game_dynamic_parameters.GAME_MODE == 'LOSE':
            pygame.mixer.Channel(1).play(sounds['game_lose'])
            pygame.mixer.Channel(2).stop()
            save_statistics.save()
            screens.lose_screen()

        groups['all_sprites'].update()
        pygame.display.flip()

        clock.tick(FPS)


if __name__ == '__main__':
    game_loop()
