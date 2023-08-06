# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['rifatozvyska']
setup_kwargs = {
    'name': 'rifatozvyska',
    'version': '1.0.0',
    'description': "Main().say_fraze('Hello world')",
    'long_description': None,
    'author': 'rifat_zabirov',
    'author_email': 'rifatzabirov08@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
