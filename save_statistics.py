import sqlite3
import time

import game_statistics
from constant import CURRENT_LVL


def save():
    connection = sqlite3.connect('assets/data/database/statistics.db')
    cursor = connection.cursor()
    try:
        cursor.execute(f'INSERT INTO {CURRENT_LVL} (time, spawn_units, killed_mobs, money) VALUES (?, ?, ?, ?)',
                       (f'{time.time() - game_statistics.time_start:.2f} сек', game_statistics.spawn_units, game_statistics.killed_mobs, game_statistics.cash))
        connection.commit()
    except Exception as er:
        print(f'Произошла ошибка! "{er}"')

    connection.close()
