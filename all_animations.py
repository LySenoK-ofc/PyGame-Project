from load_animation_func import load_anim

ANIMATIONS = {
    'ARCHER': load_anim("assets/animations/Troops/archer/Archer.png", 'troops', 'archer'),
    'KNIGHT': load_anim("assets/animations/Troops/knight/Knight.png", 'troops', 'knight'),
    'LANCER': load_anim("assets/animations/Troops/lancer/Lancer.png", 'troops', 'lancer', scale=(230, 230)),
    'WIZARD': load_anim("assets/animations/Troops/wizard/Wizard.png", 'troops', 'wizard'),
    'PRIEST': load_anim("assets/animations/Troops/priest/Priest.png", 'troops', 'priest'),
    'ARROW01': load_anim("assets/animations/Troops/arrows/Arrow01(100x100).png", 'arrows', 'arrow01', scale=(230, 230)),
    'ORC': load_anim("assets/animations/Orcs/orc/Orc.png", 'orcs', 'orc', True)
}
