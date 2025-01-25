from Board_class import Board
from Map_constructor import Map_constructor, load_level, generate_level
from sprite_groups import *
from constant import WIDTH, HEIGHT

import pygame

pygame.init()
size = width, height = 1500, 825
screen = pygame.display.set_mode(size)

if __name__ == '__main__':
    pygame.display.set_caption('demo_project')
    board = Board(6, 5, (75 * 6), (75 * 4), 75)
    clock = pygame.time.Clock()
    fps = 60

    generate_level(load_level('map.txt'))
    Map_constructor(WIDTH, HEIGHT, board)
    board.render('assets/map_tiles/Tiles/FieldsTile_47.png')

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
    clock.tick(fps)
