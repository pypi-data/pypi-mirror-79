# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ecis_processing']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.0.5,<2.0.0']

entry_points = \
{'console_scripts': ['ecis-processing = ecis_processing.__main__:main']}

setup_kwargs = {
    'name': 'ecis-processing',
    'version': '0.6.0',
    'description': 'A program that processes diagnosis and medication data ',
    'long_description': "====================\nECIS Data Processing\n====================\n.. image:: https://img.shields.io/pypi/v/ecis-processing\n    :alt: PyPI\n    :target: https://pypi.org/project/ecis-processing/\n.. image:: https://img.shields.io/lgtm/alerts/github/tactlessfish/ecis-processing\n    :alt: LGTM Alerts\n    :target: https://lgtm.com/projects/g/tactlessfish/ecis-processing?mode=list\n\nUsage\n=====\n.. code-block::\n\n    usage: ecis-processing [-h] [-o OUTPUT] DIRECTORY\n\n    Process diagnosis and medication data.\n\n    positional arguments:\n      DIRECTORY             path to input directory\n\n    optional arguments:\n      -h, --help            show this help message and exit\n      -o OUTPUT, --output OUTPUT\n                            output file name, defaults to 'processed.csv'\n\nDisclaimer\n==========\nAll test data EHRs are fictitious. No identification with actual persons (living or deceased)\nis intended or should be inferred.\n",
    'author': 'Fisher Sun',
    'author_email': 'fisher521.fs@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tactlessfish/ecis-processing',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
