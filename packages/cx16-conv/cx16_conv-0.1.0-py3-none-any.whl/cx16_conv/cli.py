import os

import click

from .palette import (
    loads,
    dumps,
    DEFAULT_PALETTE,
    palette_to_bytes,
    blank_palette,
    palette_to_gpl,
)
from .image import image_to_bytes, extend_palette_from_image
from .array import convert
from .util import write_file


@click.group()
def common():
    pass


@common.group(help="Palette-related commands")
def pal():
    pass


@common.command(help="Convert graphics to VERA format")
@click.option("-p", "--palette", type=click.Path(exists=True))
@click.option("-f", "--format", type=click.Choice(["C-array"]), default="C-array")
@click.argument("input")
@click.argument("output")
@click.argument("symbol_name")
def gfx(palette, format, input, output, symbol_name):
    loaded_palette = load_palette(palette)
    bytes_ = image_to_bytes(input, loaded_palette)
    data_out = convert(format, symbol_name, bytes_)
    write_file(output, data_out)


@pal.command()
@click.option("-p", "--palette", type=click.Path(exists=True))
@click.option(
    "-f", "--format", type=click.Choice(["C-array", "GPL"]), default="C-array"
)
@click.argument("output")
@click.argument("symbol_name")
def export(palette, format, output, symbol_name):
    loaded_palette = load_palette(palette)
    if format == "GPL":
        data_out = palette_to_gpl(loaded_palette)
    else:
        bytes_ = palette_to_bytes(loaded_palette)
        data_out = convert(format, symbol_name, bytes_)
    write_file(output, data_out)


@pal.command()
@click.argument("image")
@click.argument("palette")
def generate(palette, image):
    """
    Generate palette file from an image

    If the palette file already exists, it is extended with any new colors
    found in the image.

    If the palette file does not already exist, it will be created.
    """
    if os.path.exists(palette):
        with open(palette, "r") as f:
            loaded_palette = loads(f.read())
    else:
        loaded_palette = blank_palette()
    extend_palette_from_image(image, loaded_palette)
    write_file(palette, dumps(loaded_palette))


def load_palette(palette):
    if palette is None:
        return loads(DEFAULT_PALETTE)

    with open(palette, "r") as f:
        return loads(f.read())
