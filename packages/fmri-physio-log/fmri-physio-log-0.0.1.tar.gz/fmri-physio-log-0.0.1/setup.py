# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fmri_physio_log']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.2,<2.0.0']

setup_kwargs = {
    'name': 'fmri-physio-log',
    'version': '0.0.1',
    'description': 'Load fMRI PMU files into python',
    'long_description': None,
    'author': 'Andrew Ross',
    'author_email': 'andrew.ross.mail@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
