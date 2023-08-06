# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['virtualcandy']

package_data = \
{'': ['*'], 'virtualcandy': ['lib/*', 'lib/tmpl/*']}

install_requires = \
['flake8>=3.8.3,<4.0.0', 'pip>=20.1.1,<21.0.0']

setup_kwargs = {
    'name': 'virtualcandy',
    'version': '3.0.1',
    'description': 'Virtualcandy provides Virtualenv_ integration with your Bash or Zsh shell',
    'long_description': None,
    'author': 'Jeff Buttars',
    'author_email': 'jeffbuttars@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
