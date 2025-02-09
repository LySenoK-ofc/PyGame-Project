import pygame.sprite as sprite


def update_group():
    global groups
    for k in groups.keys():
        for i in groups[k]:
            try:
                i.kill()
            except AttributeError:
                for k1 in groups[k].keys():
                    for j in groups[k][k1]:
                        j.kill()


groups = {
    "all_sprites": sprite.Group(),

    "characters": sprite.Group(),
    "shells": sprite.Group(),
    "mobs": sprite.Group(),

    "shop_units": sprite.Group(),
    "drag_units": sprite.Group(),

    "rows": {
        0: sprite.Group(),
        1: sprite.Group(),
        2: sprite.Group(),
        3: sprite.Group(),
        4: sprite.Group(),
        5: sprite.Group(),
    },

    "moneys": sprite.Group(),

    "map_tiles": sprite.Group(),
    "map_objects": sprite.Group(),
    "animated_map_objects": sprite.Group(),

    "level_doors": sprite.Group(),
    "buttons": sprite.Group(),

"characters_page": pygame.sprite.Group(),
"mobs_page": pygame.sprite.Group()
}