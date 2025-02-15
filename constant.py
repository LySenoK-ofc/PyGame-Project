CELL_SIZE = 75
FPS = 30
WIDTH_CELL = 6
HEIGHT_CELL = 5

TOP = 75 * 4
LEFT = 75 * 6

WIDTH, HEIGHT = 1500, 825

CURRENT_LVL = 'lvl1'
WAVES = {
    'lvl1': [
        {'enemies': [
            ('Orc', 2),
            ('Skeleton', 2),
            ('Slime', 1)
        ],
            'interval': 4000},
        {'enemies': [
            ('EliteOrc', 1),
            ('RiderOrc', 1),
            ('ArmoredOrc', 1),
            ('GreateswordSkeleton', 1),
            ('ArmoredSkeleton', 1)
        ],
            'interval': 5000},
        {'enemies': [
            ('Werebear', 1),
            ('Werewolf', 1)
        ],
            'interval': 6000}
    ],
    'lvl2': [
        {'enemies': [
            ('Orc', 5),
            ('Skeleton', 4),
            ('Slime', 2)
        ],
            'interval': 2000},
        {'enemies': [
            ('Orc', 6),
            ('Skeleton', 5),
            ('EliteOrc', 2),
            ('RiderOrc', 2),
            ('Slime', 3)
        ],
            'interval': 2500},
        {'enemies': [
            ('Orc', 6),
            ('Skeleton', 6),
            ('EliteOrc', 2),
            ('RiderOrc', 3),
            ('ArmoredOrc', 3),
            ('Slime', 3)
        ],
            'interval': 3000},
        {'enemies': [
            ('Orc', 6),
            ('Skeleton', 6),
            ('EliteOrc', 2),
            ('RiderOrc', 3),
            ('ArmoredOrc', 3),
            ('Werebear', 2),
            ('Werewolf', 2),
            ('Slime', 4)
        ],
            'interval': 3000},
        {'enemies': [
            ('Orc', 6),
            ('Skeleton', 6),
            ('EliteOrc', 2),
            ('RiderOrc', 3),
            ('ArmoredOrc', 3),
            ('Werebear', 2),
            ('Werewolf', 2),
            ('GreateswordSkeleton', 2),
        ],
            'interval': 2500},
        {'enemies': [
            ('Orc', 8),
            ('Skeleton', 8),
            ('EliteOrc', 3),
            ('RiderOrc', 4),
            ('ArmoredOrc', 4),
            ('Werebear', 3),
            ('Werewolf', 3),
            ('GreateswordSkeleton', 3),
            ('ArmoredSkeleton', 3),
            ('Slime', 5)
        ],
            'interval': 3500}]
}

frame_count = 0
cash = 500
hp = 5

def reset_state():
    """Сбрасываем параметры."""
    global frame_count, cash, hp
    frame_count = 0
    cash = 500
    hp = 5
