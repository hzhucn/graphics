<div itemscope itemtype="http://developers.google.com/ReferenceObject">
<meta itemprop="name" content="tfg.geometry.convolution.utils.check_valid_graph_pooling_input" />
<meta itemprop="path" content="Stable" />
</div>

# tfg.geometry.convolution.utils.check_valid_graph_pooling_input

Checks that the inputs are valid for graph pooling.

``` python
tfg.geometry.convolution.utils.check_valid_graph_pooling_input(
    data,
    pool_map,
    sizes
)
```



Defined in [`geometry/convolution/utils.py`](https://github.com/tensorflow/graphics/blob/master/tensorflow_graphics/geometry/convolution/utils.py).

<!-- Placeholder for "Used in" -->

#### Note:

In the following, A1 to An are optional batch dimensions.


#### Args:

* <b>`data`</b>: A `float` tensor with shape `[A1, ..., An, V1, C]`.
* <b>`pool_map`</b>: A SparseTensor with the same type as `data` and with shape
  `[A1, ..., An, V2, V1]`.
* <b>`sizes`</b>: An `int` tensor of shape `[A1, ..., An, 2]`. Can be `None`.


#### Raises:

* <b>`TypeError`</b>: if the input types are invalid.
* <b>`ValueError`</b>: if the input dimensions are invalid.