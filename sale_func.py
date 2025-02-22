import game_dynamic_parameters
from sprite_groups import groups


def sale_unit(mouse_pos):
    """Продаём юнита"""
    for unit in groups['shop_units']:
        local_mouse_pos = (mouse_pos[0] - unit.rect.x, mouse_pos[1] - unit.rect.y)
        if 0 <= local_mouse_pos[0] < unit.rect.width and 0 <= local_mouse_pos[1] < unit.rect.height:
            if unit.mask.get_at(local_mouse_pos) and unit in groups['characters']:
                game_dynamic_parameters.cash += unit.sale
                unit.lose_hp(1000)
                break
