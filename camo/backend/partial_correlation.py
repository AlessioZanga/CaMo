from typing import Set

import numpy as np
import pandas as pd

from ..utils import _as_set


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


def fast_partial_correlation(cov: pd.DataFrame, X: str, Y: str, Z: Set[str]):
    Z = _as_set(Z)
    mask = [X, Y, *Z]
    cov = cov.loc[mask, mask]

    out = 0.0

    try:
        U, S, VT = np.linalg.svd(cov)
    except np.linalg.LinAlgError:
        return out

    EPS = len(cov) * S[0] * np.finfo(float).eps ** 2
    mask = S > EPS

    # Since covariance matrix as been rearrenged cov[[X, Y, *Z]],
    # X and Y are mapped to index 0 and 1

    k00 = np.sum(U[0, mask] * VT[mask, 0] / S[mask])
    k01 = np.sum(U[0, mask] * VT[mask, 1] / S[mask])
    k11 = np.sum(U[1, mask] * VT[mask, 1] / S[mask])

    if k00 < EPS or k11 < EPS:
        return out

    out = -k01 / np.sqrt(k00 * k11)
    out = np.clip(out, -1.0, 1.0)

    return out
