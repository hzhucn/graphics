<div itemscope itemtype="http://developers.google.com/ReferenceObject">
<meta itemprop="name" content="tfg.math.interpolation.bspline.interpolate" />
<meta itemprop="path" content="Stable" />
</div>

# tfg.math.interpolation.bspline.interpolate

Applies B-spline interpolation to input control points (knots).

``` python
tfg.math.interpolation.bspline.interpolate(
    knots,
    positions,
    degree,
    cyclical,
    name=None
)
```



Defined in [`math/interpolation/bspline.py`](https://cs.corp.google.com/#piper///depot/google3/third_party/py/tensorflow_graphics/math/interpolation/bspline.py).

<!-- Placeholder for "Used in" -->

Note:
  In the following, A1 to An, and B1 to Bk are optional batch dimensions.

#### Args:

* <b>`knots`</b>: A tensor with shape `[B1, ..., Bk, num_knots]` containing knot
    values.
* <b>`positions`</b>: Tensor with shape `[A1, .. An, num_splines]`. Positions must be
    between [0, num_knots-`degree`) for non-cyclical and [0, num_knots) for
    cyclical splines.
* <b>`degree`</b>: An `int` between 0 and 4, or an enumerated constant from the Degree
    class, which is the degree of the splines.
* <b>`cyclical`</b>: A `bool`, whether the splines are cyclical.
* <b>`name`</b>: A name for this op. Defaults to "bspline_interpolate".


#### Returns:

A tensor of shape `[A1, ... An, B1, ..., Bk]`, which is the result of spline
interpolation.