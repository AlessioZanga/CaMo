from inspect import getmembers, ismethod
from typing import Any, Tuple

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

from ..utils import _as_set, _try_get

regressors = dict(getmembers(smf, ismethod))


def g_formula(
    data: pd.DataFrame,
    X: str,
    Y: str,
    Z: str = None,
    regressor: str = "ols"
) -> float:
    # Try get value from regressors
    regressor = _try_get(regressor, regressors)

    # Build the formula
    Z = _as_set(Z)
    formula = f"{Y} ~ {X}"
    if Z:
        formula += " + " + " + ".join(Z)

    # Fit the regressor
    regressor = regressor(formula, data)
    regressor = regressor.fit()

    # Helper function
    def _fill_copy(data, x):
        data = data[[X, *Z]].copy()
        data[X] = x
        return data

    # Estimate E[Y|do(X=0),Z] and E[Y|do(X=1),Z]
    estimates = (
        _fill_copy(data, x)
        for x in (0, 1)
    )
    estimates = [
        regressor.predict(x)
        for x in estimates
    ]
    return estimates


def ipw(
    data: pd.DataFrame,
    X: str,
    Y: str,
    Z: str = None,
    regressor: str = "ols"
) -> float:
    raise NotImplementedError()  # TODO
