from abc import ABC, abstractmethod
from typing import Any, Iterable, Set, Tuple

import pandas as pd

from ..backend import DirectedMarkovGraph


class CausalModel(DirectedMarkovGraph, ABC):

    _V: Set[str]
    _U: Set[str]

    def __init__(
        self,
        V: Iterable[str] = None,
        U: Iterable[str] = None,
        E: Iterable[Tuple[str]] = None,
    ):
        self._V = set(V) if V else set()
        self._U = set(U) if U else set()

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
    def causal_graph(self) -> Any:
        raise NotImplementedError()  # TODO

    @property
    def endogenous_variables(self) -> Set[str]:
        return set(self._V)

    @property
    def exogenous_variables(self) -> Set[str]:
        return set(self._U)

    @abstractmethod
    def do(self, **kwargs):
        pass

    @abstractmethod
    def sample(self, size: int) -> pd.DataFrame:
        pass
