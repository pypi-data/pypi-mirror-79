# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['srupy']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'srupy',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'Andreas Lüschow',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
