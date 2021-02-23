from typing import Iterable, Optional, Set, Tuple

import networkx as nx

from .graph import Graph
from ..utils import _as_set


class DirectedGraph(Graph):

    def __init__(
        self,
        V: Optional[Iterable[str]] = None,
        E: Optional[Iterable[Tuple[str, str]]] = None
    ):
        super().__init__()
        self._G = nx.DiGraph()
        if V:
            self._G.add_nodes_from(V)
        if E:
            self._G.add_edges_from(E)

    def ancestors(self, v: str) -> Set[str]:
        return {
            a
            for u in _as_set(v)
            for a in nx.ancestors(self._G, u)
        }

    def parents(self, v: str) -> Set[str]:
        return {
            p
            for u in _as_set(v)
            for p in self._G.predecessors(u)
        }

    def children(self, v: str) -> Set[str]:
        return {
            c
            for u in _as_set(v)
            for c in self._G.successors(u)
        }

    def descendants(self, v: str) -> Set[str]:
        return {
            d
            for u in _as_set(v)
            for d in nx.descendants(self._G, u)
        }

    def is_acyclic(self) -> bool:
        return nx.is_directed_acyclic_graph(self._G)

    def to_undirected(self) -> Graph:
        G = Graph()
        G._G = self._G.to_undirected()
        return G

    @classmethod
    def from_undirected(cls, other: Graph):
        G = cls()
        G._G = other._G.to_directed()
        return G


def moral(G: DirectedGraph) -> Graph:
    out = Graph()
    out._G = nx.moral.moral_graph(G._G)
    return out


def topological_sort(G: DirectedGraph) -> Iterable[str]:
    return nx.topological_sort(G._G)
