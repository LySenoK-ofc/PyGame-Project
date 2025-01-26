import os

import pygame


def load_image(file=None, reverse=None, colorkey=None, scale=(), convert_to_alpha=False):
    try:
        if isinstance(file, str):
            image = pygame.image.load(os.path.join(file))
        else:
            image = file

        try:
            if colorkey is not None:
                image = image.convert()
                if colorkey == -1:
                    colorkey = image.get_at((0, 0))
                image.set_colorkey(colorkey)
            else:
                image = image.convert_alpha()
        except Exception:
            print('Не удалось конвертировать в альфу')

        if reverse:
            image = pygame.transform.flip(image, True, False)
        if scale:
            image = pygame.transform.scale(image, scale)
        return image
    except Exception:
        print(f'Произошла ошибка! "{file}"')
