from Mobs import Orc, RiderOrc, EliteOrc, ArmoredOrc, Skeleton, GreateswordSkeleton, ArmoredSkeleton, Slime, Werebear, \
    Werewolf

lvls = {
    'lvl1': {
        'waves': {
            '1': [Orc] * 6,
            '2': [Orc] * 8 + [RiderOrc],
            '3': [Orc] * 7 + [RiderOrc] * 3,
            '4': [Orc] * 6 + [EliteOrc] * 4 + [ArmoredOrc] * 2,
            '5': [Orc] * 7 + [EliteOrc] * 4 + [ArmoredOrc] * 2 + [RiderOrc] * 2
        }},
    'lvl2': {
        'waves': {
            '1': [Orc] * 4 + [Skeleton] * 2,
            '2': [Orc] * 5 + [GreateswordSkeleton] * 2 + [ArmoredOrc],
            '3': [Orc] * 7 + [RiderOrc] * 3 + [ArmoredSkeleton] * 2 + [Slime] * 4,
            '4': [Orc] * 9 + [RiderOrc] * 3 + [ArmoredSkeleton] * 3 + [Slime] * 4 + [Werebear] * 2 + [Werewolf] * 2,
            '5': [Orc] * 13 + [RiderOrc] * 5 + [ArmoredSkeleton] * 5 + [Slime] * 6 + [Werebear] * 3 + [Werewolf] * 4 + [EliteOrc] * 4
        }}
}
