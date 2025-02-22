import time

frame_count = 0
cash = 250
hp = 5
time_start = 0
killed_mobs = 0
spawn_units = 0


def reset_state():
    """Сбрасываем параметры."""
    global frame_count, cash, hp, killed_mobs, spawn_units, time_start
    frame_count = 0
    cash = 250
    hp = 5
    killed_mobs = 0
    spawn_units = 0
    time_start = time.time()
