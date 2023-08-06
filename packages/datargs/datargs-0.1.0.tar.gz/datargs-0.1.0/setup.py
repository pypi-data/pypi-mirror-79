# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datargs', 'datargs.compat']

package_data = \
{'': ['*']}

extras_require = \
{':python_version == "3.6"': ['dataclasses>=0.6,<0.7'],
 'attrs': ['attrs>=20.2.0,<21.0.0']}

setup_kwargs = {
    'name': 'datargs',
    'version': '0.1.0',
    'description': 'Declerative, type-safe command line argument parsers from dataclasses and attrs classes',
    'long_description': None,
    'author': 'Roee Nizan',
    'author_email': 'roeen30@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
