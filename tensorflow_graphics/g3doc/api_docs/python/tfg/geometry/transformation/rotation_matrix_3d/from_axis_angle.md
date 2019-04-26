<div itemscope itemtype="http://developers.google.com/ReferenceObject">
<meta itemprop="name" content="tfg.geometry.transformation.rotation_matrix_3d.from_axis_angle" />
<meta itemprop="path" content="Stable" />
</div>

# tfg.geometry.transformation.rotation_matrix_3d.from_axis_angle

Convert an axis-angle representation to a rotation matrix.

``` python
tfg.geometry.transformation.rotation_matrix_3d.from_axis_angle(
    axis,
    angle,
    name=None
)
```



Defined in [`geometry/transformation/rotation_matrix_3d.py`](https://github.com/tensorflow/agents/tree/master/tensorflow_graphics/geometry/transformation/rotation_matrix_3d.py).

<!-- Placeholder for "Used in" -->

Note:
  In the following, A1 to An are optional batch dimensions.

#### Args:

* <b>`axis`</b>: A tensor of shape `[A1, ..., An, 3]`, where the last dimension
    represents a normalized axis.
* <b>`angle`</b>: A tensor of shape `[A1, ..., An, 1]`, where the last dimension
    represents a normalized axis.
* <b>`name`</b>: A name for this op that defaults to
    "rotation_matrix_3d_from_axis_angle".


#### Returns:

A tensor of shape `[A1, ..., An, 3, 3]`, where the last two dimensions
represents a 3d rotation matrix.


#### Raises:

* <b>`ValueError`</b>: If the shape of `axis` or `angle` is not supported.