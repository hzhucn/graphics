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
"""Tests for quaternion."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from absl.testing import flagsaver
from absl.testing import parameterized
import numpy as np
import tensorflow as tf

from tensorflow_graphics.transformation import axis_angle
from tensorflow_graphics.transformation import quaternion
from tensorflow_graphics.transformation import rotation_matrix_3d
from tensorflow_graphics.transformation.tests import test_data as td
from tensorflow_graphics.transformation.tests import test_helpers
from tensorflow_graphics.util import test_case


class QuaternionTest(test_case.TestCase):

  @parameterized.parameters(
      ((3,), (3,)),
      ((None, 3), (None, 3)),
  )
  def test_between_two_vectors_3d_exception_not_raised(self, *shapes):
    """Tests that the shape exceptions are not raised."""
    self.assert_exception_is_not_raised(quaternion.between_two_vectors_3d,
                                        shapes)

  @parameterized.parameters(
      ("'vector1' must have 3 dimensions.", (None,), (3,)),
      ("'vector2' must have 3 dimensions.", (3,), (None,)),
  )
  def test_between_two_vectors_3d_exception_raised(self, error_msg, *shape):
    """Tests that the shape exceptions are raised."""
    self.assert_exception_is_raised(quaternion.between_two_vectors_3d,
                                    error_msg, shape)

  @flagsaver.flagsaver(tfg_add_asserts_to_graph=False)
  def test_between_two_vectors_3d_jacobian_random(self):
    """Tests the Jacobian of between_two_vectors_3d."""
    tensor_size = np.random.randint(3)
    tensor_shape = np.random.randint(1, 10, size=(tensor_size)).tolist()
    x_1_init = np.random.random(tensor_shape + [3])
    x_2_init = np.random.random(tensor_shape + [3])
    x_1 = tf.convert_to_tensor(value=x_1_init)
    x_2 = tf.convert_to_tensor(value=x_2_init)
    y = quaternion.between_two_vectors_3d(x_1, x_2)
    self.assert_jacobian_is_correct(x_1, x_1_init, y, atol=1e-4)
    self.assert_jacobian_is_correct(x_2, x_2_init, y, atol=1e-4)

  def test_between_two_vectors_3d_random(self):
    """Checks the extracted rotation between two 3d vectors."""
    tensor_size = np.random.randint(3)
    tensor_shape = np.random.randint(1, 10, size=(tensor_size)).tolist()
    source = np.random.random(tensor_shape + [3]).astype(np.float32)
    target = np.random.random(tensor_shape + [3]).astype(np.float32)
    rotation = quaternion.between_two_vectors_3d(source, target)
    rec_target = quaternion.rotate(source, rotation)
    self.assertAllClose(
        tf.nn.l2_normalize(target, axis=-1),
        tf.nn.l2_normalize(rec_target, axis=-1))
    # Checks that resulting quaternions are normalized.
    self.assertAllEqual(
        quaternion.is_normalized(rotation), np.full(tensor_shape + [1], True))

  @parameterized.parameters(
      ((4,),),
      ((None, 4),),
  )
  def test_conjugate_exception_not_raised(self, *shape):
    """Tests that the shape exceptions of conjugate are not raised."""
    self.assert_exception_is_not_raised(quaternion.conjugate, shape)

  @parameterized.parameters(
      ("'quaternion' must have 4 dimensions.", (None,)),)
  def test_conjugate_exception_raised(self, error_msg, *shape):
    """Tests that the shape exceptions are raised."""
    self.assert_exception_is_raised(quaternion.conjugate, error_msg, shape)

  @flagsaver.flagsaver(tfg_add_asserts_to_graph=False)
  def test_conjugate_jacobian_preset(self):
    """Test the Jacobian of the conjugate function."""
    x_init = test_helpers.generate_preset_test_quaternions()
    x = tf.convert_to_tensor(value=x_init)
    y = quaternion.conjugate(x)
    self.assert_jacobian_is_correct(x, x_init, y)

  @flagsaver.flagsaver(tfg_add_asserts_to_graph=False)
  def test_conjugate_jacobian_random(self):
    """Test the Jacobian of the conjugate function."""
    x_init = test_helpers.generate_random_test_quaternions()
    x = tf.convert_to_tensor(value=x_init)
    y = quaternion.conjugate(x)
    self.assert_jacobian_is_correct(x, x_init, y)

  @parameterized.parameters(
      ((3,), (1,)),
      ((None, 3), (None, 1)),
  )
  def test_from_axis_angle_exception_not_raised(self, *shapes):
    """Tests that the shape exceptions are not raised."""
    self.assert_exception_is_not_raised(quaternion.from_axis_angle, shapes)

  @parameterized.parameters(
      ("'axis' must have 3 dimensions.", (None,), (1,)),
      ("'angle' must have 1 dimension.", (3,), (None,)),
  )
  def test_from_axis_angle_raised(self, error_msg, *shape):
    """Tests that the shape exceptions are raised."""
    self.assert_exception_is_raised(quaternion.from_axis_angle, error_msg,
                                    shape)

  @flagsaver.flagsaver(tfg_add_asserts_to_graph=False)
  def test_axis_angle_jacobian_preset(self):
    """Test the Jacobian of the from_axis_angle function."""
    x_axis_init, x_angle_init = test_helpers.generate_preset_test_axis_angle()
    x_axis = tf.convert_to_tensor(value=x_axis_init)
    x_angle = tf.convert_to_tensor(value=x_angle_init)
    y = quaternion.from_axis_angle(x_axis, x_angle)
    self.assert_jacobian_is_correct(x_axis, x_axis_init, y)
    self.assert_jacobian_is_correct(x_angle, x_angle_init, y)

  @flagsaver.flagsaver(tfg_add_asserts_to_graph=False)
  def test_from_axis_angle_jacobian_random(self):
    """Test the Jacobian of the from_axis_angle function."""
    x_axis_init, x_angle_init = test_helpers.generate_random_test_axis_angle()
    x_axis = tf.convert_to_tensor(value=x_axis_init)
    x_angle = tf.convert_to_tensor(value=x_angle_init)
    y = quaternion.from_axis_angle(x_axis, x_angle)
    self.assert_jacobian_is_correct(x_axis, x_axis_init, y)
    self.assert_jacobian_is_correct(x_angle, x_angle_init, y)

  def test_from_axis_angle_normalized_random(self):
    """Test that from_axis_angle produces normalized quaternions."""
    random_axis, random_angle = test_helpers.generate_random_test_axis_angle()
    random_quaternion = quaternion.from_axis_angle(random_axis, random_angle)
    self.assertAllEqual(
        quaternion.is_normalized(random_quaternion),
        np.ones(shape=random_angle.shape, dtype=bool))

  def test_from_axis_angle_random(self):
    """Tests quaternion conversion from an axis angle."""
    random_euler_angles = test_helpers.generate_random_test_euler_angles()
    axis, angle = axis_angle.from_euler(random_euler_angles)
    grountruth = rotation_matrix_3d.from_quaternion(
        quaternion.from_euler(random_euler_angles))
    prediction = rotation_matrix_3d.from_quaternion(
        quaternion.from_axis_angle(axis, angle))
    self.assertAllClose(grountruth, prediction, rtol=1e-3)

  @parameterized.parameters(
      ((3,),),
      ((None, 3),),
  )
  def test_from_euler_exception_not_raised(self, *shape):
    """Tests that the shape exceptions are not raised."""
    self.assert_exception_is_not_raised(quaternion.from_euler, shape)

  @parameterized.parameters(
      ("'angles' must have 3 dimensions.", (None,)),)
  def test_from_euler_exception_raised(self, error_msg, *shape):
    """Tests that the shape exceptions are raised."""
    self.assert_exception_is_raised(quaternion.from_euler, error_msg, shape)

  @flagsaver.flagsaver(tfg_add_asserts_to_graph=False)
  def test_from_euler_jacobian_preset(self):
    """Test the Jacobian of the from_euler function."""
    x_init = test_helpers.generate_preset_test_euler_angles()
    x = tf.convert_to_tensor(value=x_init)
    y = quaternion.from_euler(x)
    self.assert_jacobian_is_correct(x, x_init, y)

  @flagsaver.flagsaver(tfg_add_asserts_to_graph=False)
  def test_from_euler_jacobian_random(self):
    """Test the Jacobian of the from_euler function."""
    x_init = test_helpers.generate_random_test_euler_angles()
    x = tf.convert_to_tensor(value=x_init)
    y = quaternion.from_euler(x)
    self.assert_jacobian_is_correct(x, x_init, y)

  def test_from_euler_normalized_random(self):
    """Tests that quaternions.from_euler returns normalized quaterions."""
    random_euler_angles = test_helpers.generate_random_test_euler_angles()
    tensor_shape = random_euler_angles.shape[:-1]
    random_quaternion = quaternion.from_euler(random_euler_angles)
    self.assertAllEqual(
        quaternion.is_normalized(random_quaternion),
        np.ones(shape=tensor_shape + (1,), dtype=bool))

  def test_from_euler_random(self):
    """Tests that quaternions can be constructed from Euler angles."""
    random_euler_angles = test_helpers.generate_random_test_euler_angles()
    tensor_shape = random_euler_angles.shape[:-1]
    random_matrix = rotation_matrix_3d.from_euler(random_euler_angles)
    random_quaternion = quaternion.from_euler(random_euler_angles)
    random_point = np.random.normal(size=tensor_shape + (3,))
    rotated_with_matrix = rotation_matrix_3d.rotate(random_point, random_matrix)
    rotated_with_quaternion = quaternion.rotate(random_point, random_quaternion)
    self.assertAllClose(rotated_with_matrix, rotated_with_quaternion)

  @parameterized.parameters(
      ((3,),),
      ((None, 3),),
  )
  def test_from_euler_with_small_angles_approximation_exception_not_raised(
      self, *shapes):
    """Tests that the shape exceptions are not raised."""
    self.assert_exception_is_not_raised(
        quaternion.from_euler_with_small_angles_approximation, shapes)

  @parameterized.parameters(
      ("'angles' must have 3 dimensions.", (None,)),)
  def test_from_euler_with_small_angles_approximation_exception_raised(
      self, error_msg, *shape):
    """Tests that the shape exceptions are raised."""
    self.assert_exception_is_raised(
        quaternion.from_euler_with_small_angles_approximation, error_msg, shape)

  def test_from_euler_with_small_angles_approximation_random(self):
    # Only generate small angles. For a test tolerance of 1e-3, 0.33 was found
    # empirically to be the range where the small angle approximation works.
    random_euler_angles = test_helpers.generate_random_test_euler_angles(
        min_angle=-0.33, max_angle=0.33)
    exact_quaternion = quaternion.from_euler(random_euler_angles)
    approximate_quaternion = (
        quaternion.from_euler_with_small_angles_approximation(
            random_euler_angles))
    self.assertAllClose(exact_quaternion, approximate_quaternion, atol=1e-3)

  @parameterized.parameters(
      ("'rotation_matrix' must have 3x3 dimensions.", (3,)),
      ("'rotation_matrix' must have 3x3 dimensions.", (None, 3)),
      ("'rotation_matrix' must have 3x3 dimensions.", (3, None)),
  )
  def test_from_rotation_matrix_raised(self, error_msg, *shape):
    """Tests that the shape exceptions are raised."""
    self.assert_exception_is_raised(quaternion.from_rotation_matrix, error_msg,
                                    shape)

  @parameterized.parameters(
      ((3, 3),),
      ((None, 3, 3),),
  )
  def test_from_rotation_matrix_not_raised(self, *shape):
    """Tests that the shape exceptions are not raised."""
    self.assert_exception_is_not_raised(quaternion.from_rotation_matrix, shape)

  @flagsaver.flagsaver(tfg_add_asserts_to_graph=False)
  def test_from_rotation_matrix_jacobian_preset(self):
    """Test the Jacobian of the from_rotation_matrix function."""
    x_init = test_helpers.generate_preset_test_rotation_matrices_3d()
    x = tf.convert_to_tensor(value=x_init)
    y = quaternion.from_rotation_matrix(x)
    self.assert_jacobian_is_finite(x, x_init, y)

  @flagsaver.flagsaver(tfg_add_asserts_to_graph=False)
  def test_from_rotation_matrix_jacobian_random(self):
    """Test the Jacobian of the from_rotation_matrix function."""
    x_init = test_helpers.generate_random_test_rotation_matrix_3d()
    x = tf.convert_to_tensor(value=x_init)
    y = quaternion.from_rotation_matrix(x)
    self.assert_jacobian_is_finite(x, x_init, y)

  def test_from_rotation_matrix_normalized_random(self):
    """Tests that from_rotation_matrix produces normalized quaternions."""
    random_matrix = test_helpers.generate_random_test_rotation_matrix_3d()
    random_quaternion = quaternion.from_rotation_matrix(random_matrix)
    tensor_shape = random_matrix.shape[:-2]
    self.assertAllEqual(
        quaternion.is_normalized(random_quaternion),
        np.ones(shape=tensor_shape + (1,), dtype=bool))

  @parameterized.parameters(
      ((td.MAT_3D_ID,), (td.QUAT_ID,)),
      ((td.MAT_3D_X_45,), (td.QUAT_X_45,)),
      ((td.MAT_3D_Y_45,), (td.QUAT_Y_45,)),
      ((td.MAT_3D_Z_45,), (td.QUAT_Z_45,)),
      ((td.MAT_3D_X_90,), (td.QUAT_X_90,)),
      ((td.MAT_3D_Y_90,), (td.QUAT_Y_90,)),
      ((td.MAT_3D_Z_90,), (td.QUAT_Z_90,)),
      ((td.MAT_3D_X_180,), (td.QUAT_X_180,)),
      ((td.MAT_3D_Y_180,), (td.QUAT_Y_180,)),
      ((td.MAT_3D_Z_180,), (td.QUAT_Z_180,)),
  )
  def test_from_rotation_matrix_preset(self, test_inputs, test_outputs):
    self.assert_output_is_correct(quaternion.from_rotation_matrix, test_inputs,
                                  test_outputs)

  def test_from_rotation_matrix_random(self):
    """Tests that from_rotation_matrix produces the expected quaternions."""
    random_euler_angles = test_helpers.generate_random_test_euler_angles()
    random_rotation_matrix_3d = rotation_matrix_3d.from_euler(
        random_euler_angles)
    groundtruth = rotation_matrix_3d.from_quaternion(
        quaternion.from_euler(random_euler_angles))
    prediction = rotation_matrix_3d.from_quaternion(
        quaternion.from_rotation_matrix(random_rotation_matrix_3d))
    self.assertAllClose(groundtruth, prediction)

  @parameterized.parameters(
      ((4,),),
      ((None, 4),),
  )
  def test_inverse_exception_not_raised(self, *shape):
    """Tests that the shape exceptions are raised."""
    self.assert_exception_is_not_raised(quaternion.inverse, shape)

  @parameterized.parameters(
      ("'quaternion' must have 4 dimensions.", (None,)),)
  def test_inverse_exception_raised(self, error_msg, *shape):
    """Tests that the shape exceptions are raised."""
    self.assert_exception_is_raised(quaternion.inverse, error_msg, shape)

  @flagsaver.flagsaver(tfg_add_asserts_to_graph=False)
  def test_inverse_jacobian_preset(self):
    """Test the Jacobian of the inverse function."""
    x_init = test_helpers.generate_preset_test_quaternions()
    x = tf.convert_to_tensor(value=x_init)
    y = quaternion.inverse(x)
    self.assert_jacobian_is_correct(x, x_init, y)

  @flagsaver.flagsaver(tfg_add_asserts_to_graph=False)
  def test_inverse_jacobian_random(self):
    """Test the Jacobian of the inverse function."""
    x_init = test_helpers.generate_random_test_quaternions()
    x = tf.convert_to_tensor(value=x_init)
    y = quaternion.inverse(x)
    self.assert_jacobian_is_correct(x, x_init, y)

  def test_inverse_normalized_random(self):
    """Tests that the inverse function returns normalized quaternions."""
    random_quaternion = test_helpers.generate_random_test_quaternions()
    inverse_quaternion = quaternion.inverse(random_quaternion)
    tensor_shape = random_quaternion.shape[:-1]
    self.assertAllEqual(
        quaternion.is_normalized(inverse_quaternion),
        np.ones(shape=tensor_shape + (1,), dtype=bool))

  def test_inverse_random(self):
    """Tests that multiplying with the inverse gives identity."""
    random_quaternion = test_helpers.generate_random_test_quaternions()
    inverse_quaternion = quaternion.inverse(random_quaternion)
    final_quaternion = quaternion.multiply(random_quaternion,
                                           inverse_quaternion)
    tensor_shape = random_quaternion.shape[:-1]
    identity_quaternion = np.array((0.0, 0.0, 0.0, 1.0), dtype=np.float32)
    identity_quaternion = np.tile(identity_quaternion, tensor_shape + (1,))
    self.assertAllClose(final_quaternion, identity_quaternion, rtol=1e-3)

  @parameterized.parameters(
      ((4,),),
      ((None, 4),),
  )
  def test_is_normalized_exception_not_raised(self, *shape):
    """Tests that the shape exceptions of from_quaternion are not raised."""
    self.assert_exception_is_not_raised(quaternion.is_normalized, shape)

  @parameterized.parameters(
      ("'quaternion' must have 4 dimensions.", (1, 5)),)
  def test_is_normalized_exception_raised(self, error_msg, *shape):
    """Tests that the shape exceptions of from_quaternion are raised."""
    self.assert_exception_is_raised(quaternion.is_normalized, error_msg, shape)

  def test_is_normalized_random(self):
    """Tests that is_normalized works as intended."""
    random_quaternion = test_helpers.generate_random_test_quaternions()
    tensor_shape = random_quaternion.shape[:-1]
    unnormalized_random_quaternion = random_quaternion * 1.01
    quat = np.concatenate((random_quaternion, unnormalized_random_quaternion),
                          axis=0)
    mask = np.concatenate((np.ones(shape=tensor_shape + (1,), dtype=bool),
                           np.zeros(shape=tensor_shape + (1,), dtype=bool)),
                          axis=0)
    is_normalized = quaternion.is_normalized(quat)
    self.assertAllEqual(mask, is_normalized)

  @parameterized.parameters(
      ((4,),),
      ((None, 4),),
  )
  def test_normalize_exception_not_raised(self, *shape):
    """Tests that the shape exceptions of from_quaternion are not raised."""
    self.assert_exception_is_not_raised(quaternion.normalize, shape)

  @parameterized.parameters(
      ("'quaternion' must have 4 dimensions.", (1, 5)),)
  def test_normalize_exception_raised(self, error_msg, *shape):
    """Tests that the shape exceptions of from_quaternion are raised."""
    self.assert_exception_is_raised(quaternion.normalize, error_msg, shape)

  def test_normalize_random(self):
    """Tests that normalize works as intended."""
    random_quaternion = test_helpers.generate_random_test_quaternions()
    tensor_shape = random_quaternion.shape[:-1]
    unnormalized_random_quaternion = random_quaternion * 1.01
    quat = np.concatenate((random_quaternion, unnormalized_random_quaternion),
                          axis=0)
    mask = np.concatenate((np.ones(shape=tensor_shape + (1,), dtype=bool),
                           np.zeros(shape=tensor_shape + (1,), dtype=bool)),
                          axis=0)
    is_normalized = quaternion.is_normalized(quat)
    self.assertAllEqual(mask, is_normalized)
    normalized = quaternion.normalize(quat)
    is_normalized = quaternion.is_normalized(normalized)
    self.assertAllEqual(is_normalized,
                        np.ones(shape=is_normalized.shape, dtype=bool))

  @flagsaver.flagsaver(tfg_add_asserts_to_graph=False)
  def test_normalize_jacobian_preset(self):
    """Test the Jacobian of the normalize function."""
    x_init = test_helpers.generate_preset_test_quaternions()
    x = tf.convert_to_tensor(value=x_init)
    y = quaternion.normalize(x)
    self.assert_jacobian_is_correct(x, x_init, y)

  @flagsaver.flagsaver(tfg_add_asserts_to_graph=False)
  def test_normalize_jacobian_random(self):
    """Test the Jacobian of the normalize function."""
    tensor_dimensions = np.random.randint(low=1, high=3)
    tensor_shape = np.random.randint(1, 10, size=(tensor_dimensions)).tolist()
    x_init = test_helpers.generate_random_test_quaternions(tensor_shape)
    x = tf.convert_to_tensor(value=x_init)
    y = quaternion.normalize(x)
    self.assert_jacobian_is_correct(x, x_init, y)

  @parameterized.parameters(
      ((4,), (4,)),
      ((None, 4), (None, 4)),
  )
  def test_multiply_exception_not_raised(self, *shapes):
    """Tests that the shape exceptions are not raised."""
    self.assert_exception_is_not_raised(quaternion.multiply, shapes)

  @parameterized.parameters(
      ("'quaternion1' must have 4 dimensions.", (None,), (4,)),
      ("'quaternion2' must have 4 dimensions.", (4,), (None,)),
  )
  def test_multiply_exception_raised(self, error_msg, *shape):
    """Tests that the shape exceptions are raised."""
    self.assert_exception_is_raised(quaternion.multiply, error_msg, shape)

  @flagsaver.flagsaver(tfg_add_asserts_to_graph=False)
  def test_multiply_jacobian_preset(self):
    """Test the Jacobian of the multiply function."""
    x_1_init = test_helpers.generate_preset_test_quaternions()
    x_2_init = test_helpers.generate_preset_test_quaternions()
    x_1 = tf.convert_to_tensor(value=x_1_init)
    x_2 = tf.convert_to_tensor(value=x_2_init)
    y = quaternion.multiply(x_1, x_2)
    self.assert_jacobian_is_correct(x_1, x_1_init, y)
    self.assert_jacobian_is_correct(x_2, x_2_init, y)

  @flagsaver.flagsaver(tfg_add_asserts_to_graph=False)
  def test_multiply_jacobian_random(self):
    """Test the Jacobian of the multiply function."""
    tensor_dimensions = np.random.randint(low=1, high=3)
    tensor_shape = np.random.randint(1, 10, size=(tensor_dimensions)).tolist()
    x_1_init = test_helpers.generate_random_test_quaternions(tensor_shape)
    x_2_init = test_helpers.generate_random_test_quaternions(tensor_shape)
    x_1 = tf.convert_to_tensor(value=x_1_init)
    x_2 = tf.convert_to_tensor(value=x_2_init)
    y = quaternion.multiply(x_1, x_2)
    self.assert_jacobian_is_correct(x_1, x_1_init, y)
    self.assert_jacobian_is_correct(x_2, x_2_init, y)

  def test_normalized_random_initializer_raised(self):
    """Tests that the shape exceptions are raised."""
    tensor_size = np.random.randint(3)
    tensor_shape = np.random.randint(1, 10, size=(tensor_size)).tolist()
    with self.assertRaisesRegexp(ValueError, "'dtype' must be tf.float32."):
      tf.compat.v1.get_variable(
          "test_variable",
          shape=tensor_shape + [4],
          dtype=tf.uint8,
          initializer=quaternion.normalized_random_uniform_initializer(),
          use_resource=False)
    with self.assertRaisesRegexp(ValueError,
                                 "Last dimension of 'shape' must be 4."):
      tf.compat.v1.get_variable(
          "test_variable",
          shape=tensor_shape + [3],
          dtype=tf.float32,
          initializer=quaternion.normalized_random_uniform_initializer(),
          use_resource=False)

  def test_normalized_random_uniform_initializer_is_normalized(self):
    """Tests normalized_random_uniform_initializer outputs are normalized."""
    tensor_size = np.random.randint(3)
    tensor_shape = np.random.randint(1, 10, size=(tensor_size)).tolist()
    variable = tf.compat.v1.get_variable(
        "test_variable",
        shape=tensor_shape + [4],
        dtype=tf.float32,
        initializer=quaternion.normalized_random_uniform_initializer(),
        use_resource=False)
    self.evaluate(tf.compat.v1.global_variables_initializer())
    value = self.evaluate(variable)
    norms = np.linalg.norm(value, axis=-1)
    ones = np.ones(tensor_shape)
    self.assertAllClose(norms, ones, rtol=1e-3)

  def test_normalized_random_uniform_is_normalized(self):
    """Tests that the normalized_random_uniform gives normalized quaternions."""
    tensor_size = np.random.randint(3)
    tensor_shape = np.random.randint(1, 10, size=(tensor_size)).tolist()
    tensor = quaternion.normalized_random_uniform(tensor_shape)
    norms = tf.norm(tensor=tensor, axis=-1)
    ones = np.ones(tensor_shape)
    self.assertAllClose(norms, ones, rtol=1e-3)

  @parameterized.parameters(
      ((3,), (4,)),
      ((None, 3), (None, 4)),
  )
  def test_rotate_exception_not_raised(self, *shape):
    """Tests that the shape exceptions are raised."""
    self.assert_exception_is_not_raised(quaternion.rotate, shape)

  @parameterized.parameters(
      ("'point' must have 3 dimensions.", (None,), (4,)),
      ("'quaternion' must have 4 dimensions.", (3,), (None,)),
  )
  def test_rotate_exception_raised(self, error_msg, *shape):
    """Tests that the shape exceptions are raised."""
    self.assert_exception_is_raised(quaternion.rotate, error_msg, shape)

  @flagsaver.flagsaver(tfg_add_asserts_to_graph=False)
  def test_rotate_jacobian_preset(self):
    """Test the Jacobian of the rotate function."""
    x_matrix_init = test_helpers.generate_preset_test_quaternions()
    x_matrix = tf.convert_to_tensor(value=x_matrix_init)
    tensor_shape = x_matrix_init.shape[:-1] + (3,)
    x_point_init = np.random.uniform(size=tensor_shape)
    x_point = tf.convert_to_tensor(value=x_point_init)
    y = quaternion.rotate(x_point, x_matrix)
    self.assert_jacobian_is_correct(x_matrix, x_matrix_init, y)
    self.assert_jacobian_is_correct(x_point, x_point_init, y)

  @flagsaver.flagsaver(tfg_add_asserts_to_graph=False)
  def test_rotate_jacobian_random(self):
    """Test the Jacobian of the rotate function."""
    x_matrix_init = test_helpers.generate_random_test_quaternions()
    x_matrix = tf.convert_to_tensor(value=x_matrix_init)
    tensor_shape = x_matrix_init.shape[:-1] + (3,)
    x_point_init = np.random.uniform(size=tensor_shape)
    x_point = tf.convert_to_tensor(value=x_point_init)
    y = quaternion.rotate(x_point, x_matrix)
    self.assert_jacobian_is_correct(x_matrix, x_matrix_init, y)
    self.assert_jacobian_is_correct(x_point, x_point_init, y)

  def test_rotate_random(self):
    """Tests the rotation using a quaternion vs a rotation matrix."""
    random_quaternion = test_helpers.generate_random_test_quaternions()
    tensor_shape = random_quaternion.shape[:-1]
    random_point = np.random.normal(size=tensor_shape + (3,))
    rotated_point_quaternion = quaternion.rotate(random_point,
                                                 random_quaternion)
    matrix = rotation_matrix_3d.from_quaternion(random_quaternion)
    rotated_point_matrix = rotation_matrix_3d.rotate(random_point, matrix)
    self.assertAllClose(
        rotated_point_matrix, rotated_point_quaternion, rtol=1e-3)

  @parameterized.parameters(
      ((td.QUAT_ID, td.QUAT_X_45), (np.pi / 4.0,)),
      ((td.QUAT_X_45, td.QUAT_ID), (np.pi / 4.0,)),
      ((td.QUAT_Y_90, td.QUAT_Y_180), (np.pi / 2.0,)),
      ((td.QUAT_X_180, td.QUAT_Z_180), (np.pi,)),
      ((td.QUAT_X_180, -1.0 * td.QUAT_Y_180), (np.pi,)),
      ((td.QUAT_X_180, td.QUAT_X_180), (0.0,)),
      ((td.QUAT_X_180, -1 * td.QUAT_X_180), (0.0,)),
      ((td.QUAT_X_90, td.QUAT_Y_90), (2 * np.pi / 3.0,)),
      ((np.array([0., 0., 0., 1]), np.array([0., 0., 0., 1])), (0.0,)),
  )
  def test_relative_angle(self, test_inputs, test_outputs):
    """Tests quaternion relative angle."""
    self.assert_output_is_correct(quaternion.relative_angle, test_inputs,
                                  test_outputs)

  @parameterized.parameters(
      ((4,), (4,)),
      ((None, 4), (None, 4)),
      ((None, None, 4), (None, None, 4)),
  )
  def test_relative_angle_not_raised(self, *shapes):
    """Tests that the shape exceptions of relative_angle are not raised."""
    self.assert_exception_is_not_raised(quaternion.relative_angle, shapes)

  @parameterized.parameters(
      ("'quaternion1' must have 4 dimensions.", (3,), (4,)),
      ("'quaternion2' must have 4 dimensions.", (4,), (3,)),
  )
  def test_relative_angle_raised(self, error_msg, *shape):
    """Tests that the shape exceptions of relative_angle are raised."""
    self.assert_exception_is_raised(quaternion.relative_angle, error_msg, shape)

  def test_valid_relative_angle_random(self):
    """Test the output is in valid range for relative_angle function."""
    tensor_dimensions = np.random.randint(low=1, high=3)
    tensor_shape = np.random.randint(1, 10, size=(tensor_dimensions)).tolist()
    x_1_init = test_helpers.generate_random_test_quaternions(tensor_shape)
    x_2_init = test_helpers.generate_random_test_quaternions(tensor_shape)
    x_1 = tf.convert_to_tensor(value=x_1_init)
    x_2 = tf.convert_to_tensor(value=x_2_init)
    y = quaternion.relative_angle(x_1, x_2)
    self.assertAllGreaterEqual(y, 0.0)
    self.assertAllLessEqual(y, np.pi)

  @flagsaver.flagsaver(tfg_add_asserts_to_graph=False)
  def test_jacobian_relative_angle_random(self):
    """Test the Jacobian of the relative_angle function."""
    tensor_dimensions = np.random.randint(low=1, high=3)
    tensor_shape = np.random.randint(1, 10, size=(tensor_dimensions)).tolist()
    x_1_init = test_helpers.generate_random_test_quaternions(tensor_shape)
    x_2_init = test_helpers.generate_random_test_quaternions(tensor_shape)
    x_1 = tf.convert_to_tensor(value=x_1_init)
    x_2 = tf.convert_to_tensor(value=x_2_init)
    y = quaternion.relative_angle(x_1, x_2)
    self.assert_jacobian_is_correct(x_1, x_1_init, y)
    self.assert_jacobian_is_correct(x_2, x_2_init, y)

  @flagsaver.flagsaver(tfg_add_asserts_to_graph=False)
  def test_jacobian_relative_angle_preset(self):
    """Test the Jacobian of the relative_angle function."""
    x_1_init = test_helpers.generate_preset_test_quaternions()
    x_2_init = test_helpers.generate_preset_test_quaternions()
    x_1 = tf.convert_to_tensor(value=x_1_init)
    x_2 = tf.convert_to_tensor(value=x_2_init)
    y = quaternion.relative_angle(x_1, x_2)
    # relative angle is not smooth near <q1, q2> = 1, which occurs for
    # certain preset test quaternions.
    self.assert_jacobian_is_finite(x_1, x_1_init, y)
    self.assert_jacobian_is_finite(x_2, x_2_init, y)


if __name__ == "__main__":
  test_case.main()