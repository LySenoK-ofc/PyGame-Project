import sqlite3
import time

import game_dynamic_parameters
import constant


def save():
    connection = sqlite3.connect('assets/data/database/statistics.db')
    cursor = connection.cursor()
    try:
        cur_time = f'{time.time() - game_dynamic_parameters.time_start:.2f}'
        result = ((game_dynamic_parameters.killed_mobs *
                   game_dynamic_parameters.cash *
                   game_dynamic_parameters.spawn_units) / float(cur_time)) * (game_dynamic_parameters.hp / 5)

        cursor.execute(
            f'INSERT INTO {constant.CURRENT_LVL} (time, spawn_units, killed_mobs, money, result) VALUES (?, ?, ?, ?, ?)',
            (f'{cur_time} сек',
             game_dynamic_parameters.spawn_units,
             game_dynamic_parameters.killed_mobs,
             game_dynamic_parameters.cash,
             int(result)))
        connection.commit()
    except Exception as er:
        print(f'Произошла ошибка! "{er}"')

    connection.close()
