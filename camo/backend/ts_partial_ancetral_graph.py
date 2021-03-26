from collections import defaultdict
from itertools import permutations
from tempfile import NamedTemporaryFile
from typing import Set, Tuple

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from .partial_ancestral_graph import PartialAncestralGraph, Endpoints


class tsPartialAncestralGraph(PartialAncestralGraph):

    def _homologous_edges(self, X: str, Y: str) -> Set[Tuple[str, str]]:
        out = set()
        x, xt = X.split(":")
        y, yt = Y.split(":")
        i, t = 0, int(xt) - int(yt)
        homologous = lambda i: (x + f":{i}", y + f":{i + t}")
        Xi, Yi = homologous(i)
        while self.has_vertex(Xi):
            if self.has_vertex(Yi) and self.has_edge(Xi, Yi):
                out.add((Xi, Yi))
            i += 1
            Xi, Yi = homologous(i)
        return out - {(X, Y)}

    def add_edge(self, X: str, Y: str, endpoint: int = Endpoints.TAIL) -> None:
        self._G.add_edge(X, Y)
        # Add homologous edges
        for e in self._homologous_edges(X, Y):
            self._G.add_edge(*e)
        self.set_endpoint(X, Y, endpoint)
        self.set_endpoint(Y, X, endpoint)

    def del_edge(self, X: str, Y: str) -> None:
        self._G.remove_edge(X, Y)
        # Del homologous edges
        for e in self._homologous_edges(X, Y):
            self._G.remove_edge(*e)
        self.unset_endpoint(X, Y)
        self.unset_endpoint(Y, X)

    def set_endpoint(self, X: str, Y: str, endpoint: int) -> None:
        self._endpoints[(X, Y)] = endpoint
        # Set homologous endpoints
        for e in self._homologous_edges(X, Y):
            self._endpoints[e] = endpoint

    def unset_endpoint(self, X: str, Y: str) -> None:
        del self._endpoints[(X, Y)]
        # Unset homologous endpoints
        for e in self._homologous_edges(X, Y):
            del self._endpoints[e]
