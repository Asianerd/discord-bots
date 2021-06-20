import pickle
import random


def colour(_random=False):
    if _random:
        return random.randint(0x100000, 0xFFFFFF)
    else:
        return 55807


def get_ping_colour(_i):
    _min = 0
    _max = 500
    _percent = (_i - _min) / _max - _min
    _r = 510 * _percent
    _g = 510 * (1 - _percent)
    if _r > 255:
        _r = 255
    if _g > 255:
        _g = 255
    return _r, _g