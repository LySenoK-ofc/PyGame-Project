from load_animation_func import load_anim

ANIMATIONS = {
    'ARCHER': load_anim("assets/animations/Troops/archer/Archer.png", 'troops', 'archer'),
    'KNIGHT': load_anim("assets/animations/Troops/knight/Knight.png", 'troops', 'knight'),
    'LANCER': load_anim("assets/animations/Troops/lancer/Lancer.png", 'troops', 'lancer', scale=(230, 230)),
    'WIZARD': load_anim("assets/animations/Troops/wizard/Wizard.png", 'troops', 'wizard'),
    'PRIEST': load_anim("assets/animations/Troops/priest/Priest.png", 'troops', 'priest'),
    'ARMORED_AXEMAN': load_anim("assets/animations/Troops/armored_axeman/Armored Axeman.png", 'troops', 'armored_axeman'),
    'ARROW01': load_anim("assets/animations/Troops/arrows/Arrow01(100x100).png", 'arrows', 'arrow01', scale=(230, 230)),
    'ORC': load_anim("assets/animations/Mobs/orc/Orc.png", 'mobs', 'orc', True),
    'ELITE_ORC': load_anim("assets/animations/Mobs/elite_orc/Elite Orc.png", 'mobs', 'elite_orc', True),
    'ARMORED_ORC': load_anim("assets/animations/Mobs/armored_orc/Armored Orc.png", 'mobs', 'armored_orc', True),
    'RIDER_ORC': load_anim("assets/animations/Mobs/rider_orc/Orc rider.png", 'mobs', 'rider_orc', True)
}
