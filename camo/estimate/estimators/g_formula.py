from typing import Any, Set

import pandas as pd

from .abstract_estimator import AbstractEstimator
from ...utils import _as_set


class GFormula(AbstractEstimator):

    def fit(self, data: pd.DataFrame, X: str, Y: str, Z: Set[str]) -> Any:
        Z = _as_set(Z)
        f = f"{Y} ~ {X}"
        f = f if not Z else f + " + " + " + ".join(Z)
        self._estimator = self._model(f, data).fit(disp=0)
        return self

    def predict(self, data: pd.DataFrame, X: str, Y: str, Z: Set[str]) -> Any:
        # Estimate E[Y|do(X=1),Z] and E[Y|do(X=0),Z]
        Y1 = self._estimator.predict(data.assign(**{X: 1}))
        Y0 = self._estimator.predict(data.assign(**{X: 0}))

        return Y1, Y0
