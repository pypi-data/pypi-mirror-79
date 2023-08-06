# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['steganossaurus']

package_data = \
{'': ['*']}

install_requires = \
['black>=20.8b1,<21.0',
 'click>=7.1.2,<8.0.0',
 'imageio>=2.9.0,<3.0.0',
 'matplotlib>=3.3.1,<4.0.0',
 'numpy>=1.19.1,<2.0.0',
 'scipy>=1.5.2,<2.0.0']

setup_kwargs = {
    'name': 'steganossaurus',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Joao Vitor Maia',
    'author_email': 'maia.tostring@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
