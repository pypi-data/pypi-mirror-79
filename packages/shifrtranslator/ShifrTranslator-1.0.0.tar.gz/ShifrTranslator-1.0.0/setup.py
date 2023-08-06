# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['shifrtranslator']
setup_kwargs = {
    'name': 'shifrtranslator',
    'version': '1.0.0',
    'description': 'Module for translating English text into: Morse code, Atbash cipher, Caesar cipher and Binary code',
    'long_description': None,
    'author': 'Pavel Popov',
    'author_email': 'p16.popov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
