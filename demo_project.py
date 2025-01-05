from load_image_func import load_image
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

IDLE = 'Idle'
WALK = 'Walk'
DEATH = 'Death'
ATTACK1 = 'Attack01'
ATTACK2 = 'Attack02'
BOW_ATTACK = 'Bow_attack'

class Money(pygame.sprite.Sprite):
    def __init__(self, group, coord, balance_view=False):
        super().__init__(group)
        self.anim_money = [load_image('animations/Money/1.png', False, (255, 255, 255)),
                           load_image('animations/Money/2.png', False, (255, 255, 255)),
                           load_image('animations/Money/3.png', False, (255, 255, 255)),
                           load_image('animations/Money/4.png', False, (255, 255, 255)),
                           load_image('animations/Money/5.png', False, (255, 255, 255)),
                           load_image('animations/Money/6.png', False, (255, 255, 255))]
        self.image = self.anim_money[0]
        self.rect = self.image.get_rect()
        if balance_view:
            self.rect.x = 1100
            self.rect.y = -25
        else:
            self.rect.x = coord[1] * 75 - 15
            self.rect.y = coord[0] * 75 - 50
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate_update = 150

    def update(self, *args, **kwargs):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate_update:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.anim_money):
                self.frame = 0
            self.image = self.anim_money[self.frame]


if __name__ == '__main__':
    pygame.display.set_caption('demo_project')
    board = Board(7, 5, 150, 300, 75)
    clock = pygame.time.Clock()
    cycle_stage = PROCESS
    fps = 45
    running = True
    Money(moneys, (1100, 0), True)
    for i in range(4, height // 75):
        for j in range(width // 75):
            Map_tile(map_tiles, [j * 75, i * 75], 'map_tiles/grass_tile_1.png')
    while running:
        screen.fill('white')
        if cycle_stage == PAUSE:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_ESCAPE]:
                        cycle_stage = PROCESS
            screen.fill('black')
            font = pygame.font.Font('assets/Ratanegra-Cyrillic.otf', 75)
            pause_text = font.render("Pause Menu", True, (255, 255, 255))
            pause_text_x = width // 2 - pause_text.get_width() // 2
            pause_text_y = 25
            screen.blit(pause_text, (pause_text_x, pause_text_y))
            continue_text = font.render("Continue", True, (255, 255, 255))
            options_text = font.render("Options", True, (255, 255, 255))
            dictionary_text = font.render("Dictionary", True, (255, 255, 255))
            exit_text = font.render("Exit", True, (255, 255, 255))
            button_text_x = 75
            button_text_y = pause_text_y + 100
            screen.blit(continue_text, (button_text_x, button_text_y))
            screen.blit(options_text, (button_text_x, button_text_y + 100))
            screen.blit(dictionary_text, (button_text_x, button_text_y + 200))
            screen.blit(exit_text, (button_text_x, button_text_y + 300))

        elif cycle_stage == PROCESS:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    board.get_click(event.pos)
                if event.type == pygame.KEYDOWN:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_ESCAPE]:
                        cycle_stage = PAUSE
                    if keys[pygame.K_SPACE]:
                        for sprite in characters:
                            if sprite.mode == IDLE:
                                sprite.mode = BOW_ATTACK
                            else:
                                sprite.mode = IDLE
                            sprite.frame = 0
                    if keys[pygame.K_e]:
                        Orc(mobs)
                        print("<_Successful spawned mob_>")
            map_tiles.draw(screen)
            board.render('map_tiles/grass_tile_2.png')
            mobs.update()
            mobs.draw(screen)
            characters.update()
            characters.draw(screen)
            killed_entities.update()
            killed_entities.draw(screen)
            shells.update()
            shells.draw(screen)
            moneys.update()
            moneys.draw(screen)
        pygame.display.flip()
    clock.tick(fps)

    pygame.quit()
