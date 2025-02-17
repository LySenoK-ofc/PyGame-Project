import json
from load_image_func import load_image
import pygame


def load_anim(path, entity_type, entity, reverse=None, scale=(290, 290)):
    with open("assets/data/params/cut_sheet_parameters.json") as f:
        try:
            atlas = pygame.image.load(path)
            frames = {}
            animations = json.load(f)

            for i in animations["animation's parameters"][entity_type][entity].keys():
                frames[i] = [
                    load_image(file=atlas.subsurface(
                        (x * animations["animation's parameters"][entity_type][entity][i]["width"],
                         animations["animation's parameters"][entity_type][entity][i]["row"] *
                         animations["animation's parameters"][entity_type][entity][i]["height"],
                         animations["animation's parameters"][entity_type][entity][i]["width"],
                         animations["animation's parameters"][entity_type][entity][i]["height"])),
                               reverse=reverse, scale=scale)
                    for x in range(animations["animation's parameters"][entity_type][entity][i]["column"])]
        except Exception as er:
            print(f'Произошла ошибка! "{er}"')

    return frames
