from random import choice

import constant
import screens
from Map_constructor import MapConstructor, generate_level, load_level
from Mobs import Slime, Skeleton, Orc, ArmoredOrc, EliteOrc, RiderOrc, ArmoredSkeleton, GreateswordSkeleton, Werewolf, \
    Werebear
from Units import Archer, Knight, Wizard, Priest, ArmoredAxeman, SwordsMan, KnightTemplar
from Waves_spawner import WaveManager
from constant import LEFT, TOP, FPS, WIDTH, HEIGHT, reset_state
from Board_class import Board
from sale_func import sale_unit
from show_info import show_unit_info
from sound_tests import play_background_music, play_sound, sounds
from sprite_groups import groups
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
                try:
                    convert_val[key1] = [frame.convert_alpha() for frame in val[key1] if
                                         bool(frame.get_flags() & pygame.SRCALPHA)]
                except pygame.error:
                    print('Не удалось конвертируем в альфу')
            ANIMATIONS[key] = convert_val
    except Exception:
        print('Ошибка изображения/структуры')


def step_sound_func():
    """Запускает звуки ходьбы"""
    if not pygame.mixer.Channel(2).get_busy():
        if len(groups['mobs']) > 0:
            sound = choice([pygame.mixer.Sound('assets/sounds/entities_sounds/step.wav'),
                            pygame.mixer.Sound('assets/sounds/entities_sounds/step1.wav')])
            pygame.mixer.Channel(2).play(sound)
            pygame.mixer.Channel(2).set_volume(0.1)
    else:
        if len(groups['mobs']) == 0:
            pygame.mixer.Channel(2).stop()


def info_drawer(info_text, info_font, x, y, line_spacing):
    """Рисуем инфу по юниту"""
    for line in info_text:
        text_surface, text_rect = info_font.render(line, (100, 255, 100))
        text_rect.x, text_rect.y = x, y
        screen.blit(text_surface, text_rect)
        y += text_rect.height + line_spacing


def system_info_drawer(money_font, hp_font):
    """Рисуем Монеты и Хп Игрока"""
    text_surface, text_rect = money_font.render(f"Деньги:{constant.cash}", (100, 255, 100))  # Деньги
    text_rect.x, text_rect.y = 10, 10
    screen.blit(text_surface, text_rect)

    text_surface, text_rect = hp_font.render(f"Хп:{constant.hp}", (100, 255, 100))  # Хп
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


def game_loop():
    """Основной игровой цикл"""
    board = Board(6, 5, LEFT, TOP, 75)
    shop_unit_coord = generate_level(load_level('map.txt'))
    MapConstructor(20, 11, board, shop_unit_coord)
    groups['map_tiles'].draw(screen)
    groups['map_objects'].draw(screen)
    reset_state()

    wave_manager = WaveManager()
    play_background_music('assets/sounds/background_sounds/lvl/Shiro_Sagisu_-_Treachery_72363454.mp3')
    play_sound(sounds['game_start'])

    static_background = pygame.Surface((WIDTH, HEIGHT))
    static_background.blit(screen, (0, 0))

    alpha_convert()

    clock = pygame.time.Clock()

    SPAWN_WAVE_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWN_WAVE_EVENT, 1500)

    money_font = pygame.freetype.Font('assets/data/Adbnorm.ttf', size=50)  # Деньги
    info_font = pygame.freetype.Font('assets/data/Adbnorm.ttf', size=20)  # Поле для информации об юните
    hp_font = pygame.freetype.Font('assets/data/Adbnorm.ttf', size=50)  # Деньги

    info_text = ''
    line_spacing = 10  # Расстояние между строками
    x, y, coord_info_text = None, None, None

    # Словарь для выбора юнита
    unit_mapping = {
        pygame.K_1: Archer,
        pygame.K_2: Knight,
        pygame.K_3: Wizard,
        pygame.K_4: Priest,
        pygame.K_5: ArmoredAxeman,
        pygame.K_6: SwordsMan,
        pygame.K_7: KnightTemplar
    }

    running = True
    while running:
        constant.frame_count += 1
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LSHIFT]:
            info_text, coord_info_text = show_unit_info(pygame.mouse.get_pos())
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
                    for key_code, unit_class in unit_mapping.items():
                        if keys[key_code]:
                            board.get_click(pygame.mouse.get_pos(), unit_class)
                            break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    play_background_music('assets/sounds/background_sounds/lobby/lobby_sound.mp3')
                    screens.main_lobby()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LSHIFT:
                    info_text, coord_info_text = '', []
            if event.type == SPAWN_WAVE_EVENT:
                wave_manager.start_wave()

        step_sound_func()

        screen.blit(static_background, (0, 0))
        entity_drawer()

        wave_manager.spawn_enemy()

        if info_text:
            info_drawer(info_text, info_font, x, y, line_spacing)
            x, y = coord_info_text

        system_info_drawer(money_font, hp_font)

        groups['all_sprites'].update()
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    game_loop()
