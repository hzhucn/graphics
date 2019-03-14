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
"""Tests for triangle."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from absl.testing import parameterized
import numpy as np
import tensorflow as tf

from tensorflow_graphics.geometry import triangle
from tensorflow_graphics.geometry import vector
from tensorflow_graphics.util import test_case


class TriangleTest(test_case.TestCase):

  @parameterized.parameters(
      ((0., 0., 0.), (0., 0., 0.), (0., 0., 0.)),
      ((1., 0., 0.), (0., 0., 0.), (0., 0., 0.)),
      ((0., 0., 0.), (0., 1., 0.), (0., 0., 0.)),
      ((0., 0., 0.), (0., 0., 0.), (0., 0., 1.)),
  )
  def test_normal_assert(self, v0, v1, v2):
    """Tests the triangle normal assertion."""
    with self.assertRaises(tf.errors.InvalidArgumentError):
      self.evaluate(triangle.normal(v0, v1, v2))

  @parameterized.parameters(
      ((3,), (3,), (3,)),
      ((1, 3), (2, 3), (2, 3)),
      ((2, 3), (1, 3), (2, 3)),
      ((2, 3), (2, 3), (1, 3)),
      ((None, 3), (None, 3), (None, 3)),
  )
  def test_normal_exception_not_raised(self, *shapes):
    """Tests that the shape exceptions are not raised."""
    self.assert_exception_is_not_raised(triangle.normal, shapes)

  @parameterized.parameters(
      ("'v0' and 'v1' should be broadcastable.", (2, 3), (3, 3), (2, 3)),
      ("'v0' and 'v2' should be broadcastable.", (2, 3), (2, 3), (3, 3)),
      ("'v0' must have 3 dimensions.", (None,), (3,), (3,)),
      ("'v1' must have 3 dimensions.", (3,), (None,), (3,)),
      ("'v2' must have 3 dimensions.", (3,), (3,), (None,)),
  )
  def test_normal_exception_raised(self, error_msg, *shapes):
    """Tests that the shape exceptions are properly raised."""
    self.assert_exception_is_raised(triangle.normal, error_msg, shapes)

  @parameterized.parameters(
      ((0., 0., 1.), (0., 0., 0.), (0., 1., 0.)),
      ((0., 1., 0.), (0., 0., 0.), (0., 0., 1.)),
      ((1., 0., 0.), (0., 0., 0.), (0., 0., 1.)),
      ((0., 0., 1.), (0., 0., 0.), (1., 0., 0.)),
      ((0., 1., 0.), (0., 0., 0.), (1., 0., 0.)),
      ((1., 0., 0.), (0., 0., 0.), (0., 1., 0.)),
      ((1., 0., 0.), (0., 1., 0.), (0., 0., 1.)),
  )
  def test_normal_jacobian_preset(self, *vertices):
    """Test the Jacobian of the triangle normal function."""
    v0_init, v1_init, v2_init = [np.array(v) for v in vertices]
    v0_tensor, v1_tensor, v2_tensor = [
        tf.convert_to_tensor(value=v) for v in [v0_init, v1_init, v2_init]
    ]
    y = triangle.normal(v0_tensor, v1_tensor, v2_tensor)
    with self.subTest(name="v0"):
      self.assert_jacobian_is_correct(v0_tensor, v0_init, y)
    with self.subTest(name="v1"):
      self.assert_jacobian_is_correct(v1_tensor, v1_init, y)
    with self.subTest(name="v2"):
      self.assert_jacobian_is_correct(v2_tensor, v2_init, y)

  def test_normal_jacobian_random(self):
    """Test the Jacobian of the triangle normal function."""
    tensor_size = np.random.randint(3)
    tensor_shape = np.random.randint(1, 10, size=(tensor_size)).tolist()
    v0_init, v1_init, v2_init = [
        np.random.random(size=tensor_shape + [3]) for _ in range(3)
    ]
    v0_tensor, v1_tensor, v2_tensor = [
        tf.convert_to_tensor(value=v) for v in [v0_init, v1_init, v2_init]
    ]
    y = triangle.normal(v0_tensor, v1_tensor, v2_tensor)
    with self.subTest(name="v0"):
      self.assert_jacobian_is_correct(v0_tensor, v0_init, y)
    with self.subTest(name="v1"):
      self.assert_jacobian_is_correct(v1_tensor, v1_init, y)
    with self.subTest(name="v2"):
      self.assert_jacobian_is_correct(v2_tensor, v2_init, y)

  @parameterized.parameters(
      (((0., 0., 1.), (0., 0., 0.), (0., 1., 0.)), ((-1., 0., 0.),)),
      (((0., 1., 0.), (0., 0., 0.), (0., 0., 1.)), ((1., 0., 0.),)),
      (((1., 0., 0.), (0., 0., 0.), (0., 0., 1.)), ((0., -1., 0.),)),
      (((0., 0., 1.), (0., 0., 0.), (1., 0., 0.)), ((0., 1., 0.),)),
      (((0., 1., 0.), (0., 0., 0.), (1., 0., 0.)), ((0., 0., -1.),)),
      (((1., 0., 0.), (0., 0., 0.), (0., 1., 0.)), ((0., 0., 1.),)),
      (((1., 0., 0.), (0., 1., 0.), (0., 0., 1.)), ((-np.sqrt(1. / 3.),) * 3,)),
  )
  def test_normal_preset(self, test_inputs, test_outputs):
    """Tests the triangle normal computation."""
    self.assert_output_is_correct(triangle.normal, test_inputs, test_outputs)

  @parameterized.parameters((False,), (True,))
  def test_normal_random(self, clockwise):
    """Tests the triangle normal computation in each axis."""
    tensor_size = np.random.randint(3)
    tensor_shape = np.random.randint(1, 10, size=(tensor_size)).tolist()
    zeros = np.zeros(shape=tensor_shape + [1])
    for i in range(3):
      v0 = np.random.random(size=tensor_shape + [3])
      v1 = np.random.random(size=tensor_shape + [3])
      v2 = np.random.random(size=tensor_shape + [3])
      v0[..., i] = 0.
      v1[..., i] = 0.
      v2[..., i] = 0.
      n = np.zeros_like(v0)
      n[..., i] = 1.
      normal = triangle.normal(v0, v1, v2, clockwise)
      with self.subTest():
        self.assertAllClose(tf.abs(normal), n)
      with self.subTest():
        self.assertAllClose(vector.dot(normal, (v1 - v0)), zeros)
      with self.subTest():
        self.assertAllClose(vector.dot(normal, (v2 - v0)), zeros)


if __name__ == "__main__":
  test_case.main()