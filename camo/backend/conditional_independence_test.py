import sys
from functools import partial
from typing import Set

import numpy as np
import pandas as pd
from scipy.stats import chi2, chi2_contingency

from ..utils import _as_set

CONDITIONAL_INDEPENDENCE_TESTS = {
    "chi_square": "pearson",
    "g_test": "log-likelihood",
    "modified_log_likelihood": "mod-log-likelihood",
    "freeman_tukey": "freeman-tukey",
    "neyman": "neyman",
    "cressie_read": "cressie-read"
}


def _power_divergence(data: pd.DataFrame, X: str, Y: str, Z: Set[str] = None, method: str = None):
    Z = list(_as_set(Z))

    # Group data by Z
    data = [data] if not Z else (d for _, d in data.groupby(Z))
    # For each group compute the absolute frequency
    data = (d.groupby([X, Y]).size().unstack(Y, 0) for d in data)
    # Apply the selected contional indepependece test
    data = (chi2_contingency(d, lambda_=method) for d in data)
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
