<div itemscope itemtype="http://developers.google.com/ReferenceObject">
<meta itemprop="name" content="tfg.geometry.transformation.quaternion.relative_angle" />
<meta itemprop="path" content="Stable" />
</div>

# tfg.geometry.transformation.quaternion.relative_angle

Computes the unsigned relative rotation angle between 2 unit quaternions.

``` python
tfg.geometry.transformation.quaternion.relative_angle(
    quaternion1,
    quaternion2,
    name=None
)
```



Defined in [`geometry/transformation/quaternion.py`](https://cs.corp.google.com/#piper///depot/google3/third_party/py/tensorflow_graphics/geometry/transformation/quaternion.py).

<!-- Placeholder for "Used in" -->

Given two normalized quanternions $$\mathbf{q}_1$$ and $$\mathbf{q}_2$$, the
relative angle is computed as
$$\theta = 2\arccos(\mathbf{q}_1^T\mathbf{q}_2)$$.

Note:
  In the following, A1 to An are optional batch dimensions.

#### Args:

* <b>`quaternion1`</b>: A tensor of shape `[A1, ..., An, 4]`, where the last dimension
    represents a normalized quaternion.
* <b>`quaternion2`</b>: A tensor of shape `[A1, ..., An, 4]`, where the last dimension
    represents a normalized quaternion.
* <b>`name`</b>: A name for this op that defaults to "quaternion_relative_angle".


#### Returns:

A tensor of shape `[A1, ..., An, 1]` where the last dimension represents
rotation angles in the range [0.0, pi].


#### Raises:

* <b>`ValueError`</b>: If the shape of `quaternion1` or `quaternion2` is not supported.