from functools import partial
from multiprocessing import Pool, cpu_count
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


class AverageCausalEffectBootstrap(AverageCausalEffect):

    _parameters: Any
    _processes: int
    _bootstrap: int
    _alpha: float

    def __init__(
        self,
        bootstrap: int,
        alpha: float = 0.05,
        processes: int = None,
        estimator: str = "g_formula",
        *args,
        **kwargs
    ):
        super().__init__(estimator)
        self._parameters = partial(
            AverageCausalEffect, estimator, *args, **kwargs
        )
        self._processes = processes if processes else cpu_count()
        self._bootstrap = bootstrap
        self._alpha = alpha

    def _predict_sample(self, estimator, data, X, Y, Z):
        # Sample from dataset with replacement
        sample = data.sample(len(data), replace=True)
        sample.reset_index(drop=True, inplace=True)
        # Compute ACE for each sample
        return estimator().fit_predict(sample, X, Y, Z)

    def predict(self, data: pd.DataFrame, X: str, Y: str, Z: Set[str] = None) -> Any:
        # Compute ACE for input data
        ACE = super().predict(data, X, Y, Z)
        # Initialize multiprocessing pool
        pool = Pool(self._processes)
        # Apply parallel worker async
        pool = pool.istarmap(self._predict_sample, (    # pylint: disable=no-member
            (self._parameters, data, X, Y, Z)
            for _ in trange(self._bootstrap)
        ))
        # Compute samples vector
        samples = np.empty(self._bootstrap)
        for i, v in enumerate(pool): samples[i] = v
        # Compute upper and lower bounds over samples
        q = [self._alpha / 2, 1 - self._alpha / 2]
        lower, upper = np.quantile(samples, q=q)
        # Compute the ACE bias
        bias = np.mean(samples) - ACE
        # Return ACE with confidence bounds and bias
        return ACE, lower, upper, bias
