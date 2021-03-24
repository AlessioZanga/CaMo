from enum import IntEnum
from tempfile import NamedTemporaryFile
from typing import Dict, Iterable, Optional, Tuple

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

    def __init__(
        self,
        V: Optional[Iterable[str]] = None,
        E: Optional[Iterable[Tuple[str, str]]] = None,
        endpoint: int = Endpoints.TAIL
    ):
        super().__init__(V, E)
        self._endpoints = {}
        for (X, Y) in E:
            self.set_endpoint(X, Y, endpoint)
            self.set_endpoint(Y, X, endpoint)

    def add_edge(self, X: str, Y: str, endpoint: int = Endpoints.TAIL) -> None:
        self._G.add_edge(X, Y)
        self.set_endpoint(X, Y, endpoint)
        self.set_endpoint(Y, X, endpoint)

    def del_edge(self, X: str, Y: str) -> None:
        self._G.remove_edge(X, Y)
        self.unset_endpoint(X, Y)
        self.unset_endpoint(Y, X)

    def has_endpoint(self, X: str, Y: str, endpoint: int) -> bool:
        return self._endpoints[(X, Y)] == endpoint

    def set_endpoint(self, X: str, Y: str, endpoint: int) -> None:
        self._endpoints[(X, Y)] = endpoint

    def unset_endpoint(self, X: str, Y: str) -> None:
        del self._endpoints[(X, Y)]

    def is_any_circle(self, X: str, Y: str) -> bool:
        return self.has_endpoint(X, Y, Endpoints.CIRCLE)

    def is_any_head(self, X: str, Y: str) -> bool:
        return self.has_endpoint(X, Y, Endpoints.HEAD)

    def is_any_tail(self, X: str, Y: str) -> bool:
        return self.has_endpoint(X, Y, Endpoints.TAIL)

    def is_circle_circle(self, X: str, Y: str) -> bool:
        return \
            self.has_endpoint(Y, X, Endpoints.CIRCLE) and \
            self.has_endpoint(X, Y, Endpoints.CIRCLE)

    def is_circle_head(self, X: str, Y: str) -> bool:
        return \
            self.has_endpoint(Y, X, Endpoints.CIRCLE) and \
            self.has_endpoint(X, Y, Endpoints.HEAD)

    def is_tail_circle(self, X: str, Y: str) -> bool:
        return \
            self.has_endpoint(Y, X, Endpoints.TAIL) and \
            self.has_endpoint(X, Y, Endpoints.CIRCLE)

    def is_tail_head(self, X: str, Y: str) -> bool:
        return \
            self.has_endpoint(Y, X, Endpoints.TAIL) and \
            self.has_endpoint(X, Y, Endpoints.HEAD)

    def is_tail_tail(self, X: str, Y: str) -> bool:
        return \
            self.has_endpoint(Y, X, Endpoints.TAIL) and \
            self.has_endpoint(X, Y, Endpoints.TAIL)

    def is_uncovered_path(self, p: Tuple[str]) -> bool:
        return all(
            not self.has_edge(X, Z)
            for (X, Y, Z) in zip(p, p[1:], p[2:])
        )

    def is_directed_path(self, p: Tuple[str]) -> bool:
        return all(self.is_any_head(X, Y) for (X, Y) in zip(p, p[1:]))

    def is_potentially_directed_path(self, p: Tuple[str]) -> bool:
        return all(
            not (self.is_any_head(Y, X) or self.is_any_tail(X, Y))
            for (X, Y) in zip(p, p[1:])
        )

    def is_collider(self, X: str, Y: str, Z: str) -> bool:
        return self.is_any_head(X, Y) and self.is_any_head(Z, Y)

    def is_discriminating_path(self, p: Tuple[str], Y: str):
        if len(p) < 4:  # (i)
            return False
        if Y != p[-2]:  # (ii)
            return False
        X, Z = p[0], p[-1]
        if self.has_edge(X, Z): # (iii.a)
            return False
        if any(
            not (self.is_collider(P, Q, R) and \
            self.has_edge(Q, Z) and \
            self.is_tail_head(Q, Z))
            for (P, Q, R) in zip(p[:-1], p[1:-1], p[2:-1])
        ):  # (iii.b)
            return False
        return True

    def to_adjacency_matrix(self) -> pd.DataFrame:
        V = sorted(self.V)
        out = pd.DataFrame(0, columns=V, index=V)
        mapping = {
            Endpoints.CIRCLE: 1,
            Endpoints.HEAD: 2,
            Endpoints.TAIL: 3
        }
        for (X, Y), k in self._endpoints.items():
            out.at[X, Y] = mapping[k]
        return out

    def plot(self, figsize: Tuple[float, float] = None) -> None:    # pragma: no cover
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
        for Y in self._G.nodes:
            G.add_node(Y, shape="none")
        for (X, Y) in self._G.edges:
            s = styles[self._endpoints[(X, Y)]]
            t = styles[self._endpoints[(Y, X)]]
            G.add_edge(X, Y, arrowhead=s, arrowtail=t, dir="both")
        G.layout(prog="dot")
        G.draw(path)
        plt.figure(figsize=figsize)
        _ = plt.imshow(mpimg.imread(path))
        plt.axis("off")
        plt.show()
