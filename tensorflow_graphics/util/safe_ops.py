#Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Safe divisions and inverse trigonometric functions for tf.graphics.

  This module uses safe fixes to prevent NaN's and Inf's from appearing due to
  machine precision issues. Safe fixes ensure that the derivative is unchanged
  and the sign of the perturbation is unbiased.

  If tf.graphics debug flag is enabled (defined as TFG_ADD_ASSERTS_TO_GRAPH
  in tfg_flags.py), all functions also add assrtions to the graph to ensure that
  the fix has worked as expected.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from absl import flags
import numpy as np
import tensorflow as tf

from tensorflow_graphics.util import asserts
from tensorflow_graphics.util import tfg_flags

FLAGS = flags.FLAGS


def nonzero_sign(x, name=None):
  """Returns the sign of x with sign(0) defined as 1 instead of 0."""
  with tf.compat.v1.name_scope(name, 'nonzero_sign', [x]):
    x = tf.convert_to_tensor(value=x)
    one = tf.ones_like(x)
    return tf.where(tf.greater_equal(x, 0.0), one, -one)


def safe_cospx_div_cosx(theta, factor, eps=None, name=None):
  """Calculates cos(factor * theta)/cos(theta) safely.

  cos(factor * theta)/cos(theta) has periodic edge cases with division by zero
  problems, and also zero / zero, e.g. when factor is equal to 1.0 and theta
  is (n + 1/2)pi. This function adds signed eps to the angles in
  both the nominator and the denominator to ensure safety, and returns the
  correct values in all edge cases.

  Args:
    theta: N-D tensor with any shape, representing angles in radians.
    factor: Float or N-D tensor that has a compatible shape with theta for
      multiplication.
    eps: A float, used to perturb the angle. If left None, its value is
      automatically determined from the dtype of theta.
    name: A name for this op. Defaults to 'safe_cospx_div_cosx'.

  Raises:
    tf.errors.InvalidArgumentError: If tfg debug flag is set and the division
      returns NaN or Inf values.

  Returns:
    N-D tensor with the same shape as theta * factor.
  """
  with tf.compat.v1.name_scope(name, 'safe_cospx_div_cosx',
                               [theta, factor, eps]):
    theta = tf.convert_to_tensor(value=theta)
    factor = tf.convert_to_tensor(value=factor, dtype=theta.dtype)
    if eps is None:
      eps = asserts.select_eps_for_division(theta.dtype)
    eps = tf.convert_to_tensor(value=eps, dtype=theta.dtype)
    # eps will be multiplied with factor next, which can make it zero.
    # Therefore we multiply eps with min(1/factor, 1e10), which can handle
    # factors as small as 1e-10 correctly, while preventing a division by zero.
    eps *= tf.clip_by_value(1.0 / factor, 1.0, 1e10)
    sign = nonzero_sign(0.5 * np.pi - tf.mod(theta - 0.5 * np.pi, np.pi))
    theta += sign * eps
    div = tf.cos(factor * theta) / tf.cos(theta)
    if FLAGS[tfg_flags.TFG_ADD_ASSERTS_TO_GRAPH].value:
      div = tf.debugging.check_numerics(div, message='Inf or NaN detected.')
    return div


