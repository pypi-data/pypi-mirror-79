# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['rabbitmqrun']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['rabbitmqrun = rabbitmqrun.cli:run']}

setup_kwargs = {
    'name': 'rabbitmqrun',
    'version': '0.1.1',
    'description': 'A package rabbitmqrun',
    'long_description': None,
    'author': 'Mayron Ceccon',
    'author_email': 'mayron.ceccon@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mayronceccon',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
