<div itemscope itemtype="http://developers.google.com/ReferenceObject">
<meta itemprop="name" content="tfg.image.color_space.srgb.from_linear" />
<meta itemprop="path" content="Stable" />
</div>

# tfg.image.color_space.srgb.from_linear

Converts linear colors to sRGB colors.

``` python
tfg.image.color_space.srgb.from_linear(
    linear,
    gamma=2.4,
    name=None
)
```



Defined in [`image/color_space/srgb.py`](https://cs.corp.google.com/#piper///depot/google3/third_party/py/tensorflow_graphics/image/color_space/srgb.py).

<!-- Placeholder for "Used in" -->

Note:
    In the following, A1 to An are optional batch dimensions.

#### Args:

* <b>`linear`</b>: A Tensor of shape `[A_1, ..., A_n, 3]`, where the last dimension
    represents RGB values in the range [0, 1] in linear color space.
* <b>`gamma`</b>: A float gamma value to use for the conversion.
* <b>`name`</b>: A name for this op that defaults to "srgb_from_linear".


#### Raises:

* <b>`ValueError`</b>: If `linear` has rank < 1 or has its last dimension not equal to
    3.


#### Returns:

A tensor of shape `[A_1, ..., A_n, 3]`, where the last dimension represents
sRGB values.