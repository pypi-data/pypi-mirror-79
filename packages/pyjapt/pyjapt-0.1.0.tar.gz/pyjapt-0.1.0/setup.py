# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyjapt']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyjapt',
    'version': '0.1.0',
    'description': 'Just Another Parsing Tool Writ ten in Python',
    'long_description': None,
    'author': 'Alejandro Klever',
    'author_email': 'alejandroklever4197@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
