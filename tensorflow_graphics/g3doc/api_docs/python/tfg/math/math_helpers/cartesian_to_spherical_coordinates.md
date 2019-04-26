<div itemscope itemtype="http://developers.google.com/ReferenceObject">
<meta itemprop="name" content="tfg.math.math_helpers.cartesian_to_spherical_coordinates" />
<meta itemprop="path" content="Stable" />
</div>

# tfg.math.math_helpers.cartesian_to_spherical_coordinates

Function to transform Cartesian coordinates to spherical coordinates.

``` python
tfg.math.math_helpers.cartesian_to_spherical_coordinates(
    point_cartesian,
    name=None
)
```



Defined in [`math/math_helpers.py`](https://cs.corp.google.com/#piper///depot/google3/third_party/py/tensorflow_graphics/math/math_helpers.py).

<!-- Placeholder for "Used in" -->

Note:
  In the following, A1 to An are optional batch dimensions.

#### Args:

* <b>`point_cartesian`</b>: A tensor of shape `[A1, ..., An, 3]`. In the last
    dimension, the data follows the x,y,z order.
* <b>`name`</b>: A name for this op. Defaults to 'cartesian_to_spherical_coordinates'.


#### Returns:

A tensor of shape `[A1, ..., An, 3]`. The last dimensions contains
(r,theta,phi), where r is the sphere radius, theta the polar angle and phi
the azimuthal angle.