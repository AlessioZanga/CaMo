from typing import Any, Set

import numpy as np
import pandas as pd

from .abstract_estimator import AbstractEstimator
from ...utils import _as_set


class PropensityScore(AbstractEstimator):

    def __init__(self, estimator: str = "logit"):
        super().__init__(estimator)

    def fit(self, data: pd.DataFrame, X: str, Y: str, Z: Set[str]) -> Any:
        Z = _as_set(Z)
        f = f"{X} ~ " + " + ".join(Z) if Z else None
        self._estimator = self._estimator(f, data).fit() if f else None
        return self

    def predict(self, data: pd.DataFrame, X: str, Y: str, Z: Set[str]) -> Any:
        if not self._estimator:
            return np.fill((len(data), ), np.mean(data[X]))
        return self._estimator.predict(data)
