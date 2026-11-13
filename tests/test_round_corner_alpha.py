# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/thumbor/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com thumbor@googlegroups.com

from thumbor.ext.filters import _round_corner

WIDTH = 100
HEIGHT = 100
RADIUS = 30
ORIGINAL = (200, 100, 50)


def test_transparent_round_corner_keeps_original_color_on_the_edge():
    pixel = bytes(ORIGINAL) + bytes([255])
    data = pixel * (WIDTH * HEIGHT)

    result = _round_corner.apply(
        1,
        "RGBA",
        RADIUS,
        RADIUS,
        255,
        255,
        255,
        WIDTH,
        HEIGHT,
        data,
        1,
    )

    pixels = [tuple(result[i : i + 4]) for i in range(0, len(result), 4)]
    darkened = [
        pixel for pixel in pixels if pixel[3] > 0 and pixel[:3] != ORIGINAL
    ]

    assert not darkened, (
        f"{len(darkened)} visible edge pixels lost their original color, "
        f"for example {darkened[0]}"
    )
