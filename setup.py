#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name="logger_serv_py_cli",
    version='0.1',
    packages = find_packages(),
    include_package_data = True,
    install_requires=["requests", "requests-futures"],
)
