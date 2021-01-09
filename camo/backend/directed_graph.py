import networkx as nx

from typing import Iterable, Set, Tuple

from .graph import Graph


class DirectedGraph(Graph):

    def __init__(
        self,
        V: Iterable[str] = None,
        E: Iterable[Tuple[str, str]] = None
    ):
        super().__init__()
        self._G = nx.DiGraph()
        if V:
            self._G.add_nodes_from(V)
        if E:
            self._G.add_edges_from(E)

    def ancestors(self, v: str) -> Set[str]:
        return set(nx.ancestors(self._G, v))

    def parents(self, v: str) -> Set[str]:
        return set(self._G.predecessors(v))

    def children(self, v: str) -> Set[str]:
        return set(self._G.successors(v))

    def descendants(self, v: str) -> Set[str]:
        return set(nx.descendants(self._G, v))

    def to_undirected(self) -> Graph:
        G = Graph()
        G._G = self._G.to_undirected()
        return G


def moral(G: DirectedGraph) -> Graph:
    out = Graph()
    out._G = nx.moral.moral_graph(G._G)
    return out


def topological_sort(G: DirectedGraph) -> Iterable[str]:
    return nx.topological_sort(G._G)
