from Board_class import Board
from Map_constructor import Map_constructor
from sprite_groups import *

import pygame

pygame.init()
size = width, height = 1500, 825
screen = pygame.display.set_mode(size)

if __name__ == '__main__':
    pygame.display.set_caption('demo_project')
    board = Board(6, 5, (75 * 6), (75 * 4), 75)
    Map_constructor(20, 11, board)
    board.render('map_tiles/Tiles/FieldsTile_47.png')
    clock = pygame.time.Clock()
    fps = 60

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    board.get_click(event.pos)
        map_tiles.draw(screen)
        map_objects.draw(screen)
        animated_map_objects.update()
        animated_map_objects.draw(screen)
        characters.update()
        characters.draw(screen)
        pygame.display.flip()

        print(f"map_objects: {map_objects}, map_tiles: {map_tiles}")
    clock.tick(fps)
