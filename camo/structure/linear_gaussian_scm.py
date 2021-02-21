from functools import partial
from typing import Any, Dict, Iterable, List, Set, Tuple

import numpy as np
import pandas as pd

from .causal_model import CausalModel
from ..utils import _as_set


class LinearGaussianSCM(CausalModel):

    _Beta: pd.DataFrame
    _Gamma: pd.DataFrame
    _Sigma: pd.Series

    _Do: pd.Series

    def __init__(
        self,
        V: Iterable[str] = None,
        Beta: np.array = None,
        Gamma: np.array = None,
        Sigma: np.array = None
    ):
        # Build weighted adjacency matrix between endogenous variables
        self._Beta = pd.DataFrame(Beta, index=V, columns=V, copy=True)

        # Build weighted adjacency matrix between endogenous-exogenous variables
        self._Gamma = np.identity(len(self._Beta)) if Gamma is None else Gamma
        self._Gamma = pd.DataFrame(self._Gamma, columns=self._Beta.columns, copy=True)
        self._Gamma.index = [
            "$U_{" + ''.join(self._Gamma.columns[self._Gamma.loc[i] != 0]) + "}$"
            for i in self._Gamma.index
        ]

        # Build vector of noise variances
        self._Sigma = np.ones((1, len(self._Gamma))) if Sigma is None else Sigma
        self._Sigma = pd.DataFrame(self._Sigma, columns=self._Gamma.index, copy=True)

        # Initialize vector of interventions
        self._Do = pd.DataFrame([[np.nan] * len(self._Beta)], columns=self._Beta.columns)

        # Get edges from adjacency matrix
        E = self._Beta[self._Beta != 0].stack().index.tolist()
        E += self._Gamma[self._Gamma != 0].stack().index.tolist()
        
        # TODO: Generalize to cyclic models
        np.fill_diagonal(self._Beta.values, 1)

        super().__init__(self._Beta.index, self._Gamma.index, E)

    def copy(self):
        return LinearGaussianSCM(
            self._Beta.index, self._Beta, self._Gamma, self._Sigma
        )

    @property
    def F(self) -> Dict[str, Any]:
        return self._Beta.T.to_dict("series")

    @property
    def P(self) -> Dict[str, Any]:
        return self._Sigma.apply(
            lambda x: partial(np.random.normal, scale=np.sqrt(x))
        ).to_dict()

    @property
    def Beta(self) -> pd.DataFrame:
        return self._Beta.copy()

    @property
    def Gamma(self) -> pd.DataFrame:
        return self._Gamma.copy()

    @property
    def Sigma(self) -> pd.DataFrame:
        return self._Sigma.copy()

    def do(self, **kwargs):
        # Check if v is endogenous
        if not (kwargs.keys() & self._V):
            raise ValueError()
        # Copy model
        out = self.copy()
        # Set intervened variables
        for (v, k) in kwargs.items():
            # Fix v variable to constant k
            out._Beta[v], out._Gamma[v], out._Do[v] = 0, 0, k
            # Remove incoming edges
            for u in out.parents(v):
                out.del_edge(u, v)
        # Restore self reference
        # TODO: Generalize to cyclic models
        np.fill_diagonal(out._Beta.values, 1)
        return out

    def sample(self, size: int, seed: int = None) -> pd.DataFrame:
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
        samples = samples @ self._Beta
        return samples

    @classmethod
    def from_structure(
        cls,
        V: Iterable[str],
        E: Iterable[Tuple[str, str]]
    ):
        V, U = list(V), set()

        # Check if both vertices are in a vertex set
        # else, add to exogenous variables
        for (u, v) in E:
            if u not in V:
                U.add(u)
            if v not in V:
                U.add(v)

        U = list(U)

        Beta = np.zeros((len(V), len(V)))
        Beta = pd.DataFrame(Beta, index=V, columns=V)
        for (u, v) in E:
            if u in V and v in V:
                Beta.loc[u, v] = 1

        Gamma = None
        if U:
            Gamma = np.zeros((len(U), len(V)))
            Gamma = pd.DataFrame(Gamma, index=U, columns=V)
            for (u, v) in E:
                if u in U and v in V:
                    Gamma.loc[u, v] = 1

        return cls(V, Beta, Gamma)
