# -*- coding: utf-8 -*-
import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="retail-stats",
  version="0.0.2",
  author="Sumanas Sarma",
  author_email="insectatorious+pypi@gmail.com",
  keywords="price-elasticity cross-elasticity sales-analysis",
  description="A simple way to calculate retail stats",
  long_description=long_description,
  long_description_content_type="text/markdown",
  install_requires=[
    "numpy~=1.19"
  ],
  url="https://github.com/insectatorious/retail-stats",
  packages=setuptools.find_packages(),
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Operating System :: OS Independent",
    "Development Status :: 3 - Alpha",
    "Topic :: Office/Business"
  ],
  python_requires='>=3.7',
)