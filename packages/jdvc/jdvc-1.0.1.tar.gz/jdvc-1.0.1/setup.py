#!/usr/bin/env python

from setuptools import setup

version = '1.0.1'

required = open('requirements.txt').read().split('\n')

setup(
    name='jdvc',
    version=version,
    description=' ',
    author='Miroslav Balaz',
    author_email='gpslayer@gmail.com',
    url='https://github.com/miro-balaz/jdvc',
    packages=['jdvc'],
    install_requires=required,
    long_description='See ' + 'https://github.com/miro-balaz/jdvc',
    license='MIT',
   entry_points='''
        [console_scripts]
        jdvc=jdvc.main:main
    '''
)
