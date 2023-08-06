# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyfacebook',
 'pyfacebook.api',
 'pyfacebook.models',
 'pyfacebook.utils',
 'tests',
 'tests.facebook',
 'tests.facebook.apis',
 'tests.facebook.models',
 'tests.instagram',
 'tests.instagram.basic_apis',
 'tests.instagram.pro_apis',
 'tests.utils']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=20.1.0,<21.0.0',
 'cattrs>=1.0.0,<2.0.0',
 'requests-oauthlib>=1.3.0,<2.0.0',
 'requests>=2.24.0,<3.0.0',
 'responses>=0.11.0,<0.12.0']

setup_kwargs = {
    'name': 'python-facebook-api',
    'version': '0.7.0',
    'description': 'A Python wrapper around the Facebook Graph API',
    'long_description': None,
    'author': 'Ikaros kun',
    'author_email': 'merle.liukun@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sns-sdks/python-facebook',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*',
}


setup(**setup_kwargs)
