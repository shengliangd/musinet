"""
map values to [0,1]
"""


epsl = 1e-4


def map_pitch(x):
    return max(x, 0)


def unmap_pitch(x):
    if x == 0:
        return -2147483648
    return x


def map_dynamic(x):
    return x


def unmap_dynamic(x):
    return x


def map_rhythm(x):
    return int(x*1e4)


def unmap_rhythm(x):
    return x/1e4


def map_duration(x):
    return int(x*1e4)


def unmap_duration(x):
    return x/1e4


'''
import math


def map_pitch(x):
    if x <= 0:
        return 0
    return 1/(1+math.exp(-(x-58)/12))


def unmap_pitch(x):
    if x <= epsl:
        return 0
    x = min(x, 1-epsl)
    return int(58-12*math.log(1/x-1))


def map_dynamic(x):
    if x == 0:
        return 0
    return 1/(1+math.exp(-(x-75)/16))


def unmap_dynamic(x):
    if x <= epsl:
        return 0
    x = min(x, 1-epsl)
    return int(75-16*math.log(1/x-1))


def map_rhythm(x):
    if x == 0:
        return 0.0
    return min(1, math.log2(x*200)/math.log2(800))


def unmap_rhythm(x):
    if x < epsl:
        return 0
    return (800**x)/200


def map_duration(x):
    if x == 0:
        return 0.0
    return min(math.log2(x*50)/math.log2(500), 1)


def unmap_duration(x):
    if x < epsl:
        return 0
    return (500**x)/50


def map_pitch(x):
    x = x-20
    x = max(x, 0)
    x = min(x, 100)
    return x


def unmap_pitch(x):
    if x == 0:
        return -2147483648
    return int(x+20)


def map_dynamic(x):
    if x > epsl:
        x = 1/(1+math.exp(-(x-75)/16))
    return int(x*100)


def unmap_dynamic(x):
    x = x/100
    if x > epsl:
        return int(75-16*math.log(1/x-1))
    return 0


def map_rhythm(x):
    if x > epsl:
        x = math.log(x*200, 800)
    x = min(int(x*100), 100)
    x = max(0, x)
    return x


def unmap_rhythm(x):
    x = x/100
    if x < epsl:
        return 0
    return (800**x)/200


def map_duration(x):
    if x > epsl:
        x = math.log(x*50, 500)
    x = min(int(x*100), 100)
    x = max(0, x)
    return x


def unmap_duration(x):
    x = x/100
    if x < epsl:
        return 0
    return (500**x)/50
'''
