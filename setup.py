#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='pytest-knows',
    version='0.1.2',
    author='mapix',
    author_email='mapix.me@gmail.com',
    py_modules=['ptknows'],
    install_requires=['pytest>=2.3.4'],
    entry_points={'pytest11': ['ptknows = ptknows']},
    url='https://github.com/mapix/ptknows',
    description='A pytest plugin that can automaticly skip test case based on dependence info calculated by trace',
    long_description=open('README.rst').read(),
    zip_safe=True,
)
