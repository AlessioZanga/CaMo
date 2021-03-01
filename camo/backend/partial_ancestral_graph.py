from collections import defaultdict
from enum import IntEnum
from tempfile import NamedTemporaryFile
from typing import Dict, Iterable, Optional, Set, Tuple

import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from .graph import Graph


class Endpoints(IntEnum):
    ANY = 42        # *
    TAIL = 45       # -
    HEAD = 62       # >
    CIRCLE = 111    # o


class PartialAncestralGraph(Graph):

    _endpoints: Dict[Tuple[str, str], int]
    _non_collider: Dict[Tuple[str, str], Set[str]]

    def __init__(
        self,
        V: Optional[Iterable[str]] = None,
        E: Optional[Iterable[Tuple[str, str]]] = None,
        endpoint: int = Endpoints.TAIL
    ):
        super().__init__(V, E)
        # Initialize dict
        self._endpoints = {}
        self._non_collider = defaultdict(set)
        # Set default endpoints
        for (u, v) in E:
            self.set_endpoint(u, v, endpoint)
            self.set_endpoint(v, u, endpoint)

    def add_edge(self, u: str, v: str, endpoint: int = Endpoints.TAIL) -> None:
        self._G.add_edge(u, v)
        self.set_endpoint(u, v, endpoint)
        self.set_endpoint(v, u, endpoint)

    def del_edge(self, u: str, v: str) -> None:
        self._G.remove_edge(u, v)
        self.unset_endpoint(u, v)
        self.unset_endpoint(v, u)

    def has_endpoint(self, u: str, v: str, endpoint: int) -> bool:
        return self._endpoints.get((u, v), None) == endpoint

    def set_endpoint(self, u: str, v: str, endpoint: int) -> None:
        self._endpoints[(u, v)] = endpoint

    def unset_endpoint(self, u: str, v: str) -> None:
        del self._endpoints[(u, v)]

    def is_any_circle(self, u: str, v: str) -> bool:
        return self.has_endpoint(u, v, Endpoints.CIRCLE)

    def is_any_head(self, u: str, v: str) -> bool:
        return self.has_endpoint(u, v, Endpoints.HEAD)

    def is_any_tail(self, u: str, v: str) -> bool:
        return self.has_endpoint(u, v, Endpoints.TAIL)

    def is_tail_head(self, u: str, v: str) -> bool:
        return \
            self.has_endpoint(v, u, Endpoints.TAIL) and \
            self.has_endpoint(u, v, Endpoints.HEAD)

    def is_tail_tail(self, u: str, v: str) -> bool:
        return \
            self.has_endpoint(v, u, Endpoints.TAIL) and \
            self.has_endpoint(u, v, Endpoints.TAIL)

    def is_directed_path(self, p: Tuple[str]) -> bool:
        return all(self.is_any_head(u, v) for (u, v) in zip(p, p[1:]))

    def is_collider(self, u: str, v: str, w: str) -> bool:
        return self.is_any_head(u, v) and self.is_any_head(w, v)

    def is_non_collider(self, u: str, v: str, w: str) -> bool:
        return \
            self.is_any_tail(u, v) or \
            self.is_any_tail(w, v) or \
            v in self._non_collider[(u, w)] or \
            v in self._non_collider[(w, u)]

    def set_non_collider(self, u: str, v: str, w: str) -> None:
        self._non_collider[(u, w)].add(v)
        self._non_collider[(w, u)].add(v)

    def unset_non_collider(self, u: str, v: str, w: str) -> None:
        self._non_collider[(u, w)].remove(v)
        self._non_collider[(w, u)].remove(v)

    def is_discriminating_path(self, p: Tuple[str], v: str):
        u, w = p[0], p[-1]
        if p[-2] == v and \
        not self.has_edge(u, w) and \
        all(    # (iii), (iv) and (o)
            self.is_collider(x, y, z) or \
            self.is_non_collider(x, y, z)
            for (x, y, z) in zip(p, p[1:], p[2:])
            if y != v
        ) and \
        all(    # (i)
            self.is_any_head(x, y)
            for (x, y) in zip(p, p[1:])
            if x != v
        ) and \
        all(    # (ii)
            (self.is_collider(x, y, z) and \
            self.is_tail_head(y, w)) or \
            self.is_any_head(w, y)
            for (x, y, z) in zip(p, p[1:], p[2:])
            if y != v
        ):
            return True
        return False

    def to_adjacency_matrix(self) -> pd.DataFrame:
        V = sorted(self.V)
        out = pd.DataFrame(0, columns=V, index=V)
        mapping = {
            Endpoints.CIRCLE: 1,
            Endpoints.HEAD: 2,
            Endpoints.TAIL: 3
        }
        for (u, v), k in self._endpoints.items():
            out.at[u, v] = mapping[k]
        return out

    def plot(self, figsize: Tuple[float, float] = None) -> None:
        import pygraphviz
        styles = {
            Endpoints.ANY: "odiamond",
            Endpoints.TAIL: "none",
            Endpoints.HEAD: "normal",
            Endpoints.CIRCLE: "odot",
        }
        path = NamedTemporaryFile(suffix=".png").name
        G = pygraphviz.AGraph(directed=True)
        figsize = figsize if figsize else (7, 7)
        G.graph_attr["fixedsize"] = True
        G.graph_attr["size"] = f"{figsize[0]},{figsize[1]}!"
        for v in self._G.nodes:
            G.add_node(v, shape="none")
        for (u, v) in self._G.edges:
            s = styles[self._endpoints[(u, v)]]
            t = styles[self._endpoints[(v, u)]]
            G.add_edge(u, v, arrowhead=s, arrowtail=t, dir="both")
        G.layout(prog="dot")
        G.draw(path)
        plt.figure(figsize=figsize)
        _ = plt.imshow(mpimg.imread(path))
        plt.axis("off")
        plt.show()
