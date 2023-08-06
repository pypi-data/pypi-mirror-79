# All .ui files and .so files are added through keyword: package_data, because setuptools doesn't include them automatically.
import sys
import os
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = "opdesign",
    version = "0.0.2",
    author = "Zhu Liang",
    author_email = "zliang8@uic.edu",
    description = "A python package for optimal-design of any experiment",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/zhul9311/optimal-design.git",
    packages = find_packages(),
    package_dir = {'':'.'},
    package_data = {
        '' : ['']
    },
    exclude_package_data = {
        '' : ['.git/','.setup.py.swp']
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires = '>=3.6',
    install_requires = [
        'scipy',
        'matplotlib',
        'lmfit',
        'numba'
    ]
)
