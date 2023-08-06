# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['silhouette']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'silhouette',
    'version': '0.0.1a0',
    'description': '',
    'long_description': None,
    'author': 'tnahs',
    'author_email': '31777797+tnahs@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
