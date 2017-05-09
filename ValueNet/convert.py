"""convert pitch, dynamic, rhythm, duration
    convert pitch, dynamic, rhythm, duration to [0-1]
"""


import math


__epsl = 1e-4


def convert_pitch(x):
    if x <= 0:
        return 0
    return 1/(1+math.exp(-(x-58)/12))


def deconvert_pitch(x):
    if x <= __epsl:
        return 0
    x = min(x, 1 - __epsl)
    return int(58-12*math.log(1/x-1))


def convert_dynamic(x):
    if x == 0:
        return 0
    return 1/(1+math.exp(-(x-75)/16))


def deconvert_dynamic(x):
    if x <= __epsl:
        return 0
    x = min(x, 1 - __epsl)
    return int(75-16*math.log(1/x-1))


def convert_rhythm(x):
    if x == 0:
        return 0.0
    return min(1, math.log2(x*200)/math.log2(800))


def deconvert_rhythm(x):
    if x < __epsl:
        return 0
    return (800**x)/200


def convert_duration(x):
    if x == 0:
        return 0.0
    return min(math.log2(x*50)/math.log2(500), 1)


def deconvert_duration(x):
    if x < __epsl:
        return 0
    return (500**x)/50

