#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 19 13:18:34 2018

@author: xszpo
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyAllegro",
    version="0.2.0",
    license = 'MIT',
    author="xSzpo",
    author_email='xszpox@gmail.com',
    description="pyAllegro is a framework, that provides a simple way to use"
                " Allegro Web API and Rest AP. ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xSzpo/pyAllegro",
    packages=setuptools.find_packages(),
    install_requires=[
    	'suds-jurko','requests'
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)