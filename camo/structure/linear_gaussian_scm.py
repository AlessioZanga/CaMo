from functools import partial
from typing import Any, Dict, Iterable, Optional

import numpy as np
import pandas as pd

from .linear_scm import LinearSCM


class LinearGaussianSCM(LinearSCM):

    _Sigma: pd.Series

    def __init__(
        self,
        V: Optional[Iterable[str]] = None,
        Beta: Optional[np.array] = None,
        Gamma: Optional[np.array] = None,
        Sigma: Optional[np.array] = None
    ):
        super().__init__(V, Beta, Gamma)

        # Build vector of noise variances
        self._Sigma = np.ones((1, len(self._Gamma))) if Sigma is None else Sigma
        self._Sigma = pd.DataFrame(self._Sigma, columns=self._Gamma.index, copy=True)

    def copy(self):
        return type(self)(
            self._Beta.index, self._Beta, self._Gamma, self._Sigma
        )

    @property
    def P(self) -> Dict[str, Any]:
        return self._Sigma.apply(
            lambda x: partial(np.random.normal, scale=np.sqrt(x))
        ).to_dict()

    @property
    def Sigma(self) -> pd.DataFrame:
        return self._Sigma.copy()

    def sample(self, size: int, seed: Optional[int] = None) -> pd.DataFrame:
        # Set random seed
        np.random.seed(seed)
        # Generate noise from normal distribution given sigma variance matrix
        samples = lambda x: np.random.normal(scale=np.sqrt(x), size=size)
        samples = self._Sigma.apply(samples)
        # Compute noise for each variable given gamma matrix
        samples = samples @ self._Gamma
        # Mask noise given fixed interventions
        mask = self._Do.columns[~self._Do.isnull().all()]
        samples[mask] = self._Do[mask].values
        # Compute variables given noise given beta matrix
        I = np.identity(len(self._Beta))
        samples = np.linalg.solve((self._Beta + I).T, samples.T)
        samples = pd.DataFrame(samples.T, columns=self._Beta.columns)
        return samples
