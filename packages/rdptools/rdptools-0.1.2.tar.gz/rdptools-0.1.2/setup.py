# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rdptools']

package_data = \
{'': ['*']}

install_requires = \
['Office365-REST-Python-Client==2.2.0', 'pandas']

setup_kwargs = {
    'name': 'rdptools',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'Baiyue Cao',
    'author_email': 'caobaiyue@live.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.0.0,<4.0.0',
}


setup(**setup_kwargs)
