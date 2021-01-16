from inspect import getmembers, isfunction
from typing import Any, Tuple

import numpy as np
import pandas as pd

from tqdm import trange

from . import methods
from ..utils import _to_categorical, _try_get

methods = dict(getmembers(methods, isfunction))


def average_causal_effect(
    data: pd.DataFrame,
    X: str,
    Y: str,
    Z: str = None,
    method: str = "g_formula",
    estimator: str = "ols",
    targets: Tuple[Any] = (0, 1),
    bootstrap: int = None,
    alpha: float = 0.05
) -> float:
    # Try get value from methods
    if isinstance(method, str):
        method = _try_get(method, methods)

    # Check if data is numeric
    is_numeric = np.vectorize(lambda x: not np.issubdtype(x, np.number))
    is_numeric = is_numeric(data.dtypes)
    # Tranform not numeric columns and targets using one-hot encoding
    if np.any(is_numeric):
        data.iloc[:, is_numeric], encoders = _to_categorical(data.iloc[:, is_numeric])
        targets = encoders[X].transform(targets) if X in encoders else targets

    # Estimate E[Y|do(X=0),Z] and E[Y|do(X=1),Z]
    effect_0, effect_1 = method(data, X, Y, Z, estimator)

    # ACE = E_Z[ E[Y|do(X=1),Z] - E[Y|do(X=0),Z] ]
    ace = np.mean(effect_1 - effect_0)

    # If bootstrap sample size is specified estimate
    # the confidence interval and the bias
    if bootstrap:
        # Preallocate samples vector
        samples = np.empty((bootstrap, ))
        # For each bootstrap sample
        for i in trange(bootstrap):
            # Sample from dataset with replacement
            sample = data.sample(len(data), replace=True)
            sample.reset_index(drop=True, inplace=True)
            # Call ACE recursively
            samples[i] = average_causal_effect(
                sample,
                X, Y, Z,
                method,
                estimator,
                targets
            )
        # Compute upper and lower bounds over samples
        lower, upper = np.quantile(samples, q=[alpha/2, 1-alpha/2])
        # Compute the ACE bias
        bias = np.mean(samples) - ace
        # Return ACE with confidence bounds
        return ace, lower, upper, bias
    
    return ace


def total_effect() -> float:
    # TE = E[Y|do(X=1)] - E[Y|do(X=0)]
    raise NotImplementedError() # TODO


def direct_effect() -> float:
    # DE = E[Y|do(X=x,Z=z)] - E[Y|do(X=x',Z=z)]
    raise NotImplementedError() # TODO


def indirect_effect() -> float:
    raise NotImplementedError() # TODO


def controlled_direct_effect() -> float:
    # CDE = E[Y|do(X=1,Z=z)] - E[Y|do(X=0,Z=z)]
    raise NotImplementedError() # TODO


def natural_direct_effect() -> float:
    raise NotImplementedError() # TODO


def natural_indirect_effect() -> float:
    raise NotImplementedError() # TODO
