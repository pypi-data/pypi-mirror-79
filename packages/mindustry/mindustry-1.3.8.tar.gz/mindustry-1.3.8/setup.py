# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['mindustry']
setup_kwargs = {
    'name': 'mindustry',
    'version': '1.3.8',
    'description': 'this library allows you to manage mindustry ------------------------------------ lib using PyAutoGUI Keyboard Mouse ----------------------------------- Command to install pip install mindustry',
    'long_description': None,
    'author': 'ASVI',
    'author_email': 'aaaaaabbbbbbccscc@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.2,<4.0',
}


setup(**setup_kwargs)
