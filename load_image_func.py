import os

import pygame


def load_image(file=None, reverse=None, colorkey=None, scale=()):
    try:
        if isinstance(file, str):
            image = pygame.image.load(os.path.join(file))
        else:
            image = file

        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)

        if reverse:
            image = pygame.transform.flip(image, True, False)
        if scale:
            image = pygame.transform.scale(image, scale)
        return image
    except Exception as er:
        print(f'Произошла ошибка! "{er}"')
