from typing import Any, Set

import numpy as np
import pandas as pd

from .abstract_estimator import AbstractEstimator
from ...utils import _as_set


class PropensityScore(AbstractEstimator):

    def __init__(self, model: str = "logit"):
        super().__init__(model)

    def fit(self, data: pd.DataFrame, X: str, Y: str, Z: Set[str]) -> Any:
        Z = _as_set(Z)
        f = f"{X} ~ " + " + ".join(Z) if Z else None
        self._estimator = self._model(f, data).fit(disp=0) if f else None
        return self

    def predict(self, data: pd.DataFrame, X: str, Y: str, Z: Set[str]) -> Any:
        if not self._estimator:
            return np.full(len(data), data[X].mean())
        return self._estimator.predict(data).to_numpy()
