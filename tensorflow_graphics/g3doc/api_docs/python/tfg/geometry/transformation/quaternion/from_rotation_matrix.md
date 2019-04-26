<div itemscope itemtype="http://developers.google.com/ReferenceObject">
<meta itemprop="name" content="tfg.geometry.transformation.quaternion.from_rotation_matrix" />
<meta itemprop="path" content="Stable" />
</div>

# tfg.geometry.transformation.quaternion.from_rotation_matrix

Converts a rotation matrix representation to a quaternion.

``` python
tfg.geometry.transformation.quaternion.from_rotation_matrix(
    rotation_matrix,
    name=None
)
```



Defined in [`geometry/transformation/quaternion.py`](https://github.com/tensorflow/agents/tree/master/tensorflow_graphics/geometry/transformation/quaternion.py).

<!-- Placeholder for "Used in" -->

Warning:
  This function is not smooth everywhere.

Note:
  In the following, A1 to An are optional batch dimensions.

#### Args:

* <b>`rotation_matrix`</b>: A tensor of shape `[A1, ..., An, 3, 3]`, where the last two
    dimensions represent a rotation matrix.
* <b>`name`</b>: A name for this op that defaults to "quaternion_from_rotation_matrix".


#### Returns:

A tensor of shape `[A1, ..., An, 4]`, where the last dimension represents
a normalized quaternion.


#### Raises:

* <b>`ValueError`</b>: If the shape of `rotation_matrix` is not supported.