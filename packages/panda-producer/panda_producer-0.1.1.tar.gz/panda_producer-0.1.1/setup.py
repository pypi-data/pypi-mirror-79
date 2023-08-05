#!python
# -*- coding:utf-8 -*-
from __future__ import print_function
from setuptools import setup, find_packages
import panda_producer

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name="panda_producer",
    version = "0.1.1",
    author="Autumn",
    author_email="zhao_qyu@163.com",
    description="put panda on your head",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://https://gitee.com/zhao_qy/panda_producer",
    packages=find_packages(),
    install_requires=[
        "numpy", "opencv-python"  
        ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
