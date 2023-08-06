# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sudoku', 'sudoku.examples', 'sudoku.test']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.1,<2.0.0']

entry_points = \
{'console_scripts': ['sudoku-tools = console:main']}

setup_kwargs = {
    'name': 'sudoku-tools',
    'version': '0.0.1',
    'description': '',
    'long_description': '# `sudoku-tools`\n\n[![](https://img.shields.io/pypi/v/sudoku-tools.svg?style=flat)](https://pypi.org/pypi/sudoku-tools/)\n[![](https://img.shields.io/pypi/dw/sudoku-tools.svg?style=flat)](https://pypi.org/pypi/sudoku-tools/)\n[![](https://img.shields.io/pypi/pyversions/sudoku-tools.svg?style=flat)](https://pypi.org/pypi/sudoku-tools/)\n[![](https://img.shields.io/pypi/format/sudoku-tools.svg?style=flat)](https://pypi.org/pypi/sudoku-tools/)\n[![](https://img.shields.io/pypi/l/sudoku-tools.svg?style=flat)](https://github.com/dawsonbooth/sudoku-tools/blob/master/LICENSE)\n\n## Description\n\nThis Python package is a collection of useful tools for generating, grading, solving, and transforming sudoku puzzles.\n\nThis package is very incomplete and should not be expected to solve or rate complicated sudoku puzzles. Only a few simple strategies are currently implemented. That said, transformations (rotate, reflect, shuffle) and conversions (to/from string, 1D array, 2D array) should be fully functional.\n\nPlease feel free to contribute and implement more [strategies](https://www.sudocue.net/guide.php) or add to the documentation if you would like to see this package progress more quickly.\n\n## Installation\n\nWith [Python](https://www.python.org/downloads/) installed, simply run the following command to add the package to your project.\n\n```bash\npip install sudoku-tools\n```\n\n## Usage\n\nThe object can be constructed with a 1-dimensional board:\n\n```python\narr_1d = [1, 0, 3, 4, 0, 4, 1, 0, 0, 3, 0, 1, 4, 0, 2, 3]\npuzzle = Puzzle(arr_1d, 0)\n```\n... or with a 2-dimensional board:\n\n```python\narr_2d = [[1, 0, 3, 4],\n\t[0, 4, 1, 0],\n\t[0, 3, 0, 1],\n\t[4, 0, 2, 3]]\npuzzle = Puzzle(arr_2d, 0)\n```\n\nFeel free to [check out the docs](https://dawsonbooth.github.io/sudoku-tools/) for more information.\n\n## License\n\nThis software is released under the terms of [MIT license](LICENSE).\n',
    'author': 'Dawson Booth',
    'author_email': 'pypi@dawsonbooth.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dawsonbooth/sudoku-tools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
