import json
from load_image_func import load_image
import pygame


def load_anim(path, type_mob, mob, reverse=None, scale=(290, 290)):
    with open("data/cut_sheet_parameters.json") as f:
        atlas = pygame.image.load(path)
        frames = {}
        animations = json.load(f)

        for i in animations["animation's parameters"][type_mob][mob].keys():
            frames[i] = [
                load_image(file=atlas.subsurface((x * animations["animation's parameters"][type_mob][mob][i]["width"],
                                                  animations["animation's parameters"][type_mob][mob][i]["row"] *
                                                  animations["animation's parameters"][type_mob][mob][i]["height"],
                                                  animations["animation's parameters"][type_mob][mob][i]["width"],
                                                  animations["animation's parameters"][type_mob][mob][i]["height"])),
                           reverse=reverse, scale=scale)
                for x in range(animations["animation's parameters"][type_mob][mob][i]["column"])]

    return frames
