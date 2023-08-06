# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tblastn_wrapper', 'tblastn_wrapper.rhymes']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['tblastn_wrapper = tblastn_wrapper.__main__:main']}

setup_kwargs = {
    'name': 'tblastn-wrapper',
    'version': '0.1.9',
    'description': 'A wrapper for tblastn that parallelises queries',
    'long_description': None,
    'author': 'Yasir Kusay',
    'author_email': 'yasir.kusay@student.unsw.edu.au',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
