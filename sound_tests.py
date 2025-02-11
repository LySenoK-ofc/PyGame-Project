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
        9: pygame.mixer.Sound('assets/sounds/entities_sounds/sword/9.mp3')

    },
    'bow': pygame.mixer.Sound('assets/sounds/entities_sounds/bow_attack.wav'),
    'death': {
        1: pygame.mixer.Sound('assets/sounds/entities_sounds/death/1.mp3'),
        2: pygame.mixer.Sound('assets/sounds/entities_sounds/death/2.wav')
    },
    'wizard': {
        'fireball': pygame.mixer.Sound('assets/sounds/entities_sounds/Wizard/fireball.wav'),
        'ice': pygame.mixer.Sound('assets/sounds/entities_sounds/Wizard/ice.wav')
    },
    'orc': {
        'death': {
            1: pygame.mixer.Sound('assets/sounds/entities_sounds/Orc/death0.wav'),
            2: pygame.mixer.Sound('assets/sounds/entities_sounds/Orc/death1.mp3'),
            3: pygame.mixer.Sound('assets/sounds/entities_sounds/Orc/death2.mp3'),
            4: pygame.mixer.Sound('assets/sounds/entities_sounds/Orc/death3.mp3'),
            5: pygame.mixer.Sound('assets/sounds/entities_sounds/Orc/death4.mp3')
        },
        'roar': {
            1: pygame.mixer.Sound('assets/sounds/entities_sounds/Orc/roar.mp3'),
            2: pygame.mixer.Sound('assets/sounds/entities_sounds/Orc/roar2.mp3'),
            3: pygame.mixer.Sound('assets/sounds/entities_sounds/Orc/roar3.mp3')
        },
        'breathing': {
            1: pygame.mixer.Sound('assets/sounds/entities_sounds/Orc/skeleton-breathing.mp3'),
            2: pygame.mixer.Sound('assets/sounds/entities_sounds/Orc/skeleton-breathing2.mp3')
        }
    },
    'priest': {
        'aura': pygame.mixer.Sound('assets/sounds/entities_sounds/Priest/aura.wav'),
        'damage': pygame.mixer.Sound('assets/sounds/entities_sounds/Priest/damage.wav'),
        'heal': pygame.mixer.Sound('assets/sounds/entities_sounds/Priest/heal.wav'),
        'hex': pygame.mixer.Sound('assets/sounds/entities_sounds/Priest/hex.wav')
    },
    'slime': {
        'damage': pygame.mixer.Sound('assets/sounds/entities_sounds/Slime/damage.wav')
    },
    'wolf': {
        'hurt': pygame.mixer.Sound('assets/sounds/entities_sounds/Wolf/hurt.mp3'),
        'roar': pygame.mixer.Sound('assets/sounds/entities_sounds/Wolf/roar.mp3')
    },
    'archer': {
        'bow_attack': pygame.mixer.Sound('assets/sounds/entities_sounds/Archer/bow_attack.wav')
    },
    'troops_hurt': pygame.mixer.Sound('assets/sounds/entities_sounds/troops_hurt.wav'),
    'unit_spawn': pygame.mixer.Sound('assets/sounds/entities_sounds/unit_spawn.wav'),
    'button_click': pygame.mixer.Sound('assets/sounds/lobby_sounds/click_button.wav'),
    'open_door': pygame.mixer.Sound('assets/sounds/lobby_sounds/open_door.wav'),
    'door_close': pygame.mixer.Sound('assets/sounds/other_sounds/door_close.wav'),
    'wave_start': pygame.mixer.Sound('assets/sounds/other_sounds/wave_start.wav'),
    'none': pygame.mixer.Sound('assets/sounds/other_sounds/none.mp3'),
    'game_start': pygame.mixer.Sound('assets/sounds/other_sounds/start_over_game/start.mp3'),
    'game=over': pygame.mixer.Sound('assets/sounds/other_sounds/start_over_game/over.mp3')
}


def play_background_music(file):
    pygame.mixer.music.stop()
    pygame.mixer.music.load(file)
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.2)


def play_sound(sound, volume=0.5):
    sounds[sound].set_volume(volume)
    sounds[sound].play()
