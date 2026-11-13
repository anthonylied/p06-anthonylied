# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/thumbor/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com thumbor@googlegroups.com

from io import BytesIO
from types import SimpleNamespace

from PIL import Image

from thumbor.config import Config
from thumbor.context import Context
from thumbor.engines.pil import Engine
from thumbor.transformer import Transformer

SOURCE_SIZE = 16
BARS = [(255, 0, 0, 255), (0, 255, 0, 255), (0, 0, 255, 255), (255, 255, 0, 255)]


def make_rainbow_png():
    image = Image.new("RGBA", (SOURCE_SIZE, SOURCE_SIZE), (0, 0, 0, 0))
    for x in range(SOURCE_SIZE):
        color = BARS[x * len(BARS) // SOURCE_SIZE]
        for y in range(SOURCE_SIZE):
            image.putpixel((x, y), color)
    buffer = BytesIO()
    image.save(buffer, "PNG")
    return buffer.getvalue()


def test_very_wide_short_resize_keeps_the_picture():
    config = Config()
    engine = Engine(Context(config=config))
    engine.load(make_rainbow_png(), ".png")

    request = SimpleNamespace(
        engine=engine,
        width=800,
        height=20,
        fit_in=False,
        full=False,
        adaptive=False,
        stretch=False,
        should_crop=False,
        focal_points=[],
        halign="center",
        valign="middle",
        debug=False,
        horizontal_flip=False,
        vertical_flip=False,
        filters="",
    )
    context = SimpleNamespace(request=request, config=config)

    Transformer(context).img_operation_worker()

    assert engine.size == (800, 20)
    most_opaque = engine.image.convert("RGBA").getchannel("A").getextrema()[1]
    assert most_opaque > 0, (
        "the 800x20 result is fully transparent; the picture was lost "
        "when it was cropped to zero height"
    )
