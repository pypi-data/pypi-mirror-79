from typing import List

from PIL import Image

from .palette import Color, Palette


def image_to_bytes(image_path: str, palette: Palette) -> bytes:
    return b"".join(
        [
            index.to_bytes(1, "little")
            for index in lookup_image_indices(image_path, palette)
        ]
    )


def lookup_image_indices(path: str, palette: Palette) -> List[int]:
    indices = []
    image = Image.open(path)
    for (red, green, blue, alpha) in _iterate_colors(image):
        if alpha == 0:
            indices.append(0)
        else:
            color = Color(red=red, green=green, blue=blue)
            indices.append(palette.index_by_color[color])
    return indices


def extend_palette_from_image(path: str, palette: Palette):
    image = Image.open(path)
    for (red, green, blue, alpha) in _iterate_colors(image):
        if alpha == 0:
            continue
        color = Color(red=red, green=green, blue=blue)

        if color not in palette.index_by_color:
            next_index = len(palette.colors)
            palette.colors.append(color)
            palette.index_by_color[color] = next_index
            if next_index > 255:
                raise RuntimeError(
                    "Too many colors in the source image, palette is full"
                )


def _get_color(image, x, y):
    pixel = image.getpixel((x, y))
    if len(pixel) == 3:
        return (pixel[0], pixel[1], pixel[2], 255)
    elif len(pixel) == 4:
        return pixel
    else:
        raise NotImplementedError(f"Channel depth of {len(pixel)}")


def _iterate_colors(image):
    (width, height) = image.size
    for y in range(0, height):
        for x in range(0, width):
            yield _get_color(image, x, y)
