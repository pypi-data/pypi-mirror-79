# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['qrcodecreator']
setup_kwargs = {
    'name': 'qrcodecreator',
    'version': '1.0.0',
    'description': 'A module for creating qr codes without any extra effort. It is based on the: qrcode module:"https://pypi.org/project/qrcode/" so it must be installed. Usage example: qrcoder("some text for the qrcode.","example.png")""" you can just write the name without format, it will be automatically saved as .jpg',
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
