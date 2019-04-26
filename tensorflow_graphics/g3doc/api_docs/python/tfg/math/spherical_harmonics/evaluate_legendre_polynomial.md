<div itemscope itemtype="http://developers.google.com/ReferenceObject">
<meta itemprop="name" content="tfg.math.spherical_harmonics.evaluate_legendre_polynomial" />
<meta itemprop="path" content="Stable" />
</div>

# tfg.math.spherical_harmonics.evaluate_legendre_polynomial

Evaluates the Legendre polynomial of degree l and order m at x.

``` python
tfg.math.spherical_harmonics.evaluate_legendre_polynomial(
    l,
    m,
    x
)
```



Defined in [`math/spherical_harmonics.py`](https://cs.corp.google.com/#piper///depot/google3/third_party/py/tensorflow_graphics/math/spherical_harmonics.py).

<!-- Placeholder for "Used in" -->

Note:
  This function is implementating the algorithm described p. 10 of `Spherical
  Harmonic Lighting: The Gritty Details`.

Note:
  In the following, A1 to An are optional batch dimensions.

#### Args:

* <b>`l`</b>: A tensor of shape `[A1, ..., An]` corresponding to the degree of the
    associated Legendre polynomial. Note that `l` must satisfy `l >= 0`.
* <b>`m`</b>: A tensor of shape `[A1, ..., An]` corresponding to the order of the
    associated Legendre polynomial. Note that `m` must satisfy `0 <= m <= l`.
* <b>`x`</b>: A tensor of shape `[A1, ..., An]` with values in [-1,1].


#### Returns:

A tensor of shape `[A1, ..., An]` containing the evaluation of the legendre
polynomial.