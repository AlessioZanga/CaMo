import networkx as nx

from itertools import combinations
from typing import Iterable, Set, Tuple

from .directed_graph import DirectedGraph


class DirectedMarkovGraph(DirectedGraph):

    def __init__(
        self,
        V: Iterable[str] = None,
        E: Iterable[Tuple[str, str]] = None
    ):
        super().__init__(V, E)

    @property
    def v_structures(self) -> Set[Tuple[str]]:
        v_structures = set()
        for v in self.vertices:
            for (i, j) in combinations(self.parents(v), 2):
                if not self.has_edge(i, j) and not self.has_edge(j, i):
                    v_structures.add((i, v, j))
        return v_structures

    def is_chain(self, X: str, Y: str, Z: str) -> bool:
        return self.has_edge(X, Y) and self.has_edge(Y, Z)

    def is_fork(self, X: str, Y: str, Z: str) -> bool:
        return self.has_edge(X, Y) and self.has_edge(X, Z)

    def is_collider(self, X: str, Y: str, Z: str) -> bool:
        return self.has_edge(X, Z) and self.has_edge(Y, Z)

    def is_d_separated(self, X: Iterable[str], Y: Iterable[str], Z: Iterable[str] = None) -> bool:
        X = set([X]) if isinstance(X, str) else set(X)
        Y = set([Y]) if isinstance(Y, str) else set(Y)
        Z = set([Z]) if isinstance(Z, str) else Z
        Z = set() if Z is None else set(Z)

        return nx.d_separated(self._G, X, Y, Z)
