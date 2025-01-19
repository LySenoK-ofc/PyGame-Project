import os
import sys

import pygame


def load_image(name=None, file=None, reverse=None, colorkey=None):
    try:
        if file is None:
            if not os.path.isfile(name):
                print(f"Файл с изображением '{name}' не найден")
                sys.exit()
            image = pygame.image.load(os.path.join(name))
        else:
            image = file

        if colorkey is not None:
            image = image.convert()
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            image = image.convert_alpha()
        if reverse:
            image = pygame.transform.flip(image, True, False)
        image = pygame.transform.scale(image, (290, 290))
        return image
    except Exception:
        print('Произошла ошибка! Проверьте пути к файлам и сами файлы.')