def safe_shrink(vector,
                minval=None,
                maxval=None,
                open_bounds=False,
                eps=None,
                name=None):
  """Shrinks vector by (1.0 - eps) based on its dtype.

  This function shrinks the input vector by a very small amount to ensure that
  it is not outside of expected range because of floating point precision
  of operations, e.g. dot product of a normalized vector with itself can
  be greater than 1.0 by a small amount determined by the dtype of the vector.
  This function can be used to shrink it without affecting its derivative
  (unlike tf.clip_by_value) and make it safe for other operations like acos(x).
  If the tfg debug flag TFG_ADD_ASSERTS_TO_GRAPH defined in tfg_flags.py
  is set to True, this function adds assertions to the graph that explicitly
  check that the vector is in range [minval, maxval] when open_bounds is False,
  or in range (minval, maxval) when open_bounds is True.

  Args:
    vector: N-D tensor of any shape.
    minval: A float or an N-D tensor with the same shape as vector. Assumed
      lower bound for tensor after shrinking. This is only used when the
      tf.graphics debug flag is set, in which case it cannot be None.
    maxval: A float or an N-D tensor with the same shape as vector. Assumed
      upper bound for tensor after shrinking. This is only used when the
      tf.graphics debug flag is set, in which case it cannot be None.
    open_bounds: A boolean indicating whether the assumed range is open or
      closed, only to be used when tf.graphics debug flag is set.
    eps: A float, used to shrink the vector. If left None, its value is
      automatically determined from the dtype of the vector.
    name: A name for this op. Defaults to 'safe_shrink'.

  Raises:
    ValueError: If tfg debug flag is set and minval or maxval is None.
    tf.errors.InvalidArgumentError: If tfg debug flag is set and the vector is
      not inside the expected range.

  Returns:
    N-D tensor with the same shape as vector, which holds the shrinked values.
  """
  with tf.compat.v1.name_scope(name, 'safe_shrink',
                               [vector, minval, maxval, eps]):
    vector = tf.convert_to_tensor(value=vector)
    if eps is None:
      eps = asserts.select_eps_for_addition(vector.dtype)
    eps = tf.convert_to_tensor(value=eps, dtype=vector.dtype)
    vector *= (1.0 - eps)
    if FLAGS[tfg_flags.TFG_ADD_ASSERTS_TO_GRAPH].value:
      if minval is None or maxval is None:
        raise ValueError('minval and maxval cannot be None '
                         'when debug flag is set to True.')
      minval = tf.convert_to_tensor(value=minval, dtype=vector.dtype)
      maxval = tf.convert_to_tensor(value=maxval, dtype=vector.dtype)
      vector = asserts.assert_all_in_range(
          vector, minval, maxval, open_bounds=open_bounds)
    return vector


def safe_signed_div(a, b, eps=None, name=None):
  """Calculates a/b safely.

  If the tfg debug flag TFG_ADD_ASSERTS_TO_GRAPH defined in tfg_flags.py
  is set to True, this function adds assertions to the graph that check whether
  abs(b + eps) is greather than zero, and the division has no NaN or Inf values.

  Args:
    a: N-D tensor or a float, which is the nominator.
    b: N-D tensor or a float for the denominator with non-negative values, with
      a compatible shape with the nominator, so that a / b is a valid operation.
    eps: A small float, to be adde to the denominator. If left None, its value
      is automatically selected using b.dtype.
    name: A name for this op. Defaults to 'safe_signed_div'.

  Raises:
     tf.errors.InvalidArgumentError: If tfg debug flag is set and abs(b + eps)
       is not greater than 0, or when division causes NaN or Inf values.

  Returns:
     N-D tensor with shape determined by the division operation.
  """
  with tf.compat.v1.name_scope(name, 'safe_signed_div', [a, b, eps]):
    a = tf.convert_to_tensor(value=a)
    b = tf.convert_to_tensor(value=b)
    if eps is None:
      eps = asserts.select_eps_for_division(b.dtype)
    eps = tf.convert_to_tensor(value=eps, dtype=b.dtype)
    b += nonzero_sign(b) * eps
    div = a / b
    if FLAGS[tfg_flags.TFG_ADD_ASSERTS_TO_GRAPH].value:
      zero = tf.zeros(shape=(1), dtype=b.dtype)
      with tf.control_dependencies(
          [tf.compat.v1.assert_greater(tf.abs(b), zero)]):
        div = tf.identity(div)
      div = tf.debugging.check_numerics(
          div,
          message='Inf or NaN detected. Consider '
          'increasing eps if nominator >> 1.0.')
    return div


