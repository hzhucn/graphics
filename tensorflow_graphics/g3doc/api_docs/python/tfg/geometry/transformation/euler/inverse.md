<div itemscope itemtype="http://developers.google.com/ReferenceObject">
<meta itemprop="name" content="tfg.geometry.transformation.euler.inverse" />
<meta itemprop="path" content="Stable" />
</div>

# tfg.geometry.transformation.euler.inverse

Computes the angles that would inverse a transformation by euler_angle.

``` python
tfg.geometry.transformation.euler.inverse(
    euler_angle,
    name=None
)
```



Defined in [`geometry/transformation/euler.py`](https://cs.corp.google.com/#piper///depot/google3/third_party/py/tensorflow_graphics/geometry/transformation/euler.py).

<!-- Placeholder for "Used in" -->

Note:
  In the following, A1 to An are optional batch dimensions.

#### Args:

* <b>`euler_angle`</b>: A tensor of shape `[A1, ..., An, 3]`, where the last dimension
    represents the three Euler angles.
* <b>`name`</b>: A name for this op that defaults to "euler_inverse".


#### Returns:

A tensor of shape `[A1, ..., An, 3]`, where the last dimension represents
the three Euler angles.


#### Raises:

* <b>`ValueError`</b>: If the shape of `euler_angle` is not supported.