#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 13:02:36 2020

@author: safir
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="classic_FindS", 
    version="1.0.0",
    author="Safir Motiwala",
    author_email="safirmotiwala@gmail.com",
    description="Find-S algorithm is a Machine Learning Algorithm that finds the most specific hypothesis that fits all the positive examples.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/safir72347/ML-FindS-PyPi",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)