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

    def add_vertex(self, v: str) -> None:
        raise NotImplementedError()  # FIXME:

    def del_vertex(self, v: str) -> None:
        raise NotImplementedError()  # FIXME:

    def add_edge(self, u: str, v: str) -> None:
        raise NotImplementedError()  # FIXME:

    def del_edge(self, u: str, v: str) -> None:
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
