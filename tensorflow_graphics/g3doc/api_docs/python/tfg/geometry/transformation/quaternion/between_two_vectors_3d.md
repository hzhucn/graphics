<div itemscope itemtype="http://developers.google.com/ReferenceObject">
<meta itemprop="name" content="tfg.geometry.transformation.quaternion.between_two_vectors_3d" />
<meta itemprop="path" content="Stable" />
</div>

# tfg.geometry.transformation.quaternion.between_two_vectors_3d

Computes quaternion over the shortest arc between two vectors.

``` python
tfg.geometry.transformation.quaternion.between_two_vectors_3d(
    vector1,
    vector2,
    name=None
)
```



Defined in [`geometry/transformation/quaternion.py`](https://github.com/tensorflow/agents/tree/master/tensorflow_graphics/geometry/transformation/quaternion.py).

<!-- Placeholder for "Used in" -->

Result quaternion describes shortest geodesic rotation from
vector1 to vector2.

Note:
  In the following, A1 to An are optional batch dimensions.

#### Args:

* <b>`vector1`</b>: A tensor of shape `[A1, ..., An, 3]`, where the last dimension
    represents the first vector.
* <b>`vector2`</b>: A tensor of shape `[A1, ..., An, 3]`, where the last dimension
    represents the second vector.
* <b>`name`</b>: A name for this op that defaults to
    "quaternion_between_two_vectors_3d".


#### Returns:

A tensor of shape `[A1, ..., An, 4]`, where the last dimension represents
a normalized quaternion.


#### Raises:

* <b>`ValueError`</b>: If the shape of `vector1` or `vector2` is not supported.