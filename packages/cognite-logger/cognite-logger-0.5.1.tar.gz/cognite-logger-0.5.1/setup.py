# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['cognite', 'cognite.logger']

package_data = \
{'': ['*']}

install_requires = \
['python-json-logger>=0.1.8,<0.2.0']

setup_kwargs = {
    'name': 'cognite-logger',
    'version': '0.5.1',
    'description': 'Library for configuring logger',
    'long_description': None,
    'author': 'Erlend Vollset',
    'author_email': 'erlend.vollset@cognite.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
