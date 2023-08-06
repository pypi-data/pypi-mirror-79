# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_demo_xxxxyy']

package_data = \
{'': ['*']}

install_requires = \
['pendulum>=2.1.2,<3.0.0']

setup_kwargs = {
    'name': 'poetry-demo-xxxxyy',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Snow Shen',
    'author_email': 'snowshen@tagtoo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
