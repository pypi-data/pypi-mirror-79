# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cx16_conv']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=7.2.0,<8.0.0', 'click>=7.1.2,<8.0.0']

entry_points = \
{'console_scripts': ['cx16-conv = cx16_conv.cli:common']}

setup_kwargs = {
    'name': 'cx16-conv',
    'version': '0.1.0',
    'description': 'Conversion utilities for the Commander x16',
    'long_description': '# cx16-conv\n\nConversion utilities for the Commander X16.\n\nCurrently supported conversions:\n - Graphics\n - Palettes\n\n## Installation\n\nRequires Python 3.8 or later.\n\n    pip install cx16_conv\n\n## Usage\n\n### Generating a palette\n\n    cx16-conv pal generate <image> <palette_file>\n\nThis command will extract all colors from the given image and save them to the\npalette file.\n\n - If the palette file already exists, new colors will be added as needed.\n - If the palette file does not already exist, an empty palette is created\n\n### Exporting a palette\n\n    cx16-conv pal export [-p palette_file] [-f format_spec] <output file> <symbol name>\n\nConverts a palette file to various supported formats:\n  - `C-array` (default)\n  - `GPL` (GIMP-formatted palette file)\n\nIf no palette file is specified, the system default palette is used.\n\n### Converting graphics\n\n    cx16-conv gfx [-p palette_file] [-f format] <image file> <output file> <symbol name>\n\nConverts an image file to various supported formats:\n  - `C-array` (default)\n\nIf no palette file is specified, the system default palette is used.\n',
    'author': 'Jennifer Wilcox',
    'author_email': 'jennifer@nitori.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Nitori-/cx16_conv',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
