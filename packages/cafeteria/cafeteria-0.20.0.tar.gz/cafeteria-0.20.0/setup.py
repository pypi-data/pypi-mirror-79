# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cafeteria',
 'cafeteria.abc',
 'cafeteria.datastructs',
 'cafeteria.datastructs.units',
 'cafeteria.decorators',
 'cafeteria.logging',
 'cafeteria.patterns',
 'cafeteria.patterns.context',
 'cafeteria.twisted']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=3.13,<6.0']

setup_kwargs = {
    'name': 'cafeteria',
    'version': '0.20.0',
    'description': 'Cafeteria: A convenience package providing various building blocks enabling pythonic patterns.',
    'long_description': '|pypi| |travis| |black| |dependabot|\n\nPython Cafeteria Package\n========================\n\nA convenience package providing various building blocks for pythonic patterns.\n\n\n.. |pypi| image:: https://badge.fury.io/py/cafeteria.svg\n    :target: https://badge.fury.io/py/cafeteria\n.. |travis| image:: https://travis-ci.org/abn/cafeteria.svg?branch=master\n    :target: https://travis-ci.org/abn/cafeteria\n.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/ambv/black\n.. |dependabot| image:: https://api.dependabot.com/badges/status?host=github&repo=abn/cafeteria\n    :target: https://dependabot.com\n',
    'author': 'Arun Babu Neelicattu',
    'author_email': 'arun.neelicattu@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/abn/cafeteria',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
