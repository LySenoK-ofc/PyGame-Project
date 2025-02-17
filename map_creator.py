import pygame
import pytmx

from constant import CELL_SIZE, WIDTH, HEIGHT


def draw_map(tmx_data):
    """Отрисовываем карту. Изменяем размер клеток."""
    background = pygame.Surface((WIDTH, HEIGHT))

    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):  # Проверяем, является ли слой тайловым
            if layer.name != 'anim_objects':  # Пропускаем анимированные объекты
                for x, y, gid in layer:
                    tile = tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        if layer.name in ('objects', 'log', 'shadow'):
                            y -= tile.get_height() // CELL_SIZE
                        else:
                            tile = pygame.transform.scale(tile, (CELL_SIZE, CELL_SIZE))

                        background.blit(tile, (x * CELL_SIZE, y * CELL_SIZE))

    return background


def get_objects(tmx_data):
    """Загружаем точки."""
    try:
        shop_unit_spawn_layer = tmx_data.get_layer_by_name("shop_unit_spawn")
        user_cell_layer = tmx_data.get_layer_by_name("user_cell")

        try:
            anim_objects_layer = tmx_data.get_layer_by_name("anim_objects")
        except ValueError:
            anim_objects_layer = []


    except Exception as er:
        print(f'Произошла ошибка! "{er}"')
        user_cell_layer, shop_unit_spawn_layer, anim_objects_layer = [], [], []

    user_cells_coord = [(obj.x, obj.y) for obj in user_cell_layer]
    shop_unit_coord = [(obj.x, obj.y) for obj in shop_unit_spawn_layer]
    anim_objects = [(obj.x, obj.y, obj.name) for obj in anim_objects_layer]

    return user_cells_coord, shop_unit_coord, anim_objects
