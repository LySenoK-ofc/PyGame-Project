import pygame

pygame.mixer.pre_init()
pygame.init()

sounds = {
    'sword': {
        1: pygame.mixer.Sound('assets/sounds/entities_sounds/sword/1.wav'),
        2: pygame.mixer.Sound('assets/sounds/entities_sounds/sword/2.wav'),
        3: pygame.mixer.Sound('assets/sounds/entities_sounds/sword/3.wav'),
        4: pygame.mixer.Sound('assets/sounds/entities_sounds/sword/4(weight).mp3'),
        5: pygame.mixer.Sound('assets/sounds/entities_sounds/sword/5(fast).mp3'),
        6: pygame.mixer.Sound('assets/sounds/entities_sounds/sword/6.wav'),
        7: pygame.mixer.Sound('assets/sounds/entities_sounds/sword/7(fast).mp3'),
        8: pygame.mixer.Sound('assets/sounds/entities_sounds/sword/8.mp3'),
        9: pygame.mixer.Sound('assets/sounds/entities_sounds/sword/9.mp3'),
        10: pygame.mixer.Sound('assets/sounds/entities_sounds/sword/10(fire).wav')

    },
    'death': {
        1: pygame.mixer.Sound('assets/sounds/entities_sounds/death/1.mp3'),
        2: pygame.mixer.Sound('assets/sounds/entities_sounds/death/2.mp3')
    },
    'wizard': {
        'fireball': pygame.mixer.Sound('assets/sounds/entities_sounds/Wizard/fireball.wav'),
        'ice': pygame.mixer.Sound('assets/sounds/entities_sounds/Wizard/ice.wav')
    },
    'mobs': {
        'death': {
            1: pygame.mixer.Sound('assets/sounds/entities_sounds/Mobs/death0.wav'),
            2: pygame.mixer.Sound('assets/sounds/entities_sounds/Mobs/death1.mp3'),
            3: pygame.mixer.Sound('assets/sounds/entities_sounds/Mobs/death2.mp3'),
            4: pygame.mixer.Sound('assets/sounds/entities_sounds/Mobs/death3.mp3'),
            5: pygame.mixer.Sound('assets/sounds/entities_sounds/Mobs/death4.mp3'),
            6: pygame.mixer.Sound('assets/sounds/entities_sounds/Mobs/death5.mp3'),
        },
        'roar': {
            1: pygame.mixer.Sound('assets/sounds/entities_sounds/Mobs/roar.mp3'),
            2: pygame.mixer.Sound('assets/sounds/entities_sounds/Mobs/roar2.mp3'),
            3: pygame.mixer.Sound('assets/sounds/entities_sounds/Mobs/roar3.mp3'),
            4: pygame.mixer.Sound('assets/sounds/entities_sounds/Mobs/roar4.mp3'),
            5: pygame.mixer.Sound('assets/sounds/entities_sounds/Mobs/roar5.mp3')
        }
    },
    'priest': {
        'aura': pygame.mixer.Sound('assets/sounds/entities_sounds/Priest/aura.wav'),
        'damage': pygame.mixer.Sound('assets/sounds/entities_sounds/Priest/damage.wav'),
        'damage2': pygame.mixer.Sound('assets/sounds/entities_sounds/Priest/damage2.mp3'),
        'heal': pygame.mixer.Sound('assets/sounds/entities_sounds/Priest/heal.wav'),
        'hex': pygame.mixer.Sound('assets/sounds/entities_sounds/Priest/hex.wav'),
        'death1': pygame.mixer.Sound('assets/sounds/entities_sounds/Priest/death1.mp3'),
        'death2': pygame.mixer.Sound('assets/sounds/entities_sounds/Priest/death2.mp3')
    },
    'slime': {
        'damage': pygame.mixer.Sound('assets/sounds/entities_sounds/Slime/damage.wav')
    },
    'animals': {
        'wolf_hurt': pygame.mixer.Sound('assets/sounds/entities_sounds/Animals/wolf_hurt.mp3'),
        'wolf_roar': pygame.mixer.Sound('assets/sounds/entities_sounds/Animals/wolf_roar.mp3'),
        'bear_death': pygame.mixer.Sound('assets/sounds/entities_sounds/Animals/bear_death.mp3'),
        'bear_roar': pygame.mixer.Sound('assets/sounds/entities_sounds/Animals/bear_roar.mp3'),
        'bear_atk': pygame.mixer.Sound('assets/sounds/entities_sounds/Animals/bear_atk.mp3')
    },
    'archer': {
        'bow_attack': pygame.mixer.Sound('assets/sounds/entities_sounds/Archer/bow_attack.wav')
    },
    'hurt': {
        1: pygame.mixer.Sound('assets/sounds/entities_sounds/hurt/1.wav'),
        2: pygame.mixer.Sound('assets/sounds/entities_sounds/hurt/2.wav')
    },
    'unit_spawn': pygame.mixer.Sound('assets/sounds/entities_sounds/unit_spawn.wav'),
    'step': pygame.mixer.Sound('assets/sounds/entities_sounds/step.wav'),
    'button_click': pygame.mixer.Sound('assets/sounds/lobby_sounds/click_button.wav'),
    'open_door': pygame.mixer.Sound('assets/sounds/lobby_sounds/open_door.wav'),
    'door_close': pygame.mixer.Sound('assets/sounds/other_sounds/door_close.wav'),
    'wave_start': pygame.mixer.Sound('assets/sounds/other_sounds/wave_start.wav'),
    'none': pygame.mixer.Sound('assets/sounds/other_sounds/none.mp3'),
    'game_start': pygame.mixer.Sound('assets/sounds/other_sounds/start_over_game/start.mp3'),
    'game_win': pygame.mixer.Sound('assets/sounds/other_sounds/start_over_game/win.wav'),
    'game_lose': pygame.mixer.Sound('assets/sounds/other_sounds/start_over_game/lose.wav')
}


def play_background_music(file, volume=0.2):
    """Проигрывает фоновую музыку"""
    try:
        pygame.mixer.music.stop()
        pygame.mixer.music.load(file)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(volume)
    except Exception:
        pass


def play_sound(sound, volume=0.5):
    """Проигрывает звук (0 канал)"""
    try:
        sound.set_volume(volume)
        sound.play()
    except Exception:
        pass
