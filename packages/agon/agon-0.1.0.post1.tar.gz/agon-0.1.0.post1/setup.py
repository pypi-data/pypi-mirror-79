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
    'version': '0.1.0.post1',
    'description': 'Thin wrapper around jmespath in order to compose projections',
    'long_description': '# Agon\n\nAgon is a thin wrapper around [jmespath](https://pypi.org/project/jmespath/) which let you to compose projections in a more natural manner.\n\nIt\'s usage is quite simple\n\n```python\nfrom agon import Agon\n\nassert Agon("foo | bar") == Agon("foo") | Agon("bar") == Agon("foo") | "bar"\nassert {"foo": {"bar": "baz"}} | Agon("foo | bar") == "baz"\nassert {"foo": {"bar": "baz"}} | Agon("foo") | Agon("bar") == "baz"\nassert {"foo": {"bar": "baz"}} | (Agon("foo") | "bar") == "baz"\n```\n',
    'author': 'Xavier Barbosa',
    'author_email': 'clint.northwood@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://lab.errorist.xyz/py/agon',
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
