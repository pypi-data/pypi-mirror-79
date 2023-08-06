# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['agon']
install_requires = \
['jmespath>=0.10.0,<0.11.0']

setup_kwargs = {
    'name': 'agon',
    'version': '0.1.0',
    'description': 'Thin wrapper around jmespath in order to compose projections',
    'long_description': None,
    'author': 'Xavier Barbosa',
    'author_email': 'clint.northwood@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
