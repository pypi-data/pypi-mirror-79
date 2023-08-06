# -*- coding: utf-8 -*-
import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="retail-stats",
  version="0.0.2-post1",
  author="Sumanas Sarma",
  author_email="insectatorious+pypi@gmail.com",
  keywords="price-elasticity cross-elasticity sales-analysis",
  description="A simple library to calculate price elasticity, cross elasticity",
  long_description=long_description,
  long_description_content_type="text/markdown",
  install_requires=[
    "numpy~=1.19"
  ],
  url="https://github.com/insectatorious/retail-stats",
  packages=setuptools.find_packages(),
  classifiers=[
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Operating System :: OS Independent",
    "Development Status :: 3 - Alpha",
    "Topic :: Office/Business",
    "Topic :: Office/Business :: Financial"
  ],
  python_requires='>=3.7',
)