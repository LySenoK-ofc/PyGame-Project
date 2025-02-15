from load_animation_func import load_anim

ANIMATIONS = {
    'ARCHER': load_anim("assets/animations/Troops/archer/Archer.png", 'troops', 'archer'),
    'KNIGHT': load_anim("assets/animations/Troops/knight/Knight.png", 'troops', 'knight'),
    'LANCER': load_anim("assets/animations/Troops/lancer/Lancer.png", 'troops', 'lancer', scale=(230, 230)),
    'WIZARD': load_anim("assets/animations/Troops/wizard/Wizard.png", 'troops', 'wizard'),
    'PRIEST': load_anim("assets/animations/Troops/priest/Priest.png", 'troops', 'priest'),
    'SWORDSMAN': load_anim("assets/animations/Troops/swordsman/Swordsman.png", 'troops', 'swordsman'),
    'KNIGHT_TEMPLAR': load_anim("assets/animations/Troops/knight_templar/Knight Templar.png", 'troops', 'knight_templar'),
    'ARMORED_AXEMAN': load_anim("assets/animations/Troops/armored_axeman/Armored Axeman.png", 'troops', 'armored_axeman'),
    'ARROW01': load_anim("assets/animations/Troops/arrows/Arrow01(100x100).png", 'arrows', 'arrow01', scale=(230, 230)),
    'ORC': load_anim("assets/animations/Mobs/orc/Orc.png", 'mobs', 'orc', True),
    'ELITE_ORC': load_anim("assets/animations/Mobs/elite_orc/Elite Orc.png", 'mobs', 'elite_orc', True),
    'ARMORED_ORC': load_anim("assets/animations/Mobs/armored_orc/Armored Orc.png", 'mobs', 'armored_orc', True),
    'RIDER_ORC': load_anim("assets/animations/Mobs/rider_orc/Orc rider.png", 'mobs', 'rider_orc', True),
    'ARMORED_SKELETON': load_anim("assets/animations/Mobs/armored_skeleton/Armored Skeleton.png", 'mobs', 'armored_skeleton', True),
    'GREATSWORD_SKELETON': load_anim("assets/animations/Mobs/greatsword_skeleton/Greatsword Skeleton.png", 'mobs', 'greatsword_skeleton', True),
    'SKELETON': load_anim("assets/animations/Mobs/skeleton/Skeleton.png", 'mobs', 'skeleton', True),
    'SLIME': load_anim("assets/animations/Mobs/slime/Slime.png", 'mobs', 'slime', True),
    'SMALL_SLIME': load_anim("assets/animations/Mobs/slime/Slime.png", 'mobs', 'slime', True, scale=(220, 220)),
    'WEREBEAR': load_anim("assets/animations/Mobs/werebear/Werebear.png", 'mobs', 'werebear', True),
    'WEREWOLF': load_anim("assets/animations/Mobs/werewolf/Werewolf.png", 'mobs', 'werewolf', True),
    'DIALOG_KNIGHT': load_anim("assets/animations/Troops/knight/Knight.png", 'troops', 'knight', scale=(1700, 1700))
}
