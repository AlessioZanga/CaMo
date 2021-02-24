import sys
from functools import partial
from typing import Optional, Set

import numpy as np
import pandas as pd
from scipy.stats import chi2, chi2_contingency, norm, t

from ..utils import _as_set

CONDITIONAL_INDEPENDENCE_TESTS = {
    "chi_squared": "pearson",
    "g_test": "log-likelihood",
    "modified_log_likelihood": "mod-log-likelihood",
    "freeman_tukey": "freeman-tukey",
    "neyman": "neyman",
    "cressie_read": "cressie-read"
}

EPS = np.finfo(float).eps


def _power_divergence(
    data: pd.DataFrame,
    X: str,
    Y: str,
    Z: Set[str],
    method: Optional[str] = None
    ):
    Z = list(_as_set(Z))

    # Group data by Z
    data = [data] if not Z else (d for _, d in data.groupby(Z))
    # For each group compute the absolute frequency
    data = (d.groupby([X, Y]).size().unstack(Y, 0) for d in data)
    # Apply the selected contional indepependece test
    data = (chi2_contingency(d + EPS, lambda_=method) for d in data)
    # Reduce results among groups by using column-wise sum,
    # discarding unnecessary results
    data = np.vstack([d[:3] for d in data]).sum(axis=0)
    # Recompute p_value using chi and dof values
    data[1] = 1 - chi2.cdf(data[0], df=data[2])
    return data


for key, value in CONDITIONAL_INDEPENDENCE_TESTS.items():
    setattr(
        sys.modules[__name__],
        key,
        partial(_power_divergence, method=value)
    )


def partial_correlation(data: pd.DataFrame, X: str, Y: str, Z: Set[str]):
    Z = list(_as_set(Z))

    # Standardize selected data
    data = data[[X] + [Y] + Z]
    data = (data - data.mean(axis=0)) / data.std(axis=0)

    if len(Z) == 0:
        res_X, res_Y = [data[v].to_numpy() for v in (X, Y)]
    else:
        X, Y, Z = [data[v].to_numpy() for v in (X, Y, Z)]
        Z = Z if len(Z.shape) > 1 else Z[:, None]
        beta_X = np.linalg.lstsq(Z, X, rcond=None)[0]
        beta_Y = np.linalg.lstsq(Z, Y, rcond=None)[0]
        res_X = X - Z @ beta_X
        res_Y = Y - Z @ beta_Y

    return np.corrcoef(res_X, res_Y)[0, 1]


def t_student(data: pd.DataFrame, X: str, Y: str, Z: Set[str]):
    Z = _as_set(Z)

    stat = partial_correlation(data, X, Y, Z)

    df = np.max(len(data) - len(Z) - 2, 0)
    tran = np.sqrt(df) * np.abs(stat / (np.sqrt(1 - np.square(stat)) + EPS))
    p_value = 2 * (1 - t.cdf(tran, df))

    return stat, p_value, df


def z_fisher(data: pd.DataFrame, X: str, Y: str, Z: Set[str]):
    Z = _as_set(Z)

    stat = partial_correlation(data, X, Y, Z)

    df = np.max(len(data) - len(Z) - 3, 0)
    stat = np.sqrt(df) * np.abs(np.arctanh(stat + EPS))
    p_value = 2 * (1 - norm.cdf(stat))

    return stat, p_value, df
