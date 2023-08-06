# Retail Stats

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/63c5fafac4ed4af59e10c88538d3d7ef)](https://app.codacy.com/manual/insectatorious/retail-stats?utm_source=github.com&utm_medium=referral&utm_content=insectatorious/retail-stats&utm_campaign=Badge_Grade_Dashboard)
[![Build Status](https://travis-ci.org/insectatorious/retail-stats.svg?branch=master)](https://travis-ci.org/insectatorious/retail-stats)
[![Coverage Status](https://coveralls.io/repos/github/insectatorious/retail-stats/badge.svg?branch=master)](https://coveralls.io/github/insectatorious/retail-stats?branch=master)
[![PyPI version shields.io](https://img.shields.io/pypi/v/retail-stats.svg)](https://pypi.python.org/pypi/retail-stats/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/retail-stats.svg)](https://pypi.python.org/pypi/retail-stats/)
[![PyPI license](https://img.shields.io/pypi/l/retail-stats.svg)](https://pypi.python.org/pypi/retail-stats/)


This repository contains code to calculate various values used in retail for 
products whose sales and prices are provided.

Metrics currently available:

 1. Price Elasticity (_In Progress_)
 2. Cross Elasticity (**Complete**)

These simple, almost naive, implementations are taken from the Wikipedia 
definitions of the metrics. All performance benefits are from the work of 
Numpy. The purpose of this repository is to provide some convenience functions.

## Installation

Install from PyPi.

```commandline
pip install retail-stats
```

If installing outside of a `[virtualenv]()` then use `--user` to avoid permission 
issues:
```commandline
pip install --user retail-stats
```

### Dependencies

1. `numpy~=1.19`

## Calculations

### Cross Elasticity
From [Wikipedia](https://en.wikipedia.org/wiki/Cross_elasticity_of_demand), 
> measures the responsiveness of the quantity demanded for a good to a change 
>in the price of another good, _ceteris paribus_.

This can be seen written using the formula:

```text
Percentage Change in Quantity Sold of Product B
-------------------------------------------------
Percentage Change in Price Charged for Product A
``` 

The implementation is a direct copy of the formula. 

```python
from retail_stats.elasticity import calculate_cross_elasticity
```

#### Calculate Cross Elasticity for a single pair of products
```python
from math import isclose
from retail_stats import elasticity

original_quantity = 200
new_quantity = 400

original_price = 1000
new_price = 1050
# (200 / 300) / (50 / 1025)
expected_ced = 13.66666666666666
ced = elasticity.calculate_cross_elasticity(original_quantity, 
                                            new_quantity, 
                                            original_price, 
                                            new_price)

assert isclose(expected_ced, ced)
```

#### Calculate All Cross Elasticities

```python
from math import isclose

import numpy as np

from retail_stats.elasticity import get_all_cross_elasticities

skus = np.array(list("ABCD"))
# [original, new]
qty_a = [200, 0]
qty_b = [200, 400]
prc_a = [1000, 1050]
prc_b = [1000, 1000]

qty_c = [1000, 1050]
qty_d = [1000, 1100]
prc_c = [100, 80]
prc_d = [80, 80]

original_quantities = [qty_a[0], qty_b[0], qty_c[0], qty_d[0]]
new_quantities = [qty_a[1], qty_b[1], qty_c[1], qty_d[1]]
original_prices = [prc_a[0], prc_b[0], prc_c[0], prc_d[0]]
new_prices = [prc_a[1], prc_b[1], prc_c[1], prc_d[1]]

"""
Cross Elasticities between pairs A,B and C,D

  | A | B | C | D 
A |   |   |   |
B |   |   |   | 
C |   |   |   | 
D |   |   |   |
"""

ceds = get_all_cross_elasticities(original_quantities=original_quantities,
                                  new_quantities=new_quantities,
                                  original_prices=original_prices,
                                  new_prices=new_prices)

assert ceds.shape == (len(skus), len(skus))
assert isclose(ceds[np.argwhere(skus == "A"), np.argwhere(skus == "A")], -41)
assert isclose(ceds[np.argwhere(skus == "B"), np.argwhere(skus == "A")], 13.66666666666666)
assert isclose(ceds[np.argwhere(skus == "D"), np.argwhere(skus == "C")], -0.4285714286)
assert isclose(ceds[np.argwhere(skus == "C"), np.argwhere(skus == "A")], 1)
assert isclose(ceds[np.argwhere(skus == "A"), np.argwhere(skus == "C")], 9)

```

## Performance

#### Core elasticity function

| Number of Products |  Time in Seconds
| ------------------ | ----------------- | 
| 1,000              | 0.065512 
| 10,000             | 0.200022 
| 100,000            | 1.727269 
| 1,000,000          | 26.730988 
