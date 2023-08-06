# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mdformat_black']

package_data = \
{'': ['*']}

install_requires = \
['black', 'mdformat>=0.1.1']

entry_points = \
{'mdformat.codeformatter': ['python = mdformat_black:format_python']}

setup_kwargs = {
    'name': 'mdformat-black',
    'version': '0.0.1',
    'description': 'Mdformat plugin to Blacken Python code blocks',
    'long_description': '# mdformat-black',
    'author': 'Taneli Hukkinen',
    'author_email': 'hukkinj1@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hukkinj1/mdformat-black',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
