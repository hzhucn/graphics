<div itemscope itemtype="http://developers.google.com/ReferenceObject">
<meta itemprop="name" content="tfg.geometry.transformation.rotation_matrix_2d.rotate" />
<meta itemprop="path" content="Stable" />
</div>

# tfg.geometry.transformation.rotation_matrix_2d.rotate

Rotates a 2d point using a 2d rotation matrix.

``` python
tfg.geometry.transformation.rotation_matrix_2d.rotate(
    point,
    matrix,
    name=None
)
```



Defined in [`geometry/transformation/rotation_matrix_2d.py`](https://github.com/tensorflow/agents/tree/master/tensorflow_graphics/geometry/transformation/rotation_matrix_2d.py).

<!-- Placeholder for "Used in" -->

Note:
  In the following, A1 to An are optional batch dimensions.

#### Args:

* <b>`point`</b>: A tensor of shape `[A1, ..., An, 2]`, where the last dimension
    represents a 2d point.
* <b>`matrix`</b>: A tensor of shape `[A1, ..., An, 2, 2]`, where the last dimension
    represents a 2d rotation matrix.
* <b>`name`</b>: A name for this op that defaults to "rotation_matrix_2d_rotate".


#### Returns:

A tensor of shape `[A1, ..., An, 2]`, where the last dimension
  represents a 2d point.


#### Raises:

* <b>`ValueError`</b>: If the shape of `point` or `matrix` is not supported.