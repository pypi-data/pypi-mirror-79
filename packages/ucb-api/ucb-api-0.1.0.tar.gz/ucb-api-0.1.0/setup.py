# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ucb_api',
 'ucb_api.api',
 'ucb_api.models',
 'ucb_api.python_client',
 'ucb_api.python_client.swagger_client',
 'ucb_api.python_client.swagger_client.api',
 'ucb_api.python_client.swagger_client.models',
 'ucb_api.python_client.test']

package_data = \
{'': ['*'], 'ucb_api.python_client': ['.swagger-codegen/*', 'docs/*']}

install_requires = \
['certifi>=2020.6.20,<2021.0.0',
 'pylint>=2.6.0,<3.0.0',
 'python_dateutil>=2.8.1,<3.0.0',
 'six>=1.15.0,<2.0.0',
 'typer[all]>=0.3.2,<0.4.0',
 'urllib3>=1.25.10,<2.0.0']

entry_points = \
{'console_scripts': ['ucb-api = ucb_api.main:app']}

setup_kwargs = {
    'name': 'ucb-api',
    'version': '0.1.0',
    'description': 'Python package for Unity Cloud Build api',
    'long_description': '# Unity Cloud Build Python Api\n\nPython package for Unity Cloud Build api.\n',
    'author': 'leynier',
    'author_email': 'leynier41@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
