# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['uncolor']

package_data = \
{'': ['*']}

install_requires = \
['pytest-datadir>=1.3.1,<2.0.0']

entry_points = \
{'console_scripts': ['uncolor = uncolor:uncolor']}

setup_kwargs = {
    'name': 'uncolor',
    'version': '0.1.0',
    'description': 'strips ANSI colors from a data stream',
    'long_description': None,
    'author': 'Ryan Delaney',
    'author_email': 'ryan.patrick.delaney@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
