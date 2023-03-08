# Copyright 2018 The JAX Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import scipy.stats as osp_stats

from jax import lax
import jax.numpy as jnp
from jax._src.lax.lax import _const as _lax_const
from jax._src.numpy.util import _wraps, _promote_args_inexact
from jax._src.typing import Array, ArrayLike


@_wraps(osp_stats.pareto.logpdf, update_doc=False)
def logpdf(x: ArrayLike, b: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  x, b, loc, scale = _promote_args_inexact("pareto.logpdf", x, b, loc, scale)
  one = _lax_const(x, 1)
  scaled_x = lax.div(lax.sub(x, loc), scale)
  normalize_term = lax.log(lax.div(scale, b))
  log_probs = lax.neg(lax.add(normalize_term, lax.mul(lax.add(b, one), lax.log(scaled_x))))
  return jnp.where(lax.lt(x, lax.add(loc, scale)), -jnp.inf, log_probs)

@_wraps(osp_stats.pareto.pdf, update_doc=False)
def pdf(x: ArrayLike, b: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  return lax.exp(logpdf(x, b, loc, scale))
