from inspect import getmembers, isfunction
from typing import Any, Tuple

import numpy as np
import pandas as pd

from . import estimators
from ..utils import _as_set, _to_categorical, _try_get

estimators = dict(getmembers(estimators, isfunction))


def average_causal_effect(
    data: pd.DataFrame,
    X: str,
    Y: str,
    Z: str = None,
    estimator: str = "g_formula",
    regressor: str = "ols",
    targets: Tuple[Any] = (0, 1)
) -> float:
    # Try get value from estimators
    estimator = _try_get(estimator, estimators)

    # Check if data is numeric
    is_numeric = np.vectorize(lambda x: not np.issubdtype(x, np.number))
    is_numeric = is_numeric(data.dtypes)
    # Tranform not numeric columns and targets using one-hot encoding
    if np.any(is_numeric):
        data.iloc[:, is_numeric], encoders = _to_categorical(data.iloc[:, is_numeric])
        targets = encoders[X].transform(targets) if X in encoders else targets

    # Estimate E[Y|do(X=0),Z] and E[Y|do(X=1),Z]
    effect_0, effect_1 = estimator(data, X, Y, Z, regressor)

    # ACE = E_Z[ E[Y|do(X=1),Z] - E[Y|do(X=0),Z] ]
    return np.mean(effect_1 - effect_0)


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
