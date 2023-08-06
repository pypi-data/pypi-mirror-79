# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nornir_tests',
 'nornir_tests.plugins',
 'nornir_tests.plugins.processors',
 'nornir_tests.plugins.tasks',
 'nornir_tests.plugins.tests']

package_data = \
{'': ['*']}

install_requires = \
['assertpy>=1.1,<2.0',
 'jsonpath-ng>=1.5.2,<2.0.0',
 'lxml>=4.5.2,<5.0.0',
 'nornir']

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.7,<0.8']}

setup_kwargs = {
    'name': 'nornir-tests',
    'version': '0.1.0a6',
    'description': '',
    'long_description': None,
    'author': 'Patrick Avery',
    'author_email': 'patrickdaj@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<3.7',
}


setup(**setup_kwargs)
