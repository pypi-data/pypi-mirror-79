# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['matroska_cache', 'matroska_cache.backends', 'matroska_cache.dep']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'matroska-cache',
    'version': '0.1.1',
    'description': 'Caching with dependency tracking',
    'long_description': None,
    'author': 'Mark Vartanyan',
    'author_email': 'kolypto@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kolypto/py-matroska_cache',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
