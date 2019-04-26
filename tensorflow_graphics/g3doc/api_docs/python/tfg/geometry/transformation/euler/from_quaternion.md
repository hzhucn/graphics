<div itemscope itemtype="http://developers.google.com/ReferenceObject">
<meta itemprop="name" content="tfg.geometry.transformation.euler.from_quaternion" />
<meta itemprop="path" content="Stable" />
</div>

# tfg.geometry.transformation.euler.from_quaternion

Converts quaternions to Euler angles.

``` python
tfg.geometry.transformation.euler.from_quaternion(
    quaternions,
    name=None
)
```



Defined in [`geometry/transformation/euler.py`](https://github.com/tensorflow/agents/tree/master/tensorflow_graphics/geometry/transformation/euler.py).

<!-- Placeholder for "Used in" -->

#### Args:

* <b>`quaternions`</b>: A tensor of shape `[A1, ..., An, 4]`, where the last dimension
    represents a normalized quaternion.
* <b>`name`</b>: A name for this op that defaults to "euler_from_quaternion".


#### Returns:

A tensor of shape `[A1, ..., An, 3]`, where the last dimension represents
the three Euler angles.