import constant
from Map_constructor import MapConstructor
from Units import Archer, Knight, Wizard, Priest
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

if __name__ == '__main__':
    pygame.display.set_caption('demo_project')

    board = Board(6, 5, LEFT, TOP, 75)
    MapConstructor(20, 11, board)

    # # Конвертируем в альфу
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
                    board.get_click(pygame.mouse.get_pos(), Archer)
                elif pygame.key.get_pressed()[pygame.K_2]:
                    board.get_click(pygame.mouse.get_pos(), Knight)
                elif pygame.key.get_pressed()[pygame.K_3]:
                    board.get_click(pygame.mouse.get_pos(), Wizard)
                elif pygame.key.get_pressed()[pygame.K_4]:
                    board.get_click(pygame.mouse.get_pos(), Priest)

            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_e]:
                    board.on_click()
                if keys[pygame.K_p]:
                    print(
                        f'map_tiles:{map_tiles},\ncharacters:{characters},\nshells:{shells},\nmobs:{mobs},\nmoneys:{moneys},\nmap_objects:{map_objects},\nanimated_map_objects:{animated_map_objects}\n')

        all_sprites.update()

        all_sprites.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

        end_time = time.time()
        execution_time = end_time - start_time
        print(f"{execution_time} секунд", constant.frame_count)

    pygame.quit()
