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


def get_statistic(n_lvl):
    connection = sqlite3.connect('assets/data/database/statistics.db')
    cursor = connection.cursor()
    statistic = None
    try:
        if n_lvl == 1:
            statistic = cursor.execute(
                '''SELECT * FROM lvl1 WHERE result = (SELECT MAX(result) FROM lvl1)''').fetchall()[0]
        elif n_lvl == 2:
            statistic = cursor.execute(
                '''SELECT * FROM lvl2 WHERE result = (SELECT MAX(result) FROM lvl2)''').fetchall()[0]
        statistic = (f'Лучший результат на {n_lvl} уровне:',
                     f'Номер игры: {statistic[0]}',
                     f'Время прохождения: {statistic[1]}',
                     f'Использовано воинов: {statistic[2]}',
                     f'Убито монстров: {statistic[3]}',
                     f'Монет заработано: {statistic[4]}',
                     f'Итоговый результат: {statistic[5]}')
        connection.close()
        return statistic

    except Exception:
        statistic = (f'Лучший результат на {n_lvl} уровне:',
                     'Данные о проходжении этого уровня отсутствуют',)
        connection.close()
        return statistic
