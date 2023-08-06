# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aurcore', 'aurcore.event', 'aurcore.util']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.5.2,<0.6.0']

setup_kwargs = {
    'name': 'aurcore',
    'version': '1.0.1',
    'description': 'Aurcore!',
    'long_description': None,
    'author': 'Zenith',
    'author_email': 'z@zenith.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>3.8',
}


setup(**setup_kwargs)
