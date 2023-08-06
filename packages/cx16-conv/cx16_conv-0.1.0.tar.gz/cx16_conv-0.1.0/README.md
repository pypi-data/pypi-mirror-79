# cx16-conv

Conversion utilities for the Commander X16.

Currently supported conversions:
 - Graphics
 - Palettes

## Installation

Requires Python 3.8 or later.

    pip install cx16_conv

## Usage

### Generating a palette

    cx16-conv pal generate <image> <palette_file>

This command will extract all colors from the given image and save them to the
palette file.

 - If the palette file already exists, new colors will be added as needed.
 - If the palette file does not already exist, an empty palette is created

### Exporting a palette

    cx16-conv pal export [-p palette_file] [-f format_spec] <output file> <symbol name>

Converts a palette file to various supported formats:
  - `C-array` (default)
  - `GPL` (GIMP-formatted palette file)

If no palette file is specified, the system default palette is used.

### Converting graphics

    cx16-conv gfx [-p palette_file] [-f format] <image file> <output file> <symbol name>

Converts an image file to various supported formats:
  - `C-array` (default)

If no palette file is specified, the system default palette is used.
