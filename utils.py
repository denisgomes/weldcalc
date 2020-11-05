"""Some handy utility functions"""

from itertools import zip_longest


def rgb_2_hex_color(rgb):
    return '#%02x%02x%02x' % rgb


def hex_2_rgb_color(hex):
    rgb = []
    for hexclr in grouper(hex.lstrip("#"), 2):
        rgb.append(int(hexclr, 16))

    return tuple(rgb)


def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)
