# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nornir_netmiko', 'nornir_netmiko.connections', 'nornir_netmiko.tasks']

package_data = \
{'': ['*']}

install_requires = \
['netmiko>=3.1.0,<4.0.0']

entry_points = \
{'nornir.plugins.connections': ['netmiko = nornir_netmiko.connections:Netmiko']}

setup_kwargs = {
    'name': 'nornir-netmiko',
    'version': '0.1.1',
    'description': "Netmiko's plugins for nornir",
    'long_description': None,
    'author': 'Kirk Byers',
    'author_email': 'ktbyers@twb-tech.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
