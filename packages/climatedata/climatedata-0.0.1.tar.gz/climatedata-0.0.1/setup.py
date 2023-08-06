#!/usr/bin/env python3

from setuptools import setup

with open("README", "r") as fh:
    long_description = fh.read()

setup(
  name="climatedata", # Replace with your own username
  version="0.0.1",
  author="Cheng Li",
  author_email="cli@gps.caltech.edu",
  description="python api for requesting climate data",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/chengcli/climatedata",
  #ext_modules = extensions,
  ext_modules = None,
  classifiers = [
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
  ],
  python_requires='>=3.6',
)
