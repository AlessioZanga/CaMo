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

    data = [data] if not Z else (d for _, d in data.groupby(Z))
    data = (d.groupby([X, Y]).size().unstack(Y, 0) for d in data)
    data = (chi2_contingency(d, lambda_=method) for d in data)
    data = np.vstack([np.array(d[:3]) for d in data]).sum(axis=0)
    data[1] = 1 - chi2.cdf(data[0], df=data[2])
    return data


for key, value in CONDITIONAL_INDEPENDENCE_TESTS.items():
    setattr(
        sys.modules[__name__],
        key,
        partial(_power_divergence, method=value)
    )
