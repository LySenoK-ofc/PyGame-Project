from Map_constructor import Map_constructor
from constant import FPS
from Board_class import Board
from sprite_groups import *
import pygame

pygame.init()
size = width, height = 1500, 825
screen = pygame.display.set_mode(size)

if __name__ == '__main__':
    pygame.display.set_caption('demo_project')
    board = Board(6, 5, (75 * 6), (75 * 4), 75)
    Map_constructor(20, 11, board)
    board.render('assets/map_tiles/Tiles/FieldsTile_47.png')
    clock = pygame.time.Clock()
    fps = 60

    running = True

    while running:
        screen.fill('black')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos, 'soldier')
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_e]:
                    board.on_click()
                    print("<_Successful spawned mob_>")
                if keys[pygame.K_p]:
                    print(
                        f'map_tiles:{map_tiles},\ncharacters:{characters},\nshells:{shells},\nmobs:{mobs},\nmoneys:{moneys},\nmap_objects:{map_objects},\nanimated_map_objects:{animated_map_objects}\n')

        all_sprites.update()
        all_sprites.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
