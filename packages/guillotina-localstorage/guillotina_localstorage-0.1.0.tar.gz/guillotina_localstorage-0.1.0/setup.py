# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['guillotina_localstorage', 'guillotina_localstorage.tests']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=0.5.0,<0.6.0', 'guillotina>5.3.48']

setup_kwargs = {
    'name': 'guillotina-localstorage',
    'version': '0.1.0',
    'description': 'Local FS storage support for Guillotina',
    'long_description': None,
    'author': 'Jordi Masip',
    'author_email': 'jordi@masip.cat',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
