# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hubitatmaker', 'hubitatmaker.tests']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6.2,<4.0.0', 'getmac>=0.8.2,<0.9.0']

entry_points = \
{'console_scripts': ['init = scripts:init',
                     'publish = scripts:publish',
                     'test = scripts:test']}

setup_kwargs = {
    'name': 'hubitatmaker',
    'version': '0.3.11',
    'description': 'A library for interfacing with Hubitat via its Maker API',
    'long_description': None,
    'author': 'Jason Cheatham',
    'author_email': 'jason@jasoncheatham.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.7,<4.0.0',
}


setup(**setup_kwargs)
