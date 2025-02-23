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


def get_statistic():
    connection = sqlite3.connect('assets/data/database/statistics.db')
    cursor = connection.cursor()
    try:
        result1 = cursor.execute('''SELECT * FROM lvl1 WHERE result = (SELECT MAX(result) FROM lvl1)''').fetchall()
        result2 = cursor.execute('''SELECT * FROM lvl2 WHERE result = (SELECT MAX(result) FROM lvl2)''').fetchall()
        return result1[0], result2[0]
    except Exception as er:
        print(f'Произошла ошибка! "{er}"')

    connection.close()