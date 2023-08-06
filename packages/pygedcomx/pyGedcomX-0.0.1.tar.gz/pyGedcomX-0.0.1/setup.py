# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gedcomx']

package_data = \
{'': ['*']}

install_requires = \
['language-tags>=1.0.0,<2.0.0',
 'lark-parser>=0.9.0,<0.10.0',
 'pendulum>=2.1.2,<3.0.0',
 'pydantic>=1.6.1,<2.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.0,<2.0']}

setup_kwargs = {
    'name': 'pygedcomx',
    'version': '0.0.1',
    'description': 'GEDCOM X toolbox for Python',
    'long_description': '====================\nWelcome to pyGedcomX\n====================\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/psf/black\n.. image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg\n    :target: https://opensource.org/licenses/Apache-2.0\n\nThis is Python implementation of GEDCOM X specification\nas described in `GEDCOM X Conceptual Model`_.\n\n.. _GEDCOM X Conceptual Model: https://github.com/FamilySearch/gedcomx/blob/master/specifications/conceptual-model-specification.md\n\nFeatures\n========\n\n* reading and writing of the GEDCOM X JSON Serialization Format with use of pydantic.\n\nFeatures in development\n=======================\n\n* GEDCOM X File Format support\n* GEDCOM X Extensions support\n',
    'author': 'Dominik Kozaczko',
    'author_email': 'dominik@kozaczko.info',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dekoza/pyGedcomX',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
