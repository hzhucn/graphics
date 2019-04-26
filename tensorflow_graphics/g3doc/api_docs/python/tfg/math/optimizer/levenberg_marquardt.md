<div itemscope itemtype="http://developers.google.com/ReferenceObject">
<meta itemprop="name" content="tfg.math.optimizer.levenberg_marquardt" />
<meta itemprop="path" content="Stable" />
</div>

# Module: tfg.math.optimizer.levenberg_marquardt

This module implements a Levenberg-Marquardt optimizer.



Defined in [`math/optimizer/levenberg_marquardt.py`](https://cs.corp.google.com/#piper///depot/google3/third_party/py/tensorflow_graphics/math/optimizer/levenberg_marquardt.py).

<!-- Placeholder for "Used in" -->

Minimizes $$\min_{\mathbf{x}} \sum_i \|\mathbf{r}_i(\mathbf{x})\|^2_2$$ where
$$\mathbf{r}_i(\mathbf{x})$$
are the residuals. This function implements Levenberg-Marquardt, an iterative
process that linearizes the residuals and iteratively finds a displacement
$$\Delta \mathbf{x}$$ such that at iteration $$t$$ an update
$$\mathbf{x}_{t+1} = \mathbf{x}_{t} + \Delta \mathbf{x}$$ improving the
loss can be computed. The displacement is computed by solving an optimization
problem
$$\min_{\Delta \mathbf{x}} \sum_i
\|\mathbf{J}_i(\mathbf{x}_{t})\Delta\mathbf{x} +
\mathbf{r}_i(\mathbf{x}_t)\|^2_2 + \lambda\|\Delta \mathbf{x} \|_2^2$$ where
$$\mathbf{J}_i(\mathbf{x}_{t})$$ is the Jacobian of $$\mathbf{r}_i$$ computed at
$$\mathbf{x}_t$$, and $$\lambda$$ is a scalar weight.

More details on Levenberg-Marquardt can be found on [this page.]
(https://en.wikipedia.org/wiki/Levenberg%E2%80%93Marquardt_algorithm)

## Functions

[`minimize(...)`](../../../tfg/math/optimizer/levenberg_marquardt/minimize.md): Minimizes a set of residuals in the least-squares sense.

