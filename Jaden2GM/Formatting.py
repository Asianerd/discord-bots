import discord
from discord.ext import commands
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


def dynamic_color(i):  # too lazy to rename to the bri'ish colour
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


def beautify_dict(d, indent=0):
    final = ''
    for key, value in d.items():
        final += '\t' * indent + str(key)
        if isinstance(value, dict):
            beautify_dict(value, indent+1)
        else:
            final += '\t' * (indent+1) + str(value)
    return final


def find_argument(message: str):
    """
    0: content
    1: amount
    """
    amount = 1
    final = []
    for x in message.split(" "):
        if x.isdigit():
            try:
                amount = int(x)
            except ValueError:
                pass
        else:
            final.append(x)
    return [' '.join(final[1:]), amount]


def progress_bar(percent, t, empty='f'):
    """
    :param percent: in float; 0.0 - 1.0
    :param fill:
    :param empty:
    """

    # <:f1:959690089930321940>
    # <:f2:959690089678659626>
    # <:f3:959690089913516112>

    # <:h1: 959690112290160720 >
    # <:h2: 959690112315305984 >
    # <:h3: 959690112512454656 >
    # <:s1: 959690112420155432 >
    # <:s2: 959690112327901224 >
    # <:s3: 959690112353075220 >
    # <:m1: 959690112390803486 >
    # <:m2: 959690112428572672 >
    # <:m3: 959690112348868619 >

    fill = {
        'f': [
            '<:f1:959690089930321940>',
            '<:f2:959690089678659626>',
            '<:f3:959690089913516112>'
        ],
        'h': [
            '<:h1:959690112290160720>',
            '<:h2:959690112315305984>',
            '<:h3:959690112512454656>'
        ],
        's': [
            '<:s1:959690112420155432>',
            '<:s2:959690112327901224>',
            '<:s3:959690112353075220>'
        ],
        'm': [
            '<:m1:959690112390803486>',
            '<:m2:959690112428572672>',
            '<:m3:959690112348868619>'
        ]
    }
    p = 1.0 if percent > 1.0 else percent
    # final = [fill[t][1]] * round(p * 10)
    # final += [fill[empty][1]] * (10-len(final))
    final = [t] * round(p * 10)
    final += [empty] * (10 - len(final))
    _t = []
    for index, x in enumerate(final):
        i = 1
        if index == 0:
            i = 0
        elif index == 9:
            i = 2
        _t.append(fill[x][i])

    return ''.join(_t)
