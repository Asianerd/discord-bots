import pickle
import random
from PIL import Image


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


"""Image-related formatting"""


def resize_image(image, new_width=100):
    width, height = image.size
    ratio = height / width / 1.65
    new_height = int(new_width * ratio)
    return image.resize((new_width, new_height))


def pixels_to_ascii(image):
    ascii_characters = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]
    ascii_characters.reverse()
    return "".join([ascii_characters[pixel // 25] for pixel in image.getdata()])


def convert_pixels_to_ascii(): # This is the main function, use this
    to_ascii_path = "_.ajuna - ToAscii.png"
    image = Image.open(to_ascii_path)
    new_image_data = pixels_to_ascii(resize_image(image).convert("L"))
    pixel_count = len(new_image_data)
    ascii_image = "\n".join([new_image_data[index:(index + 100)] for index in range(0, pixel_count, 100)])
    return ascii_image
