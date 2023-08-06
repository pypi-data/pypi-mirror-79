# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['davidjbarnes_init']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['dev = davidjbarnes_init.index:main']}

setup_kwargs = {
    'name': 'davidjbarnes-init',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'davidjbarnes',
    'author_email': 'david@onepointone.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
