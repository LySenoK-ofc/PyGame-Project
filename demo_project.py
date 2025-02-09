from random import choice

import constant
import screens
from Map_constructor import MapConstructor, generate_level, load_level
from Mobs import Slime, Skeleton, Orc, ArmoredOrc, EliteOrc, RiderOrc, ArmoredSkeleton, GreateswordSkeleton, Werewolf, \
    Werebear
from Units import Archer, Knight, Wizard, Priest, ArmoredAxeman, SwordsMan, KnightTemplar
from Waves_spawner import WaveManager
from constant import LEFT, TOP, FPS, WIDTH, HEIGHT
from Board_class import Board
from sale_func import sale_unit
from show_info import show_unit_info
from sprite_groups import groups
import pygame
import pygame.freetype
from all_animations import ANIMATIONS

pygame.init()
size = WIDTH, HEIGHT
screen = pygame.display.set_mode(size)
background = pygame.Surface((WIDTH, HEIGHT))

pygame.display.set_caption('demo_project')


def game_loop():
    board = Board(6, 5, LEFT, TOP, 75)
    shop_unit_coord = generate_level(load_level('map.txt'))
    MapConstructor(20, 11, board, shop_unit_coord)

    wave_manager = WaveManager()

    # Конвертируем спрайты в альфу
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

    clock = pygame.time.Clock()

    SPAWN_WAVE_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWN_WAVE_EVENT, 1500)

    money_font = pygame.freetype.Font('assets/data/Adbnorm.ttf', size=50)  # Деньги
    info_font = pygame.freetype.Font('assets/data/Adbnorm.ttf', size=20)  # Поле для информации об юните
    hp_font = pygame.freetype.Font('assets/data/Adbnorm.ttf', size=50)  # Деньги

    info_text = ''
    line_spacing = 10  # Расстояние между строками
    x, y, coord_info_text = None, None, None

    running = True
    while running:
        constant.frame_count += 1
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LSHIFT]:
            info_text, coord_info_text = show_unit_info(pygame.mouse.get_pos())
            x, y = coord_info_text
        if keys[pygame.K_e]:
            board.on_click(choice(
                [Slime, Skeleton, Orc, ArmoredOrc, EliteOrc, RiderOrc, ArmoredSkeleton, GreateswordSkeleton,
                 Werebear, Werewolf]))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                screens.terminate()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    sale_unit(pygame.mouse.get_pos())
                else:
                    if keys[pygame.K_1]:
                        board.get_click(pygame.mouse.get_pos(), 'Troops', Archer)
                    elif keys[pygame.K_2]:
                        board.get_click(pygame.mouse.get_pos(), 'Troops', Knight)
                    elif keys[pygame.K_3]:
                        board.get_click(pygame.mouse.get_pos(), 'Troops', Wizard)
                    elif keys[pygame.K_4]:
                        board.get_click(pygame.mouse.get_pos(), 'Troops', Priest)
                    elif keys[pygame.K_5]:
                        board.get_click(pygame.mouse.get_pos(), 'Troops', ArmoredAxeman)
                    elif keys[pygame.K_6]:
                        board.get_click(pygame.mouse.get_pos(), 'Troops', SwordsMan)
                    elif keys[pygame.K_7]:
                        board.get_click(pygame.mouse.get_pos(), 'Troops', KnightTemplar)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    screens.main_lobby()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LSHIFT:
                    info_text, coord_info_text = '', []

            if event.type == SPAWN_WAVE_EVENT:
                wave_manager.start_wave()

        groups['all_sprites'].update()
        groups['all_sprites'].draw(screen)

        groups['drag_units'].draw(screen)

        wave_manager.spawn_enemy()

        if info_text:  # Инфа
            for line in info_text:
                text_surface, text_rect = info_font.render(line, (100, 255, 100))
                text_rect.x, text_rect.y = x, y
                screen.blit(text_surface, text_rect)
                y += text_rect.height + line_spacing
            x, y = coord_info_text

        text_surface, text_rect = money_font.render(f"Деньги:{constant.cash}", (100, 255, 100))  # Деньги
        text_rect.x, text_rect.y = 10, 10  # Деньги
        screen.blit(text_surface, text_rect)  # Деньги

        text_surface, text_rect = hp_font.render(f"Хп:{constant.hp}", (100, 255, 100))  # Хп
        text_rect.x, text_rect.y = 10, text_rect.height * 2  # Хп
        screen.blit(text_surface, text_rect)  # Хп

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    game_loop()
