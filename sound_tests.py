import pygame

pygame.mixer.pre_init()
pygame.init()

sounds = {'sword': pygame.mixer.Sound('assets/sounds/entities_sounds/sword_attack.wav'),
          'bow': pygame.mixer.Sound('assets/sounds/entities_sounds/bow_attack.wav'),
          'troops_hurt': pygame.mixer.Sound('assets/sounds/entities_sounds/troops_hurt.wav'),
          'fireball': pygame.mixer.Sound('assets/sounds/entities_sounds/fireball_attack.wav'),
          'ice': None,
          'heal': None,
          'block': None,
          'button_click': pygame.mixer.Sound('assets/sounds/lobby_sounds/click_button.wav'),
          'open_door': pygame.mixer.Sound('assets/sounds/lobby_sounds/open_door.wav')}


def play_background_music(file):
    pygame.mixer.music.stop()
    pygame.mixer.music.load(file)
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.2)


def play_sound(sound, volume=0.5):
    sounds[sound].set_volume(volume)
    sounds[sound].play()

# play_sound_event = pygame.USEREVENT + 1
# pygame.time.set_timer(play_sound_event, 2000)
#
# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             terminate()
#         if event.type == play_sound_event:
#             play_entity_sound('troops_hurt', 0.20)
