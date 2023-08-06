# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['servergrimoire', 'servergrimoire.operation', 'servergrimoire.script']

package_data = \
{'': ['*']}

install_requires = \
['Click>=7.1.2,<8.0.0',
 'dnspython>=2.0.0,<3.0.0',
 'pyOpenssl>=19.1.0,<20.0.0',
 'python-whois>=0.7.3,<0.8.0',
 'requests>=2.24.0,<3.0.0',
 'tabulate>=0.8.7,<0.9.0']

setup_kwargs = {
    'name': 'servergrimoire',
    'version': '1.0.0',
    'description': 'Package for record and store info about servers and their stuffs',
    'long_description': None,
    'author': 'Fundor333',
    'author_email': 'fundor333@fundor333.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
