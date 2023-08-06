# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nppes']

package_data = \
{'': ['*']}

install_requires = \
['Pygments>=2.6.1,<3.0.0',
 'click>=7.1.2,<8.0.0',
 'notebook>=6.0.3,<7.0.0',
 'nox>=2020.5.24,<2021.0.0',
 'pytest-mock>=3.2.0,<4.0.0',
 'requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'nppes',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Jason Turan',
    'author_email': 'jason.turan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
