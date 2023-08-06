# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['perip']

package_data = \
{'': ['*']}

install_requires = \
['aosong>=0.0.2,<0.0.3']

setup_kwargs = {
    'name': 'perip',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'David J Barnes',
    'author_email': 'david@onepointone.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
