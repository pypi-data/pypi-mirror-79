# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tropic',
 'tropic.common',
 'tropic.linalg',
 'tropic.utils',
 'tropic.utils.casters',
 'tropic.utils.codecs']

package_data = \
{'': ['*']}

install_requires = \
['logzero>=1.5.0,<2.0.0', 'tabulate>=0.8.7,<0.9.0', 'tensorflow>=2.3.0,<3.0.0']

setup_kwargs = {
    'name': 'tropic',
    'version': '0.2.4',
    'description': '',
    'long_description': None,
    'author': 'skip',
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
