from typing import Any, Set

import numpy as np
import pandas as pd

from tqdm import trange

from .estimators import AbstractEstimator, ESTIMATORS
from ..utils import _try_get


class AverageCausalEffect(AbstractEstimator):

    def __init__(self, estimator: str = "g_formula", *args, **kwargs):
        super().__init__(estimator, ESTIMATORS)
        self._estimator = self._estimator(*args, **kwargs)

    def fit(self, data: pd.DataFrame, X: str, Y: str, Z: Set[str] = None) -> Any:
        self._estimator = self._estimator.fit(data, X, Y, Z)
        return self

    def predict(self, data: pd.DataFrame, X: str, Y: str, Z: Set[str] = None) -> Any:
        # Estimate E[Y|do(X=1),Z] and E[Y|do(X=0),Z]
        Y1, Y0 = self._estimator.predict(data, X, Y, Z)
        # ACE = E_Z[ E[Y|do(X=1),Z] - E[Y|do(X=0),Z] ]
        return np.mean(Y1 - Y0)

    """
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
                estimator
            )
        # Compute upper and lower bounds over samples
        lower, upper = np.quantile(samples, q=[alpha/2, 1-alpha/2])
        # Compute the ACE bias
        bias = np.mean(samples) - ace
        # Return ACE with confidence bounds
        return ace, lower, upper, bias

    return ace

    def __init__(
        bootstrap: int = None,
        alpha: float = 0.05
    ):
        pass
    """
