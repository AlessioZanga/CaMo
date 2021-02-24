from typing import Any, Dict, Optional

import numpy as np
import pandas as pd

from .linear_scm import LinearSCM


class LinearNonGaussianSCM(LinearSCM):

    @property
    def P(self) -> Dict[str, Any]:
        return {u: np.random.uniform for u in self._U}

    def sample(self, size: int, seed: Optional[int] = None) -> pd.DataFrame:
        # Set random seed
        np.random.seed(seed)
        # Generate noise from uniform distribution
        samples = np.array([
            np.random.uniform(size=size)
            for u in self._Gamma.index
        ])
        samples = pd.DataFrame(samples.T, columns=self._Gamma.index)
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
