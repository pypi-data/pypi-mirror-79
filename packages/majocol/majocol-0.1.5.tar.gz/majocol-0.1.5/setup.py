# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['majocol']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=7.2.0,<8.0.0', 'numpy>=1.19.1,<2.0.0', 'scikit-learn>=0.23.2,<0.24.0']

setup_kwargs = {
    'name': 'majocol',
    'version': '0.1.5',
    'description': 'pick major colors from image',
    'long_description': '<p align="center">\n  <img width="420px" src="https://raw.githubusercontent.com/suzukey/majocol/main/docs/img/majocol.png" alt=\'majocol\'>\n</p>\n\n<p align="center">\n  <em>Pick major colors from image</em>\n</p>\n\n<p align="center">\n  <a href="https://pypi.org/project/majocol/" target="_blank">\n    <img src="https://img.shields.io/pypi/v/majocol?color=blue" alt="Package version">\n  </a>\n</p>\n\n---\n\n**Documentation**:\n\n**Demo**:\n\n---\n\n# MajoCol\n\n## Requirements\n\nPython 3.6+\n\n## Installation\n\n```shell\n$ pip3 install majocol\n```\n\n## Example\n\n```python\nfrom majocol import color, convert\n\n# Using Pillow (Open local image)\nfrom PIL import Image\n\nimage = Image.open(<IMAGE_PATH>)\nimage_ndarr = convert.pillow_to_rgb_ndarr(image)\ncolors = color.pick(image_ndarr, 3)\n\n\n# Using opencv-python (Open local image)\nimport cv2\n\nimage = cv2.imread(<IMAGE_PATH>)\nimage_ndarr = convert.cv2_to_rgb_ndarr(image)\ncolors = color.pick(image_ndarr, 3)\n\n\n# Using requests (Fetch web image)\nimport requests\n\nresp = requests.get(<IMAGE_URL>)\nimage_ndarr = convert.byte_to_rgb_ndarr(resp.content)\ncolors = color.pick(image_ndarr, 3)\n```\n\n<p align="center">&mdash; \U0001fa84 &mdash;</p>\n\n<p align="center">\n  <i>MajoCol is licensed under the terms of the <a href="https://github.com/suzukey/majocol/blob/main/LICENSE">MIT license</a>.</i>\n</p>\n',
    'author': 'suzukey',
    'author_email': 'suzukey28@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/suzukey/majocol',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
