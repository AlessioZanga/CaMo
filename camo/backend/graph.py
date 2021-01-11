import matplotlib.pyplot as plt
import networkx as nx

from typing import Iterable, List, Set, Tuple


class Graph:

    _G: nx.Graph

    def __init__(
        self,
        V: Iterable[str] = None,
        E: Iterable[Tuple[str, str]] = None
    ):
        self._G = nx.Graph()
        if V:
            self._G.add_nodes_from(V)
        if E:
            self._G.add_edges_from(E)

    @property
    def vertices(self) -> Set[str]:
        return set(self._G.nodes)

    def has_vertex(self, v: str) -> bool:
        return self._G.has_node(v)

    def add_vertex(self, v: str) -> None:
        self._G.add_node(v)

    def del_vertex(self, v: str) -> None:
        self._G.remove_node(v)

    @property
    def edges(self) -> Set[Tuple[str, str]]:
        return set(self._G.edges)

    def has_edge(self, u: str, v: str) -> bool:
        return self._G.has_edge(u, v)

    def add_edge(self, u: str, v: str) -> None:
        self._G.add_edge(u, v)

    def del_edge(self, u: str, v: str) -> None:
        self._G.remove_edge(u, v)

    def neighbors(self, v: str) -> Set[str]:
        return set(self._G.neighbors(v))

    def subgraph(self, V: Set[str]):
        subgraph = self._G.subgraph(V)
        return type(self)(subgraph.nodes, subgraph.edges)

    def has_path(self, u: str, v: str) -> bool:
        return nx.has_path(self._G, u, v)

    def paths(self, u: str, v: str) -> List[Tuple[str]]:
        return [tuple(p) for p in nx.all_simple_paths(self._G, u, v)]

    def plot(self) -> None:
        sty = {"node_shape": ""}
        pos = nx.nx_agraph.pygraphviz_layout(self._G, prog="dot")
        nx.draw(self._G, pos, with_labels=True, **sty)
        plt.show()

    def __repr__(self):
        return f"{self.__class__.__name__}(V={self.vertices}, E={self.edges})"
