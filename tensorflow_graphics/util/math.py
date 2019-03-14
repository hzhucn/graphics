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
"""This module contains math routines that are shared by across different modules."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import inspect
import sys

import numpy as np
import tensorflow as tf

from tensorflow_graphics.util import asserts
from tensorflow_graphics.util import safe_ops


def cartesian_to_spherical_coordinates(point_cartesian, name=None):
  """Function to transform Cartesian coordinates to spherical coordinates.

  Args:
    point_cartesian: N-D tensor of shape `[?, ..., ?, 3]`. In the last
      dimension, the data follows the x,y,z order.
    name: A name for this op. Defaults to 'cartesian_to_spherical_coordinates'.

  Returns:
    N-D tensor of shape `[?, ..., ?, 3]`. The last dimensions contains
    (r,theta,phi), where r is the sphere radius, theta the polar angle and phi
    the azimuthal angle.
  """
  with tf.compat.v1.name_scope(name, "cartesian_to_spherical_coordinates",
                               [point_cartesian]):
    point_cartesian = tf.convert_to_tensor(value=point_cartesian)
    if point_cartesian.shape.as_list()[-1] != 3:
      raise ValueError("'point_cartesian' must have 3 dimensions.")
    x, y, z = tf.unstack(point_cartesian, axis=-1)
    radius = tf.norm(tensor=point_cartesian, axis=-1)
    theta = tf.acos(safe_ops.safe_signed_div(z, radius))
    phi = tf.atan2(y, x)
    return tf.stack((radius, theta, phi), axis=-1)


def _double_factorial_loop_body(n, result, two):
  result = tf.where(tf.greater_equal(n, two), result * n, result)
  return n - two, result, two


def _double_factorial_loop_condition(n, result, two):
  del result  # Unused
  return tf.cast(tf.math.count_nonzero(tf.greater_equal(n, two)), tf.bool)


def double_factorial(n):
  """Computes the double factorial of `n`.

  Args:
    n: N-D tensor of shape `[?, ..., ?]`.

  Returns:
    N-D tensor of shape `[?, ..., ?]`.
  """
  n = tf.convert_to_tensor(value=n)
  two = tf.ones_like(n) * 2
  result = tf.ones_like(n)
  _, result, _ = tf.while_loop(
      cond=_double_factorial_loop_condition,
      body=_double_factorial_loop_body,
      loop_vars=[n, result, two])
  return result


def factorial(n):
  """Computes the factorial of `n`.

  Args:
    n: N-D tensor of shape `[?, ..., ?]`.

  Returns:
    N-D tensor of shape `[?, ..., ?]`.
  """
  n = tf.convert_to_tensor(value=n)
  return tf.exp(tf.math.lgamma(n + 1))


def spherical_to_cartesian_coordinates(point_spherical, name=None):
  """Function to transform Cartesian coordinates to spherical coordinates.

  Args:
    point_spherical: N-D tensor of shape `[?, ..., ?, 3]`. The last dimension
      contains r, theta, and phi that respectively correspond to the radius,
      polar angle and azimuthal angle; r must be non-negative.
    name: A name for this op. Defaults to 'spherical_to_cartesian_coordinates'.

  Raises:
    tf.errors.InvalidArgumentError: If r, theta or phi contains out of range
    data.

  Returns:
    N-D tensor of shape `[?, ..., ?, 3]`. The data in the last dimension
    follows the x,y,z order.
  """
  with tf.compat.v1.name_scope(name, "spherical_to_cartesian_coordinates",
                               [point_spherical]):
    point_spherical = tf.convert_to_tensor(value=point_spherical)
    if point_spherical.shape.as_list()[-1] != 3:
      raise ValueError("'point_spherical' must have 3 dimensions.")
    r, theta, phi = tf.unstack(point_spherical, axis=-1)
    r = asserts.assert_all_above(r, 0)
    tmp = r * tf.sin(theta)
    x = tmp * tf.cos(phi)
    y = tmp * tf.sin(phi)
    z = r * tf.cos(theta)
    return tf.stack((x, y, z), axis=-1)


def square_to_spherical_coordinates(point_2d, name=None):
  """Maps points from a unit square to a unit sphere.

  Args:
    point_2d: N-D tensor of shape `[?, ..., ?, 2]` with values in [0,1].
    name: A name for this op. Defaults to
      "math_square_to_spherical_coordinates".

  Returns:
    N-D tensor of shape `[?, ..., ?, 2]` with [..., 0] having values in [0, pi]
    and [..., 1] with values in [0, 2pi].

  Raises:
    ValueError: if the shape of `point_2d`  is not supported.
    InvalidArgumentError: if at least an element of `point_2d` is outside of
    [0,1].

  """
  with tf.compat.v1.name_scope(name, "math_square_to_spherical_coordinates",
                               [point_2d]):
    point_2d = tf.convert_to_tensor(value=point_2d)
    point_2d = asserts.assert_all_in_range(
        point_2d, 0.0, 1.0, open_bounds=False)
    if point_2d.shape.as_list()[-1] != 2:
      raise ValueError("'point_2d' must have 2 dimensions.")
    x, y = tf.unstack(point_2d, axis=-1)
    theta = 2.0 * tf.acos(tf.sqrt(1.0 - x))
    phi = 2.0 * np.pi * y
    return tf.stack((tf.ones_like(theta), theta, phi), axis=-1)


# API contains all public functions.
__all__ = [
    obj_name for obj_name, obj in inspect.getmembers(sys.modules[__name__])
    if inspect.isfunction(obj) and not obj_name.startswith("_")
]
