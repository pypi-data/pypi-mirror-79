#! /usr/bin/env python3
import setuptools

with open("README", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="climatehub", # Replace with your own username
  version="0.0.1",
  author="Cheng Li",
  author_email="cli@gps.caltech.edu",
  description="hub for climate data",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/chengcli/climatehub",
  #ext_modules = extensions,
  ext_modules = None,
  classifiers = [
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
  ],
  python_requires='>=3.6',
)
