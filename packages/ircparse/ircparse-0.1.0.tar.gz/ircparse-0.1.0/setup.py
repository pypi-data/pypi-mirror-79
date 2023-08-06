# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['ircparse']
install_requires = \
['pydantic>=1.6.1,<2.0.0']

setup_kwargs = {
    'name': 'ircparse',
    'version': '0.1.0',
    'description': 'IRC parsing utilities',
    'long_description': None,
    'author': 'Andrew Herbig',
    'author_email': 'notandrewherbig@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
