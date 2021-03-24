from typing import Any, Dict, Iterable, Optional, Tuple

import numpy as np
import pandas as pd

from .causal_model import CausalModel


class LinearSCM(CausalModel):

    _Beta: pd.DataFrame
    _Gamma: pd.DataFrame

    _Do: pd.Series

    def __init__(
        self,
        V: Optional[Iterable[str]] = None,
        Beta: Optional[np.array] = None,
        Gamma: Optional[np.array] = None
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

        # Initialize vector of interventions
        self._Do = pd.DataFrame([[np.nan] * len(self._Beta)], columns=self._Beta.columns)

        # Get edges from adjacency matrix
        E = self._Beta[self._Beta != 0].stack().index.tolist()
        E += self._Gamma[self._Gamma != 0].stack().index.tolist()

        super().__init__(self._Beta.index, self._Gamma.index, E)

    def add_vertex(self, X: str) -> None:
        raise NotImplementedError()  # FIXME:

    def del_vertex(self, X: str) -> None:
        raise NotImplementedError()  # FIXME:

    def add_edge(self, X: str, Y: str) -> None:
        raise NotImplementedError()  # FIXME:

    def del_edge(self, X: str, Y: str) -> None:
        raise NotImplementedError()  # FIXME:

    def copy(self):
        return type(self)(self._Beta.index, self._Beta, self._Gamma)

    @property
    def F(self) -> Dict[str, Any]:
        return self._Beta.T.to_dict("series")

    @property
    def Beta(self) -> pd.DataFrame:
        return self._Beta.copy()

    @property
    def Gamma(self) -> pd.DataFrame:
        return self._Gamma.copy()

    def do(self, **kwargs):
        # Check if X is endogenous
        if not (kwargs.keys() & self._V):
            raise ValueError()
        # Copy model
        out = self.copy()
        # Set intervened variables
        for (Y, k) in kwargs.items():
            # Fix X variable to constant k
            out._Beta[Y], out._Gamma[Y], out._Do[Y] = 0, 0, k
            # Remove incoming edges
            for X in out.parents(Y):
                out.del_edge(X, Y)
        return out

    @classmethod
    def from_structure(
        cls,
        V: Iterable[str],
        E: Iterable[Tuple[str, str]]
    ):
        V, U = list(V), set()

        # Check if both vertices are in a vertex set
        # else, add to exogenous variables
        for (X, Y) in E:
            if X not in V:
                U.add(X)
            if Y not in V:
                U.add(Y)

        U = list(U)

        Beta = np.zeros((len(V), len(V)))
        Beta = pd.DataFrame(Beta, index=V, columns=V)
        for (X, Y) in E:
            if X in V and Y in V:
                Beta.loc[X, Y] = 1

        Gamma = None
        if U:
            Gamma = np.zeros((len(U), len(V)))
            Gamma = pd.DataFrame(Gamma, index=U, columns=V)
            for (X, Y) in E:
                if X in U and Y in V:
                    Gamma.loc[X, Y] = 1

        return cls(V, Beta, Gamma)
