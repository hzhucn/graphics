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
"""Tests for srgb."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from absl.testing import parameterized
import numpy as np
import tensorflow as tf

from tensorflow_graphics.image.color_space import srgb
from tensorflow_graphics.util import test_case


class SrgbTest(test_case.TestCase):

  def test_to_linear_random(self):
    """Tests conversion from sRGB to linear color space for random inputs."""
    tensor_size = np.random.randint(3)
    tensor_shape = np.random.randint(1, 10, size=(tensor_size)).tolist()
    srgb_input = np.random.uniform(size=tensor_shape + [3])
    linear_output = srgb.to_linear(srgb_input)
    srgb_reverse = srgb.from_linear(linear_output)
    self.assertAllClose(srgb_input, srgb_reverse)

  @parameterized.parameters(
      (((0., 0.5, 1.), (0.0404, 0.04045, 0.0405)),
       ((0., 0.214041, 1.), (0.003127, 0.003131, 0.003135))),)
  def test_to_linear_preset(self, test_inputs, test_outputs):
    """Tests conversion from sRGB to linear color space for preset inputs."""
    self.assert_output_is_correct(srgb.to_linear, (test_inputs,),
                                  (test_outputs,))

  def test_to_linear_jacobian_random(self):
    """Tests the Jacobian of the to_linear function for random inputs."""
    tensor_size = np.random.randint(3)
    tensor_shape = np.random.randint(1, 10, size=(tensor_size)).tolist()
    srgb_random_init = np.random.uniform(size=tensor_shape + [3])
    srgb_random = tf.convert_to_tensor(value=srgb_random_init)
    linear_random = srgb.to_linear(srgb_random)
    self.assert_jacobian_is_correct(srgb_random, srgb_random_init,
                                    linear_random)

  @parameterized.parameters((np.array((0., 0.01, 0.02)),), (np.array(
      (0.05, 0.06, 1.)),))
  def test_to_linear_jacobian_preset(self, inputs_init):
    """Tests the Jacobian of the to_linear function for preset inputs."""
    inputs_tensor = tf.convert_to_tensor(value=inputs_init)
    outputs = srgb.to_linear(inputs_tensor)
    self.assert_jacobian_is_correct(inputs_tensor, inputs_init, outputs)

  @parameterized.parameters(
      ((3,),),
      ((None, None, None, 3),),
  )
  def test_to_linear_exception_not_raised(self, *shape):
    """Tests that the shape exceptions are not raised."""
    self.assert_exception_is_not_raised(srgb.to_linear, shape)

  @parameterized.parameters(
      ("Input Tensor must be of rank >= 1.", ()),
      ("Input Tensor must have last dimension equal to 3.", (2, 3, 4)),
  )
  def test_to_linear_exception_raised(self, error_msg, *shape):
    """Tests that the shape exceptions are properly raised."""
    self.assert_exception_is_raised(srgb.to_linear, error_msg, shape)

  def test_from_linear_random(self):
    """Tests conversion from linear to sRGB color space for random inputs."""
    tensor_size = np.random.randint(3)
    tensor_shape = np.random.randint(1, 10, size=(tensor_size)).tolist()
    linear_input = np.random.uniform(size=tensor_shape + [3])
    srgb_output = srgb.from_linear(linear_input)
    linear_reverse = srgb.to_linear(srgb_output)
    self.assertAllClose(linear_input, linear_reverse)

  @parameterized.parameters(
      (((0., 0.5, 1.), (0.00312, 0.0031308, 0.00314)),
       ((0., 0.735357, 1.), (0.04031, 0.04045, 0.040567))),)
  def test_from_linear_preset(self, test_inputs, test_outputs):
    """Tests conversion from linear to sRGB color space for preset inputs."""
    self.assert_output_is_correct(srgb.from_linear, (test_inputs,),
                                  (test_outputs,))

  def test_from_linear_jacobian_random(self):
    """Tests the Jacobian of the from_linear function for random inputs."""
    tensor_size = np.random.randint(3)
    tensor_shape = np.random.randint(1, 10, size=(tensor_size)).tolist()
    linear_random_init = np.random.uniform(size=tensor_shape + [3])
    linear_random = tf.convert_to_tensor(value=linear_random_init)
    srgb_random = srgb.from_linear(linear_random)
    self.assert_jacobian_is_correct(linear_random, linear_random_init,
                                    srgb_random)

  @parameterized.parameters((np.array((0., 0.001, 0.002)),), (np.array(
      (0.004, 0.005, 1.)),))
  def test_from_linear_jacobian_preset(self, inputs_init):
    """Tests the Jacobian of the from_linear function for preset inputs."""
    inputs_tensor = tf.convert_to_tensor(value=inputs_init)
    outputs = srgb.from_linear(inputs_tensor)
    self.assert_jacobian_is_correct(inputs_tensor, inputs_init, outputs)

  @parameterized.parameters(
      ((3,),),
      ((None, None, None, 3),),
  )
  def test_from_linear_exception_not_raised(self, *shape):
    """Tests that the shape exceptions are not raised."""
    self.assert_exception_is_not_raised(srgb.from_linear, shape)

  @parameterized.parameters(
      ("Input Tensor must be of rank >= 1.", ()),
      ("Input Tensor must have last dimension equal to 3.", (2, 3, 4)),
  )
  def test_from_linear_exception_raised(self, error_msg, *shape):
    """Tests that the shape exceptions are properly raised."""
    self.assert_exception_is_raised(srgb.from_linear, error_msg, shape)


if __name__ == "__main__":
  test_case.main()
