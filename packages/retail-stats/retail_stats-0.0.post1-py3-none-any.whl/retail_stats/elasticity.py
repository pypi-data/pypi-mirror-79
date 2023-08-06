# -*- coding: utf-8 -*-
import numpy as np


def calculate_cross_elasticity(original_quantities: object,
                               new_quantities: object,
                               original_prices: object,
                               new_prices: object) -> np.ndarray:
  """Calculate cross elasticity of two items.

  Pass in single values (for a single pair of products) or arrays where
  the products are linked by the same index.

  When calculating the percentage change, instead of simply taking the base
  value, the average of the original and new value is used. For example, when
  the original value is 100 and the new value is 110, instead of calculating
  the % change using 100 as the base value, 105 is used.

  Instead of % change being = 10 / 100 it is 10 /105.

  This is done so that the % change is valid both when going from the
  original value to the new value and the new value to the original value.

  See https://www.youtube.com/watch?v=Ngv0Be9NxAw.

  Simple Usage:

  The cross elasticity can be calculated by executing:

    calculate_cross_elasticity(original_quantities=200,
                               new_quantities=400,
                               original_prices=1000,
                               new_prices=1050)

  which will return a value of approx `13.67`.

  Batch Usage:

  Cross elasticities can also be calculated in a batch by passing in arrays
  of values.

  Consider two pairs of products, A, B and C, D. They have the following
  values:

  A goes from 200 units to 400 units when the price of B increases from
  1000 to 1050.

  C goes from 1000 units to 1100 units when the price of
  D drops from 100 to 80.

  Their cross elasticities can be calculated as a batch using:

    calculate_cross_elasticity(original_quantities=[200, 1000],
                               new_quantities=[400, 1100],
                               original_prices=[1000, 100],
                               new_prices=[1050, 80])

  which will return an array `[13.667, -0.429]`.

  Args:
    original_quantities: numpy array or scalar value of original quantity sold
    new_quantities: numpy array or scalar value of the new quantity sold
    original_prices: numpy array or scalar value of the original price
    new_prices: numpy array or scalar value of the new price

  Returns:
    np.ndarray: shape (M,) where M is len(original_quantity) storing cross
      elasticities.

  """

  if not isinstance(original_quantities, np.ndarray):
    original_quantities = np.asarray([original_quantities])

  if not isinstance(new_quantities, np.ndarray):
    new_quantities = np.asarray([new_quantities])

  if not isinstance(original_prices, np.ndarray):
    original_prices = np.asarray([original_prices])

  if not isinstance(new_prices, np.ndarray):
    new_prices = np.asarray([new_prices])

  __check_shape_of_arrays(original_quantities,
                          new_quantities,
                          original_prices,
                          new_prices)

  cross_elasticity = __cross_elasticity_calc(new_prices,
                                             new_quantities,
                                             original_prices,
                                             original_quantities)

  return cross_elasticity


def __cross_elasticity_calc(new_prices,
                            new_quantities,
                            original_prices,
                            original_quantities):

  quantity_base_value = np.mean([original_quantities, new_quantities], axis=0)
  price_base_value = np.mean([original_prices, new_prices], axis=0)
  change_in_quantity = new_quantities - original_quantities
  percent_change_in_quantity = change_in_quantity / quantity_base_value
  change_in_price = new_prices - original_prices
  percent_change_in_price = change_in_price / price_base_value

  return np.divide(percent_change_in_quantity,
                   percent_change_in_price,
                   out=np.zeros_like(percent_change_in_quantity),
                   where=percent_change_in_price != 0)


def get_all_cross_elasticities(original_quantities,
                               new_quantities,
                               original_prices,
                               new_prices):
  """Calculate cross elasticities for all products against each other.

  For example, given 5 products, this function will calculate the cross
  elasticity values for all possible pairings of the products = (n-1)^n.

  In this case, 5 products results in a 5x5 matrix where the rows and columns
  are the products in order. The 2nd row 3rd column stores the cross elasticity
  of the 2nd product and the 3rd product.

  As the underlying calculations are performed using Numpy's vectorised code,
  cross elasticities for 5000 products can be calculated in ~600ms ±250ms on a
  modern laptop with an i7 processor and Cython installed.

  Args:
    original_quantities: numpy array of original quantities sold
    new_quantities: numpy array of the new quantities sold
    original_prices: numpy array of the original prices
    new_prices: numpy array of the new prices

  Returns:
    np.ndarray: shape (M,M) where M is len(original_quantities) storing the
      cross elasticities of all the products against each other. dtype=float32

  """

  if not isinstance(original_quantities, np.ndarray):
    original_quantities = np.asarray(original_quantities)

  if not isinstance(new_quantities, np.ndarray):
    new_quantities = np.asarray(new_quantities)

  if not isinstance(original_prices, np.ndarray):
    original_prices = np.asarray(original_prices)

  if not isinstance(new_prices, np.ndarray):
    new_prices = np.asarray(new_prices)

  __check_shape_of_arrays(original_quantities,
                          new_quantities,
                          original_prices,
                          new_prices)

  num_skus = original_quantities.shape[0]
  ceds = np.zeros((num_skus, num_skus), dtype=np.float32)

  for i in np.arange(num_skus):
    ceds[i] = calculate_cross_elasticity(original_quantities=np.repeat(original_quantities[i], num_skus),
                                         new_quantities=np.repeat(new_quantities[i], num_skus),
                                         original_prices=original_prices, new_prices=new_prices)

  return ceds


def __check_shape_of_arrays(original_quantities,
                            new_quantities,
                            original_prices,
                            new_prices):

  if new_quantities.shape != original_quantities.shape:
    raise ValueError(f"Expected 'new_quantities' to have the same shape as "
                     f"'original_quantities'."
                     f" 'new_quantities' is {new_quantities.shape} and "
                     f" 'original_quantities' is {original_quantities.shape}.")
  if original_prices.shape != original_quantities.shape:
    raise ValueError(f"Expected 'original_prices' to have the same shape as "
                     f"'original_quantities'."
                     f" 'original_prices' is {original_prices.shape} and "
                     f" 'original_quantities' is {original_quantities.shape}.")
  if new_prices.shape != original_quantities.shape:
    raise ValueError(f"Expected 'new_prices' to have the same shape as "
                     f"'original_quantities'."
                     f" 'new_prices' is {new_prices.shape} and "
                     f" 'original_quantities' is {original_quantities.shape}.")
