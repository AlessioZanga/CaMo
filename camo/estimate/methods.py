from inspect import getmembers, ismethod

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

from ..utils import _as_set, _try_get

estimators = dict(getmembers(smf, ismethod))


def g_formula(
    data: pd.DataFrame,
    X: str,
    Y: str,
    Z: str = None,
    estimator: str = "ols"
) -> float:
    # Try get value from estimators
    estimator = _try_get(estimator, estimators)

    # Build the formula
    Z = _as_set(Z)
    formula = f"{Y} ~ {X}"
    if Z:
        formula += " + " + " + ".join(Z)

    # Fit the estimator
    estimator = estimator(formula, data)
    estimator = estimator.fit()

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
        estimator.predict(x)
        for x in estimates
    ]
    return estimates


def propensity_score(
    data: pd.DataFrame,
    X: str,
    Y: str,
    Z: str = None,
    estimator: str = "logit"
) -> float:
    # Try get value from estimators
    estimator = _try_get(estimator, estimators)

    Z = _as_set(Z)
    if Z:
        # Build the formula
        formula = f"{X} ~ " + " + ".join(Z)
        # Fit the estimator
        estimator = estimator(formula, data)
        estimator = estimator.fit()
        # Compute the propensity given Z
        propensity = estimator.predict(data)
    else:
        # Compute the propensity without Z
        propensity = np.mean(data[X])
        propensity = np.fill((len(data), ), propensity)

    return propensity


def ipw(
    data: pd.DataFrame,
    X: str,
    Y: str,
    Z: str = None,
    estimator: str = "logit"
) -> float:
    # Compute the propensity score
    propensity = propensity_score(data, X, Y, Z, estimator)

    # Compute the complement propensity
    complement = data.index[data[X] == 0]
    propensity[complement] = 1 - propensity[complement]

    # Estimate E[Y|do(X=0),Z] and E[Y|do(X=1),Z]
    estimates = [
        # Reweight data to get pseudo-population
        (data[X] == x) / propensity * data[Y]
        for x in (0, 1)
    ]
    return estimates
