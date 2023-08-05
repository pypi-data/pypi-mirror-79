# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['drf_api_checker']

package_data = \
{'': ['*']}

install_requires = \
['django', 'djangorestframework>=3.10,<4.0', 'pytz>=2019.3,<2020.0']

setup_kwargs = {
    'name': 'drf-api-checker',
    'version': '0.10.0',
    'description': '',
    'long_description': None,
    'author': 'sax',
    'author_email': 's.apostolico@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
