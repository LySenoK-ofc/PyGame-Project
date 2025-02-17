from sprite_groups import groups


def show_info(mouse_pos):
    """Возвращает инфу о юните"""
    text, coord = '', (-1, -1)
    for unit in groups['shop_units']:
        local_mouse_pos = (mouse_pos[0] - unit.rect.x, mouse_pos[1] - unit.rect.y)

        if 0 <= local_mouse_pos[0] < unit.rect.width and 0 <= local_mouse_pos[1] < unit.rect.height:
            if unit.mask.get_at(local_mouse_pos):
                text = unit.info.split('\n')
                coord = [unit.rect.center[0] + 30, unit.rect.center[1] - 20]
                break

    return text, coord
