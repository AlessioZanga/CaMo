from abc import ABC, abstractmethod
from inspect import getmembers, ismethod
from typing import Any, Set

import pandas as pd
import statsmodels.formula.api as smf

from ...utils import _try_get

STATSMODELS = dict(getmembers(smf, ismethod))


class AbstractEstimator(ABC):

    _estimator: Any

    def __init__(self, estimator: str = "ols", ESTIMATORS: Any = None):
        self._estimator = _try_get(estimator, ESTIMATORS or STATSMODELS)

    @abstractmethod
    def fit(self, data: pd.DataFrame, X: str, Y: str, Z: Set[str]) -> Any:
        pass

    def fit_predict(self, data: pd.DataFrame, X: str, Y: str, Z: Set[str]) -> Any:
        return self.fit(data, X, Y, Z).predict(data, X, Y, Z)

    @abstractmethod
    def predict(self, data: pd.DataFrame, X: str, Y: str, Z: Set[str]) -> Any:
        pass
