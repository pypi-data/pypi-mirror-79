# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['openstates_metadata', 'openstates_metadata.data', 'openstates_metadata.tests']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=19.3,<20.0']

setup_kwargs = {
    'name': 'openstates-metadata',
    'version': '2020.9.1',
    'description': 'metadata for the openstates project',
    'long_description': "# openstates-metadata\n\nThis package is obsolete, please install 'openstates' instead and change your imports to openstates.metadata.\n\n",
    'author': 'James Turk',
    'author_email': 'james@openstates.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/openstates/metadata',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
