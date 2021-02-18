from abc import ABC, abstractmethod, abstractproperty
from typing import Any, Dict, Iterable, Set, Tuple

import pandas as pd

from ..backend import DirectedMarkovGraph
from ..utils import _as_set


class CausalModel(DirectedMarkovGraph, ABC):

    _V: Set[str]
    _U: Set[str]

    def __init__(
        self,
        V: Iterable[str] = None,
        U: Iterable[str] = None,
        E: Iterable[Tuple[str]] = None,
    ):
        self._V, self._U, E = _as_set(V), _as_set(U), _as_set(E)

        # Check if V and U are disjoint
        if self._V & self._U:
            raise ValueError()

        # Check if both vertices are in a vertex set
        # else, add to exogenous variables
        for (u, v) in E:
            if u not in self._V:
                self._U.add(u)
            if v not in self._V:
                self._U.add(v)

        super().__init__(self._V | self._U, E)

    @property
    def V(self) -> Set[str]:
        return set(self._V)

    @property
    def U(self) -> Set[str]:
        return set(self._U)

    @abstractproperty
    def F(self) -> Dict[str, Any]:
        pass

    @abstractproperty
    def P(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def copy(self):
        pass

    @abstractmethod
    def do(self, **kwargs):
        pass

    @abstractmethod
    def fit(self, data: pd.DataFrame):
        pass

    @abstractmethod
    def sample(self, size: int) -> pd.DataFrame:
        pass
