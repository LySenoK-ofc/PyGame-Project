from Orc_class import Orc
from Board_class import Board
from Map_tiles_class import Map_tile
from sprite_groups import *

import pygame

pygame.init()
size = width, height = 1200, 675
screen = pygame.display.set_mode(size)

PROCESS = 'Process'
FINISH = 'Finish'
PAUSE = 'Pause'
PREPARE = 'Prepare'

board = Board(6, 5, (64 * 6), (64 * 4), 64)

if __name__ == '__main__':
    pygame.display.set_caption('demo_project')
    clock = pygame.time.Clock()
    fps = 30

    for i in range(height // 64):
        for j in range(width // 64):
            if i >= height // 64 - 2:
                Map_tile(map_tiles, (j * 64, i * 64), 'new_map_tiles(64x64)/Tiles/FieldsTile_38.png')
            elif board.left // 64 < j and board.top // 64 <= i < height // 64 - 1:
                Map_tile(map_tiles, (j * 64, i * 64), 'new_map_tiles(64x64)/Tiles/FieldsTile_31.png')
            elif i == 2 and (j == 6 or j == 9 or j == 12 or j == 15):
                Map_tile(map_tiles, (j * 64, i * 64), 'new_map_tiles(64x64)/Tiles/FieldsTile_47.png')
            elif i >= height // 64 - 2:
                Map_tile(map_tiles, (j * 64, i * 64), 'new_map_tiles(64x64)/Tiles/FieldsTile_38.png')
            elif i == 4 and j == 5:
                Map_tile(map_tiles, (j * 64, i * 64), 'new_map_tiles(64x64)/Tiles/FieldsTile_43.png')
            elif j == 5 and i == 8:
                Map_tile(map_tiles, (j * 64, i * 64), 'new_map_tiles(64x64)/Tiles/FieldsTile_44.png')
            elif i == 1:
                Map_tile(map_tiles, (j * 64, i * 64), 'new_map_tiles(64x64)/Tiles/FieldsTile_38.png')
            elif 0 <= j < 5:
                Map_tile(map_tiles, (j * 64, i * 64), 'new_map_tiles(64x64)/Tiles/FieldsTile_38.png')
            elif i <= 3:
                Map_tile(map_tiles, (j * 64, i * 64), 'new_map_tiles(64x64)/Tiles/FieldsTile_38.png')
            elif j == 5:
                Map_tile(map_tiles, (j * 64, i * 64), 'new_map_tiles(64x64)/Tiles/FieldsTile_40.png')

    Map_tile(map_objects, (125, 200), 'new_map_tiles(64x64)/Objects/camp/1.png')
    Map_tile(map_objects, (10, 150), 'new_map_tiles(64x64)/Objects/camp/2.png')

    Map_tile(map_objects, (440, 30), 'new_map_tiles(64x64)/Objects/decor/Tree1.png')
    Map_tile(map_objects, (640, 30), 'new_map_tiles(64x64)/Objects/decor/Tree1.png')
    Map_tile(map_objects, (835, 30), 'new_map_tiles(64x64)/Objects/decor/Tree1.png')
    Map_tile(map_objects, (1030, 30), 'new_map_tiles(64x64)/Objects/decor/Tree1.png')

    running = True

    board.render('new_map_tiles(64x64)/Tiles/FieldsTile_47.png')

    while running:
        screen.fill('white')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos)
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_e]:
                    Orc(mobs)
                    print("<_Successful spawned mob_>")
        map_tiles.draw(screen)
        map_objects.draw(screen)
        animated_map_objects.update()
        animated_map_objects.draw(screen)

        mobs.update()
        mobs.draw(screen)
        characters.update()
        characters.draw(screen)
        killed_entities.update()
        killed_entities.draw(screen)
        shells.update()
        shells.draw(screen)

        pygame.display.flip()
        # Для наглядности, какие сущности соществуют
        print(f'map_tiles:{map_tiles}, characters:{characters}, shells:{shells}, mobs:{mobs}, killed_entities:{killed_entities}, moneys:{moneys}, map_objects:{map_objects}, animated_map_objects:{animated_map_objects}')
        clock.tick(fps)

    pygame.quit()
