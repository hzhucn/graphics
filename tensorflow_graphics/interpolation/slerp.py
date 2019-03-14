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
"""Tensorflow.graphics slerp interpolation module.

  Spherical linear interpolation (slerp) is defined for both quaternions and for
  regular N-D vectors, and act slightly differently because of inherent
  ambiguity of quaternions. This module has two functions returning the
  interpolation weights for quaternions (quaternion_weights) and for vectors
  (vector_weights), which can then be used in a weighted sum to calculate the
  final interpolated quaternions and vectors. A helper interpolate function is
  also provided.

  The main differences between two methods are:
  vector_weights:
    can get any N-D tensor as input,
    does not expect normalized vectors as input,
    returns unnormalized outputs (in general) for unnormalized inputs.

  quaternion_weights:
    expects N-D tensors with a last dimension of 4,
    assumes normalized input,
    checks for ambiguity by looking at the angle between quaternions,
    returns normalized quaternions naturally.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import inspect
import sys

import enum
import tensorflow as tf

from tensorflow_graphics.util import asserts
from tensorflow_graphics.util import safe_ops


class InterpolationType(enum.Enum):
  """Defines interpolation methods for slerp module."""
  VECTOR = 0
  QUATERNION = 1


def _check_shapes(vector1, vector2, percent):
  """Checks if input shapes are as expected."""
  if vector1.shape.as_list() != vector2.shape.as_list():
    raise ValueError("Input tensors should have the same shape.")
  if percent.get_shape().as_list():
    if percent.shape[-1] != 1:
      raise ValueError(
          "percent should be float or a tensor with last dimension of 1.")


def _safe_dot(vector1, vector2, eps):
  """Calculates dot product while ensuring it is in the range [-1, 1]."""
  dot_product = tf.reduce_sum(
      input_tensor=vector1 * vector2, axis=-1, keepdims=True)
  # Safely shrink to make sure machine precision does not cause the dot
  # product to be outside the [-1.0, 1.0] range.
  return safe_ops.safe_shrink(
      vector=dot_product, minval=-1.0, maxval=1.0, open_bounds=False, eps=eps)


def interpolate(vector1,
                vector2,
                percent,
                method=InterpolationType.QUATERNION,
                eps=None,
                name=None):
  """Applies slerp to vectors or quaternions.

  Args:
    vector1: N-D tensor representing a vector or quaternion. Check
      vector_weights or quaternion_weights for exact requirements.
    vector2: N-D tensor representing a vector or quaternion. Check
      vector_weights or quaternion_weights for exact requirements.
    percent: A float or tensor with shape broadcastable to the shape of input
      vectors.
    method: An enumerated constant from the class InterpolationType, which is
      either InterpolationType.QUATERNION (default) if input vectors are 4-D
      quaternions, or InterpolationType.VECTOR if they are regular N-D vectors.
    eps: A small float for operation safety. If left None, its value is
      automatically selected using dtype of input vectors.
    name: A name for this op. Defaults to "vector_weights" or
      "quaternion_weights" depending on the method.

  Returns:
    N-D tensor with the same shape as input vectors, which is the result of
      interpolation.

  Raises:
    ValueError: if method is not amongst enumerated constants defined in
      InterpolationType.
  """
  if method == InterpolationType.QUATERNION:
    weight1, weight2 = quaternion_weights(
        vector1, vector2, percent, eps=eps, name=name)
  elif method == InterpolationType.VECTOR:
    weight1, weight2 = vector_weights(
        vector1, vector2, percent, eps=eps, name=name)
  else:
    raise ValueError("Unknown interpolation type supplied.")
  return interpolate_with_weights(vector1, vector2, weight1, weight2)


def interpolate_with_weights(vector1, vector2, weight1, weight2, name=None):
  """Interpolates vectors by taking their weighted sum.

  Interpolation for all variants of slerp is a simple weighted sum over inputs.
  Therefore this function simply returns weight1 * vector1 + weight2 * vector2.

  Args:
    vector1: N-D tensor representing a vector or quaternion. Check
      vector_weights or quaternion_weights for exact requirements.
    vector2: N-D tensor representing a vector or quaternion. Check
      vector_weights or quaternion_weights for exact requirements.
    weight1: A float or tensor with shape broadcastable to the shape of input
      vectors, which are the weights of vector1.
    weight2: A float or tensor with shape broadcastable to the shape of input
      vectors, which are the weights of vector2.
    name: A name for this op. Defaults to "interpolate_with_weights".

  Returns:
    N-D tensor with the same shape as input vectors, which is the result of
      interpolation.
  """
  with tf.compat.v1.name_scope(name, "interpolate_with_weights",
                               [vector1, vector2, weight1, weight2]):
    return weight1 * vector1 + weight2 * vector2


def quaternion_weights(quaternion1, quaternion2, percent, eps=None, name=None):
  """Calculates slerp weights for two normalized quaternions.

  Given a percent and two normalized quaternions, this function returns the
  slerp weights. It can also produce extrapolation weights when percent is
  outside of the [0, 1] range. It reduces to lerp when input quaternions are
  almost parallel or anti-parallel. Input quaternions are assumed to be
  normalized. The tf.graphics debug flag TFG_ADD_ASSERTS_TO_GRAPH defined
  in tfg_flags.py can be set to add assertions to the graph that check whether
  the inputs are normalized, and whether Inf or Nan values are produced.

  Args:
    quaternion1: N-D tensor of shape [?, ... , ?, 4] with a rank of at least 1.
      The tensor should be normalized in its last dimension.
    quaternion2: N-D tensor of shape [?, ... , ?, 4] with a rank of at least 1.
      The tensor should be normalized in its last dimension, and should have the
      same shape as quaternion1.
    percent: A float or tensor with shape broadcastable to the shape of input
      quaternions.
    eps: A float used to make operations safe. When left as None, the function
      automatically picks the best epsilon based on the dtype and the operation.
    name: A name for this op. Defaults to "quaternion_weights".

  Raises:
    ValueError: If the shapes of quaternions do not match, if the last
      dimensions of quaternions are not 4, or if percent is neither a float, nor
      a tensor with last dimension 1.

  Returns:
    Two N-D tensors with shape `[?, ..., ?, 1]` each, which are the two slerp
      weights for each quaternion.
  """
  with tf.compat.v1.name_scope(name, "quaternion_weights",
                               [quaternion1, quaternion2, percent]):
    quaternion1 = tf.convert_to_tensor(value=quaternion1)
    quaternion2 = tf.convert_to_tensor(value=quaternion2)
    percent = tf.convert_to_tensor(value=percent, dtype=quaternion1.dtype)
    _check_shapes(quaternion1, quaternion2, percent)

    if quaternion1.shape[-1] != 4 or quaternion2.shape[-1] != 4:
      raise ValueError("Expected quaternions with last dimension 4.")

    # Check norms if the debug flag is set, since we assume normalized inputs.
    quaternion1 = asserts.assert_normalized(quaternion1)
    quaternion2 = asserts.assert_normalized(quaternion2)

    dot_product = _safe_dot(quaternion1, quaternion2, eps)

    # Take the shorter path
    theta = tf.acos(tf.abs(dot_product))

    # safe_sinpx_div_sinx returns p for very small x, which means slerp reduces
    # to lerp automatically.
    scale1 = safe_ops.safe_sinpx_div_sinx(theta, 1.0 - percent, eps)
    scale2 = safe_ops.safe_sinpx_div_sinx(theta, percent, eps)

    # Flip the sign of scale1 if quaternions are in different hemispheres.
    # tf.sign can make scale1 zero if quaternions are orthogonal.
    scale1 *= safe_ops.nonzero_sign(dot_product)
    return scale1, scale2


def vector_weights(vector1, vector2, percent, eps=None, name=None):
  """Spherical linear interpolation (slerp) between two unnormalized vectors.

  This function applies geometric slerp to unnormalized vectors by first
  normalizing them to return the interpolation weights. It reduces to lerp when
  input vectors are exactly anti-parallel.

  Args:
    vector1: N-D tensor of shape [dim_1, ... , dim_j] with j>= 1. The tensor
      should be normalized in its last dimension.
    vector2: N-D tensor of shape [dim_1, ... , dim_j] with j>= 1. The tensor
      should be normalized in its last dimension, and should have the same shape
      as vector1.
    percent: A float or tensor with shape broadcastable to the shape of input
      vectors.
    eps: A small float for operation safety. If left None, its value is
      automatically selected using dtype of input vectors.
    name: A name for this op. Defaults to "vector_weights".

  Raises:
    ValueError: if the shape of `vector1`, `vector2`, or 'percent' is not
      supported.

  Returns:
    Two N-D tensors with shape [dim_1, ..., 1], representing interpolation
      weights for each input vector.
  """
  with tf.compat.v1.name_scope(name, "vector_weights",
                               [vector1, vector2, percent]):
    vector1 = tf.convert_to_tensor(value=vector1)
    vector2 = tf.convert_to_tensor(value=vector2)
    percent = tf.convert_to_tensor(value=percent, dtype=vector1.dtype)
    _check_shapes(vector1, vector2, percent)

    normalized1 = tf.nn.l2_normalize(vector1, axis=-1)
    normalized2 = tf.nn.l2_normalize(vector2, axis=-1)

    dot_product = _safe_dot(normalized1, normalized2, eps)

    theta = tf.acos(dot_product)
    scale1 = safe_ops.safe_sinpx_div_sinx(theta, 1.0 - percent, eps)
    scale2 = safe_ops.safe_sinpx_div_sinx(theta, percent, eps)
    return scale1, scale2


# API contains all public functions.
__all__ = [
    obj_name for obj_name, obj in inspect.getmembers(sys.modules[__name__])
    if inspect.isfunction(obj) or
    inspect.isclass(obj) and not obj_name.startswith("_")
]