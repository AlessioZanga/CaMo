from typing import Any, Set

import pandas as pd

from .abstract_estimator import AbstractEstimator
from ...utils import _as_set


class GFormula(AbstractEstimator):

    def fit(self, data: pd.DataFrame, X: str, Y: str, Z: Set[str]) -> Any:
        Z = _as_set(Z)
        f = f"{Y} ~ {X}"
        f = f if not Z else f + " + " + " + ".join(Z)
        self._estimator = self._estimator(f, data).fit()
        return self

    def predict(self, data: pd.DataFrame, X: str, Y: str, Z: Set[str]) -> Any:
        Z = list(_as_set(Z))

        # Helper function
        def _fill_copy(data, x):
            data = data[Z].copy()
            data[X] = x
            return data

        # Estimate E[Y|do(X=1),Z] and E[Y|do(X=0),Z]
        Y1 = self._estimator.predict(_fill_copy(data, 1))
        Y0 = self._estimator.predict(_fill_copy(data, 0))

        return Y1, Y0
