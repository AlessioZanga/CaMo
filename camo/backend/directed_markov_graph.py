from itertools import combinations
from typing import Iterable, Set, Tuple

import networkx as nx

from .graph import Graph
from .directed_graph import DirectedGraph, topological_sort
from ..utils import _as_set


class DirectedMarkovGraph(DirectedGraph):

    def __init__(
        self,
        V: Iterable[str] = None,
        E: Iterable[Tuple[str, str]] = None
    ):
        super().__init__(V, E)

    @property
    def probability_distribution(self) -> str:
        P = [
            (v, self.parents(v))
            for v in topological_sort(self)
        ]
        P = [
            f"P({v}|{','.join(parents)})"
            if parents else f"P({v})"
            for (v, parents) in P
        ]
        return ''.join(P)

    @property
    def skeleton(self) -> Graph:
        return self.to_undirected()

    @property
    def v_structures(self) -> Set[Tuple[str]]:
        v_structures = set()
        for v in self.vertices:
            for (i, j) in combinations(self.parents(v), 2):
                if not self.has_edge(i, j) and not self.has_edge(j, i):
                    v_structures.add((i, v, j))
        return v_structures

    @property
    def equivalence_class(self):
        raise NotImplementedError()  # TODO

    def is_chain(self, X: str, Y: str, Z: str) -> bool:
        return self.has_edge(X, Y) and self.has_edge(Y, Z)

    def is_fork(self, X: str, Y: str, Z: str) -> bool:
        return self.has_edge(X, Y) and self.has_edge(X, Z)

    def is_collider(self, X: str, Y: str, Z: str) -> bool:
        return self.has_edge(X, Z) and self.has_edge(Y, Z)

    def is_d_separated(self, X: Iterable[str], Y: Iterable[str], Z: Iterable[str] = None) -> bool:
        X, Y, Z = _as_set(X), _as_set(Y), _as_set(Z)

        if X & Z or Y & Z:
            return True

        return nx.d_separated(self._G, X, Y, Z)
