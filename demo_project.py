import screens
from Map_constructor import MapConstructor, generate_level, load_level
from Mobs import *
from Units import Archer, Knight, Wizard, Priest, ArmoredAxeman, SwordsMan, KnightTemplar
from constant import LEFT, TOP, FPS, WIDTH, HEIGHT
from Board_class import Board
from sprite_groups import *
import pygame
from all_animations import ANIMATIONS
import time

pygame.init()
size = WIDTH, HEIGHT
screen = pygame.display.set_mode(size)
background = pygame.Surface((WIDTH, HEIGHT))

pygame.display.set_caption('demo_project')


def game_loop():
    board = Board(6, 5, LEFT, TOP, 75)
    shop_unit_coord = generate_level(load_level('map.txt'))
    MapConstructor(20, 11, board, shop_unit_coord)

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

    running = True
    while running:
        start_time = time.time()

        constant.frame_count += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.key.get_pressed()[pygame.K_1]:
                    board.get_click(pygame.mouse.get_pos(), 'Troops', Archer)
                elif pygame.key.get_pressed()[pygame.K_2]:
                    board.get_click(pygame.mouse.get_pos(), 'Troops', Knight)
                elif pygame.key.get_pressed()[pygame.K_3]:
                    board.get_click(pygame.mouse.get_pos(), 'Troops', Wizard)
                elif pygame.key.get_pressed()[pygame.K_4]:
                    board.get_click(pygame.mouse.get_pos(), 'Troops', Priest)
                elif pygame.key.get_pressed()[pygame.K_5]:
                    board.get_click(pygame.mouse.get_pos(), 'Troops', ArmoredAxeman)
                elif pygame.key.get_pressed()[pygame.K_6]:
                    board.get_click(pygame.mouse.get_pos(), 'Troops', SwordsMan)
                elif pygame.key.get_pressed()[pygame.K_7]:
                    board.get_click(pygame.mouse.get_pos(), 'Troops', KnightTemplar)

            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]:
                    screens.main_lobby()
                if keys[pygame.K_e]:
                    pass
                # board.on_click(choice(
                #     [Slime, Skeleton, Orc, ArmoredOrc, EliteOrc, RiderOrc, ArmoredSkeleton, GreateswordSkeleton,
                #      Werebear, Werewolf]))
                # board.on_click(ArmoredSkeleton)
                if keys[pygame.K_p]:
                    print(
                        f'map_tiles:{map_tiles},\ncharacters:{characters},\nshells:{shells},\nmobs:{mobs},\nmoneys:{moneys},\nmap_objects:{map_objects},\nanimated_map_objects:{animated_map_objects}\n')

        all_sprites.update()
        all_sprites.draw(screen)

        drag_units.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

        end_time = time.time()
        execution_time = end_time - start_time
        # print(f"{execution_time} секунд")

    pygame.quit()


if __name__ == '__main__':
    game_loop()
