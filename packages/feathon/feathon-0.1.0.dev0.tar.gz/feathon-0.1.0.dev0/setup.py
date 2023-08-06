# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['feathon']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0', 'mxu>=0.0.6,<0.0.7']

setup_kwargs = {
    'name': 'feathon',
    'version': '0.1.0.dev0',
    'description': 'The Python feature toolbox.',
    'long_description': '# Feathon\n\nThe Python feature toolbox.\n',
    'author': 'Maximilian Köhl',
    'author_email': 'koehl@cs.uni-saarland.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
