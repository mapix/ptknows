# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name="ptknows",
    author='mapix',
    author_email='mapix.me@gmail.com',
    py_modules=['ptknows'],
    entry_points = {'pytest11': ['ptknows = ptknows']},
    zip_safe=True,
)
