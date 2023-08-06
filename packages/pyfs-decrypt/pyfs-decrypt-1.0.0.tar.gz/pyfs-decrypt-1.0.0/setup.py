# -*- coding: utf-8 -*-

from setuptools import setup


version = '1.0.0'


setup(
    name='pyfs-decrypt',
    version=version,
    keywords='Feishu Decrypt',
    description='Feishu Decrypt Module for Python.',
    long_description=open('README.rst').read(),

    url='https://github.com/feishu-sdk-python/pyfs-decrypt',

    author='Hackathon',
    author_email='kimi.huang@brightcells.com',

    packages=['pyfs_decrypt'],
    py_modules=[],
    # Python3.x
    # from Crypto.Util.py3compat import byte_string ImportError: cannot import name 'byte_string'
    # pip3 uninstall pycrypto
    # pip3 uninstall pycryptodome
    # pip3 install pycryptodome
    install_requires=['pycryptodome'],

    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
