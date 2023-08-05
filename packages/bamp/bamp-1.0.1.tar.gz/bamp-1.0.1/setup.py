# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bamp', 'bamp.config', 'bamp.helpers', 'bamp.vcs']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0', 'dulwich==0.19.11', 'six>=1.14.0,<2.0.0']

setup_kwargs = {
    'name': 'bamp',
    'version': '1.0.1',
    'description': 'Bamp version according to semantic versioning',
    'long_description': None,
    'author': 'Michał Klich',
    'author_email': 'michal@klichx.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
