import os

import pygame


def load_image(file=None, reverse=None, colorkey=None, scale=()):
    try:
        if isinstance(file, str):
            image = pygame.image.load(os.path.join(file))
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
        if scale:
            image = pygame.transform.scale(image, scale)
        return image
    except Exception:
        print(f'Произошла ошибка! Проверьте пути к файлам и сами файлы. "{file}"')
