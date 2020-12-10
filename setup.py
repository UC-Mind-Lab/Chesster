#!/usr/bin/env python
"""The setup file for installing Chesster as a module"""
import os
from setuptools import setup, find_packages

setup(
    version="0.5.1",
    setup_requires=[],
    test_require=[],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'chesster = chesster.cli:cli_interface'
        ]
    }
)