def safe_sinpx_div_sinx(theta, factor, eps=None, name=None):
  """Calculates sin(factor * theta)/sin(theta) safely.

  sin(factor * theta)/sin(theta) appears when calculating spherical
  interpolation weights, and it has periodic edge cases causing both zero / zero
  and division by zero problems. This function adds signed eps to the angles in
  both the nominator and the denominator to ensure safety, and returns the
  correct values estimated by l'Hopital rule in the case of zero / zero.

  Args:
    theta: N-D tensor with any shape, representing angles in radians.
    factor: Float or N-D tensor that has a compatible shape with theta for
      multiplication.
    eps: A float, used to perturb the angle. If left None, its value is
      automatically determined from the dtype of theta.
    name: A name for this op. Defaults to 'safe_sinpx_div_sinx'.

  Raises:
    tf.errors.InvalidArgumentError: If tfg debug flag is set and the division
      returns NaN or Inf values.

  Returns:
    N-D tensor with the same shape as theta * factor, containing values
      sin(factor * theta)/sin(theta).
  """
  with tf.compat.v1.name_scope(name, 'safe_sinpx_div_sinx',
                               [theta, factor, eps]):
    theta = tf.convert_to_tensor(value=theta)
    factor = tf.convert_to_tensor(value=factor, dtype=theta.dtype)
    if eps is None:
      eps = asserts.select_eps_for_division(theta.dtype)
    eps = tf.convert_to_tensor(value=eps, dtype=theta.dtype)
    # eps will be multiplied with factor next, which can make it zero.
    # Therefore we multiply eps with min(1/factor, 1e10), which can handle
    # factors as small as 1e-10 correctly, while preventing a division by zero.
    eps *= tf.clip_by_value(1.0 / factor, 1.0, 1e10)
    sign = nonzero_sign(0.5 * np.pi - tf.mod(theta, np.pi))
    theta += sign * eps
    div = tf.sin(factor * theta) / tf.sin(theta)
    if FLAGS[tfg_flags.TFG_ADD_ASSERTS_TO_GRAPH].value:
      div = tf.debugging.check_numerics(div, message='Inf or NaN detected.')
    return div


def safe_unsigned_div(a, b, eps=None, name=None):
  """Calculates a/b with b >= 0 safely.

  If the tfg debug flag TFG_ADD_ASSERTS_TO_GRAPH defined in tfg_flags.py
  is set to True, this function adds assertions to the graph that check whether
  b + eps is greather than zero, and the division has no NaN or Inf values.

  Args:
    a: N-D tensor or a float, which is the nominator.
    b: N-D tensor or a float for the denominator with non-negative values, with
      a compatible shape with the nominator, so that a / b is a valid operation.
    eps: A small float, to be added to the denominator. If left None, its value
      is automatically selected using b.dtype.
    name: A name for this op. Defaults to 'safe_unsigned_div'.

  Raises:
     tf.errors.InvalidArgumentError: If tfg debug flag is set and b + eps is not
       greater than 0, or when division causes NaN or Inf values.

  Returns:
     N-D tensor with shape determined by the division operation.
  """
  with tf.compat.v1.name_scope(name, 'safe_unsigned_div', [a, b, eps]):
    a = tf.convert_to_tensor(value=a)
    b = tf.convert_to_tensor(value=b)
    if eps is None:
      eps = asserts.select_eps_for_division(b.dtype)
    eps = tf.convert_to_tensor(value=eps, dtype=b.dtype)
    b += eps
    div = a / b
    if FLAGS[tfg_flags.TFG_ADD_ASSERTS_TO_GRAPH].value:
      zero = tf.zeros_like(b)
      with tf.control_dependencies([tf.compat.v1.assert_greater(b, zero)]):
        div = tf.identity(div)
      div = tf.debugging.check_numerics(
          div,
          message='Inf or NaN detected. Consider '
          'increasing eps if nominator >> 1.0.')
    return div