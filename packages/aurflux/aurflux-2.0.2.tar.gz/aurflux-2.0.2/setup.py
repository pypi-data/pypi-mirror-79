# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aurflux', 'aurflux.command']

package_data = \
{'': ['*']}

install_requires = \
['aurcore', 'discord.py', 'loguru>=0.5.2,<0.6.0', 'pyyaml']

setup_kwargs = {
    'name': 'aurflux',
    'version': '2.0.2',
    'description': 'Aurflux!',
    'long_description': None,
    'author': 'Zenith',
    'author_email': 'inbox@zenith.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
