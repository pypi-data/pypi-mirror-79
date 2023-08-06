# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyhackasm']

package_data = \
{'': ['*']}

install_requires = \
['typer[all]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['pyasm = pyhackasm.cli:cli']}

setup_kwargs = {
    'name': 'pyhackasm',
    'version': '0.1.1',
    'description': 'Assembler for Hack ASM written in Python 3',
    'long_description': '# Assembler - Hack ASM\n\n[![DeepSource](https://static.deepsource.io/deepsource-badge-light-mini.svg)](https://deepsource.io/gh/volf52/nand2tetris-assembler-python/?ref=repository-badge)\n\n[Project 6](https://www.nand2tetris.org/project06) for the [Nand2Tetris](https://www.nand2tetris.org/) course(?)\n',
    'author': 'Arslan',
    'author_email': 'rslnkrmt2552@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
