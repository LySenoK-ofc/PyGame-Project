from Board_class import Board
from Map_constructor import Map_constructor, load_level, generate_level
from sprite_groups import *
from constant import WIDTH, HEIGHT
from screens import terminate, pick_level_screen

import pygame

pygame.init()
size = width, height = 1500, 825
screen = pygame.display.set_mode(size)

if __name__ == '__main__':
    pygame.display.set_caption('demo_project')
    board = Board(6, 5, (75 * 6), (75 * 4), 75)
    clock = pygame.time.Clock()
    fps = 60

    pick_level_screen(screen)
    clock.tick(fps)
