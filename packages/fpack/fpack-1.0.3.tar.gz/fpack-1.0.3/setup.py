# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fpack']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'fpack',
    'version': '1.0.3',
    'description': 'fpack is a simple message (de)seriealizer in pure python',
    'long_description': None,
    'author': 'Frank Chang',
    'author_email': 'frank@csie.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/frankurcrazy/fpack',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
