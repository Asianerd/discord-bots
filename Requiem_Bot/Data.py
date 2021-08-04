from pathlib import Path
import pickle
import random

command_prefix = ":"
author_id = 517998886141558786
save_file_path = Path(".") / "Requiem_Data"
disposable_messages = []

reactions = ["\N{WASTEBASKET}"]

stand_roles = {
    'ger': [719240102043451484,""],
    'sp': [719215347223494680,""],
    'kcr': [719240103314194473,""],
    'sptw': [719240107902763030,""],
    'sc': [719215343498690682,""],
    'kqbtd': [719240106187292732,""],
    'scr': [719240104559771710,""],
    'mr': [719215345109565450,""],
    'hg': [719215340617465947,""],
    '6p': [719215353338658906,""],
    'tw': [719215349278441472,""],
    'twau': [732814956042518538,""],
    'th': [719215349857255494,""],
    'aero': [719215354546487326,""],
    'cd': [719215351312678913,""],
    'mp': [719215360263323720,""],
    'bb': [719215363400794182,""],
    'sf': [719215358476550224,""],
    'wa': [719215364621205571,""],
    'ph': [719215361928462416,""],
    'kq': [719215352260853790,""],
    'sm': [732815302727041137,""],
    'ge': [719215357000286300,""],
    'tusk': [755050971142553610,""],
    'd4c': [732815147810160683,""],
    'hp': [725008534550609951,""],
    'anubis': [838387420701523998,""],
    'kc': [719215355817361458,""],
    'd4clt': [732815499112611890,""],
    'cream': [719215346325913600,""],
    'ws': [769793466343096331,""],
    'cmoon': [785526380472696862,""],
    'mih': [807125974898573333,""],
    'twoh': [807125980137259008,""],
    'rhcp': [872144129151340544,""]
}


def save():
    pass


def load():
    pass


# Formatting stuff
def colour(_random=False):
    if _random:
        return random.randint(0x100000, 0xFFFFFF)
    else:
        #9708fc

        #R 9895936
        #G 2048
        #B 252

        #9898236

        return 9898236


def get_ping_colour(_i):
    _min = 0
    _max = 500
    _percent = (_i - _min) / _max - _min
    _r = (_max+10) * _percent
    _g = (_max+10) * (1 - _percent)
    if _r > 255:
        _r = 255
    elif _r < 0:
        _r = 0
    if _g > 255:
        _g = 255
    elif _g < 0:
        _g = 0
    return _r, _g


def dynamic_color(i):
    """Enter a float from 0-1 and will return red and green values accordingly,
    with 0 being fully green and 1 being fully red"""
    r = 255 * i
    g = 255 * (1 - i)

    if r > 255:
        r = 255
    elif r < 0:
        r = 0

    if g > 255:
        g = 255
    elif g < 0:
        g = 0

    return int(r), int(g)


def uptime_string(enoch_time):
    if enoch_time > 3600:
        hour = enoch_time // 3600
        minute = (enoch_time / 60) - (int(hour) * 60)
        return f"{int(hour)}h {int(minute)}m"
    else:
        minute = enoch_time / 60
        second = enoch_time - (int(minute) * 60)
        return f"{int(minute)}m {int(second)}s"
