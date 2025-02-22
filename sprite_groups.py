import pygame.sprite as sprite


def update_group():
    """Очищаем все группы спрайтов."""
    for group in groups.values():
        clear_group(group)


def clear_group(group):
    """Удаляет все спрайты из переданной группы."""
    if isinstance(group, sprite.Group):
        try:
            group.empty()
        except Exception as er:
            print(f'Произошла ошибка! "{er}"')
    elif isinstance(group, dict):
        for sub_group in group.values():
            clear_group(sub_group)  # Рекурсивно очищаем вложенные словари


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

    "characters_page": sprite.Group(),
    "mobs_page": sprite.Group(),
    "current_dict_entity": sprite.Group(),

    "characters_view": sprite.Group(),
    "mobs_view": sprite.Group()
}
