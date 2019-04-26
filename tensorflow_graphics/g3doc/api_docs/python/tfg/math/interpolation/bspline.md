<div itemscope itemtype="http://developers.google.com/ReferenceObject">
<meta itemprop="name" content="tfg.math.interpolation.bspline" />
<meta itemprop="path" content="Stable" />
</div>

# Module: tfg.math.interpolation.bspline

Tensorflow.graphics B-spline interpolation module.



Defined in [`math/interpolation/bspline.py`](https://cs.corp.google.com/#piper///depot/google3/third_party/py/tensorflow_graphics/math/interpolation/bspline.py).

<!-- Placeholder for "Used in" -->

This module supports cardinal B-spline interpolation up to degree 4, with up
to C3 smoothness. It has functions to calculate basis functions, control point
weights, and the final interpolation.

## Classes

[`class Degree`](../../../tfg/math/interpolation/bspline/Degree.md): Defines valid degrees for B-spline interpolation.

## Functions

[`interpolate(...)`](../../../tfg/math/interpolation/bspline/interpolate.md): Applies B-spline interpolation to input control points (knots).

[`interpolate_with_weights(...)`](../../../tfg/math/interpolation/bspline/interpolate_with_weights.md): Interpolates knots using knot weights.

[`knot_weights(...)`](../../../tfg/math/interpolation/bspline/knot_weights.md): Function that converts cardinal B-spline positions to knot weights.

