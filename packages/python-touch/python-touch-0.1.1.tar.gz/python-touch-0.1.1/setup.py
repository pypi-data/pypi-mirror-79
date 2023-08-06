# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['python_touch']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0']

entry_points = \
{'console_scripts': ['pytouch = python_touch.cli:main']}

setup_kwargs = {
    'name': 'python-touch',
    'version': '0.1.1',
    'description': '',
    'long_description': "# python-touch\n\nThis is a CLI tool for people who are tired of creating `__init__.py` files in their Python projects.\n\n# Instration\n\n```bash\n$ pip install python-touch\n$ # if you're a pipx user.\n$ pipx install python-touch\n```\n\n# Usage\n\nThe following command creates `__init__.py` recursively.\n\n```bash\n$ pytouch {directory name}\n```",
    'author': 'takeshi0406',
    'author_email': 'sci.and.eng@gmail.com',
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
