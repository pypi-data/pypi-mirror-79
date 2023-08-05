# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asgi_cable', 'asgi_cable.contrib', 'asgi_cable.contrib.django']

package_data = \
{'': ['*'], 'asgi_cable': ['static/wire/*']}

setup_kwargs = {
    'name': 'asgi-cable',
    'version': '0.1.0',
    'description': 'A framework for the real-time ASGI apps.',
    'long_description': None,
    'author': 'Alex Oleshkevich',
    'author_email': 'alex.oleshkevich@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
