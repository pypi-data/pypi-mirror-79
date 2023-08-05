# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyqueryinterafce']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyqueryinterafce',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'YutaUra',
    'author_email': 'yuuta3594@outlook.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
