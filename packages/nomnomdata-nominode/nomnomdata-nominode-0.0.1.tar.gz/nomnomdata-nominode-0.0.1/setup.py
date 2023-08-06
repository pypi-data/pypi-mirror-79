# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nomnomdata', 'nomnomdata.nominode']

package_data = \
{'': ['*']}

install_requires = \
['dunamai>=1.1.0,<2.0.0', 'nomnomdata-cli>=0.1.3,<0.2.0']

entry_points = \
{'nomnomdata.cli_plugins': ['nominode = nomnomdata.nominode.cli:cli']}

setup_kwargs = {
    'name': 'nomnomdata-nominode',
    'version': '0.0.1',
    'description': 'Package containing tooling for interacting with nominodes',
    'long_description': '# nomnomdata-nominode\n\nCLI Project for interacting with nominode api',
    'author': 'Nom Nom Data Inc',
    'author_email': 'info@nomnomdata.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/nomnomdata/tools/nomnomdata-nominode',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
