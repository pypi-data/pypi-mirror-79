# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gnome_extension_uploader']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=6.0.2,<7.0.0', 'requests>=2.24.0,<3.0.0', 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['geu = gnome_extension_uploader.cli:app']}

setup_kwargs = {
    'name': 'gnome-extension-uploader',
    'version': '0.1.4',
    'description': 'Gnome Extension Uploader',
    'long_description': None,
    'author': 'Sebastian Noel Lübke',
    'author_email': 'sebastian@luebke.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
