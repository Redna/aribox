#!/usr/bin/env python

import os
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
    'aribot')))

sys.path.pop(0)

setup(
    name='aribot',
    packages=find_packages(),
    include_package_data=True,
    version="0.0.1",
    description='AriBox is an NFC action based box which allowes to play songs from NFC chips.',
    long_description='AriBox is an NFC action based box which allowes to play songs from NFC chips.',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Parents',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    author='gruhl',
    author_email='gruhl.alexander@gmail.com',
    url='https://github.com/redna/aribox',
    license='MIT',
    install_requires=['spidev', 'RPi.GPIO', 'pi-rc522'],
)
