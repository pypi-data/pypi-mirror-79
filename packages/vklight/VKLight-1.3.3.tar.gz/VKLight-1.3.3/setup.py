# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vklight']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'vklight',
    'version': '1.3.3',
    'description': "VKLight - Light wrapper for VK's API",
    'long_description': None,
    'author': 'Ivan',
    'author_email': 'pass@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
