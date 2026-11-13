# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/thumbor/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com thumbor@googlegroups.com

from io import BytesIO

from PIL import Image

from thumbor.config import Config
from thumbor.context import Context
from thumbor.engines.pil import Engine

SIZE = 40
TRANSPARENT_INDEX = 0


def make_palette_gif():
    image = Image.new("P", (SIZE, SIZE), TRANSPARENT_INDEX)
    image.putpalette([0, 0, 0, 0, 0, 255] + [0, 0, 0] * 254)
    for x in range(10, 30):
        for y in range(10, 30):
            image.putpixel((x, y), 1)
    buffer = BytesIO()
    image.save(buffer, "GIF", transparency=TRANSPARENT_INDEX)
    return buffer.getvalue()


def test_resized_palette_gif_keeps_its_transparency_index():
    config = Config(
        ALLOW_ANIMATED_GIFS=False, PILLOW_PRESERVE_INDEXED_MODE=True
    )
    engine = Engine(Context(config=config))
    engine.load(make_palette_gif(), ".gif")

    engine.resize(SIZE // 2, SIZE // 2)
    output = Image.open(BytesIO(engine.read(".gif")))

    assert "transparency" in output.info, (
        "resized GIF has no transparency index; the transparent "
        "background is now opaque"
    )
