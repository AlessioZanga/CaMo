from typing import Iterable, Optional, Set, Tuple

import matplotlib.pyplot as plt
import networkx as nx

from ..utils import _as_set


class Graph:

    _G: nx.Graph

    def __init__(
        self,
        V: Optional[Iterable[str]] = None,
        E: Optional[Iterable[Tuple[str, str]]] = None
    ):
        self._G = nx.Graph()
        if V:
            self._G.add_nodes_from(V)
        if E:
            self._G.add_edges_from(E)

    @property
    def V(self) -> Set[str]:
        return set(self._G.nodes)

    def has_vertex(self, v: str) -> bool:
        return self._G.has_node(v)

    def add_vertex(self, v: str) -> None:
        self._G.add_node(v)

    def del_vertex(self, v: str) -> None:
        self._G.remove_node(v)

    @property
    def E(self) -> Set[Tuple[str, str]]:
        return set(self._G.edges) | {tuple(reversed(e)) for e in self._G.edges}

    def has_edge(self, u: str, v: str) -> bool:
        return self._G.has_edge(u, v)

    def add_edge(self, u: str, v: str) -> None:
        self._G.add_edge(u, v)

    def del_edge(self, u: str, v: str) -> None:
        self._G.remove_edge(u, v)

    def neighbors(self, v: str) -> Set[str]:
        return {
            n
            for u in _as_set(v)
            for n in self._G.neighbors(u)
        }

    def subgraph(self, V: Set[str]):
        subgraph = self._G.subgraph(V)
        return type(self)(subgraph.nodes, subgraph.edges)

    def paths(self, u: str, v: str) -> Set[Tuple[str]]:
        return {tuple(p) for p in nx.all_simple_paths(self._G, u, v)}

    def has_path(self, u: str, v: str) -> bool:
        return nx.has_path(self._G, u, v)

    def plot(self, figsize: Tuple[float, float] = None) -> None:    # pragma: no cover
        sty = {"node_shape": ""}
        pos = nx.nx_agraph.pygraphviz_layout(self._G, prog="dot")
        figsize = figsize if figsize else (5, 5)
        plt.figure(figsize=figsize)
        nx.draw(self._G, pos, with_labels=True, **sty)
        plt.draw()
        plt.show()
        plt.close()

    @classmethod
    def from_complete(cls, V: Set[str]):
        G = cls()
        G._G = nx.complete_graph(V)
        return G

    def __repr__(self):
        return f"{self.__class__.__name__}(V={self.V}, E={self.E})"
