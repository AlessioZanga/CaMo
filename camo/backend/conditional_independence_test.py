from abc import ABC, abstractmethod
from typing import Optional, Set

import numpy as np
import pandas as pd
from scipy.stats import chi2, chi2_contingency, norm, t

from .partial_correlation import partial_correlation, fast_partial_correlation
from ..utils import _as_set

EPS = np.finfo(float).eps


class ConditionalIndependenceTest(ABC):

    _n: int
    _data: pd.DataFrame

    def fit(self, data: pd.DataFrame):
        self._data = data.copy()
        self._n = len(data)
        return self

    def fit_predict(self, data: pd.DataFrame, X: str, Y: str, Z: Set[str]):
        return self.fit(data).predict(X, Y, Z)

    @abstractmethod
    def predict(self, X: str, Y: str, Z: Set[str]):
        pass


class ChiSquared(ConditionalIndependenceTest):

    def predict(self, X: str, Y: str, Z: Set[str]):
        Z = list(_as_set(Z))
        # Group data by Z
        data = [self._data] if not Z else (d for _, d in self._data.groupby(Z))
        # For each group compute the absolute frequency
        data = (d.groupby([X, Y]).size().unstack(Y, 0) for d in data)
        # Apply the selected contional indepependece test
        data = (chi2_contingency(d + EPS, lambda_="pearson") for d in data)
        # Reduce results among groups by using column-wise sum,
        # discarding unnecessary results
        data = np.vstack([d[:3] for d in data]).sum(axis=0)
        # Recompute p_value using chi and dof values
        data[1] = 1 - chi2.cdf(data[0], df=data[2])
        return data


class FisherZ(ConditionalIndependenceTest):

    def predict(self, X: str, Y: str, Z: Set[str]):
        Z = _as_set(Z)

        stat = partial_correlation(self._data, X, Y, Z)

        df = np.max(self._n - len(Z) - 3, 0)
        stat = np.sqrt(df) * np.abs(np.arctanh(stat + EPS))
        p_value = 2 * (1 - norm.cdf(stat))

        return stat, p_value, df


class StudentT(ConditionalIndependenceTest):

    def predict(self, X: str, Y: str, Z: Set[str]):
        Z = _as_set(Z)

        stat = partial_correlation(self._data, X, Y, Z)

        df = np.max(self._n - len(Z) - 2, 0)
        tran = np.sqrt(df) * np.abs(stat / (np.sqrt(1 - np.square(stat)) + EPS))
        p_value = 2 * (1 - t.cdf(tran, df))

        return stat, p_value, df


class FastFisherZ(ConditionalIndependenceTest):

    def fit(self, data: pd.DataFrame):
        self._data = data.cov()
        self._n = len(data)
        return self

    def predict(self, X: str, Y: str, Z: Set[str]):
        Z = _as_set(Z)

        stat = fast_partial_correlation(self._data, X, Y, Z)

        df = np.max(self._n - len(Z) - 3, 0)
        stat = np.sqrt(df) * np.abs(np.arctanh(stat + EPS))
        p_value = 2 * (1 - norm.cdf(stat))

        return stat, p_value, df


class FastStudentT(ConditionalIndependenceTest):

    def fit(self, data: pd.DataFrame):
        self._data = data.cov()
        self._n = len(data)
        return self

    def predict(self, X: str, Y: str, Z: Set[str]):
        Z = _as_set(Z)

        stat = fast_partial_correlation(self._data, X, Y, Z)

        df = np.max(self._n - len(Z) - 2, 0)
        tran = np.sqrt(df) * np.abs(stat / (np.sqrt(1 - np.square(stat)) + EPS))
        p_value = 2 * (1 - t.cdf(tran, df))

        return stat, p_value, df
