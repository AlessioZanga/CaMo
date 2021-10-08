from itertools import combinations, permutations
from typing import Optional, Iterable, Tuple

from .pc import PC
from ..backend import PAG, tsPAG, Endpoints


class CI(PC):

    def _R0(self, G: PAG) -> bool:
        is_closed = True
        for Y in G.V:
            for (X, Z) in combinations(G.neighbors(Y) - {Y}, 2):
                if (not G.has_edge(X, Z) and
                    Y not in self._dsep[(X, Z)]):
                    G.set_endpoint(X, Y, Endpoints.HEAD)
                    G.set_endpoint(Z, Y, Endpoints.HEAD)
                    is_closed = False
        return is_closed

    def _R1(self, G: PAG) -> bool:
        is_closed = True
        for Y in G.V:
            for (X, Z) in permutations(G.neighbors(Y) - {Y}, 2):
                if (G.is_any_head(X, Y) and
                    G.is_any_circle(Z, Y) and
                    not G.has_edge(X, Z)):
                    G.set_endpoint(Z, Y, Endpoints.TAIL)
                    G.set_endpoint(Y, Z, Endpoints.HEAD)
                    is_closed = False
        return is_closed

    def _R2(self, G: PAG) -> bool:
        is_closed = True
        for Y in G.V:
            for X in G.neighbors(Y) - {Y}:
                for Z in (G.neighbors(X) & G.neighbors(Y)) - {X, Y}:
                    if (G.is_any_circle(X, Z) and
                        G.is_any_head(X, Y) and
                        G.is_any_head(Y, Z) and
                        (G.is_any_tail(Y, X) or G.is_any_tail(Z, Y))):
                        G.set_endpoint(X, Z, Endpoints.HEAD)
                        is_closed = False
        return is_closed

    def _R3(self, G: PAG) -> bool:
        is_closed = True
        for Y in G.V:
            for (X, Z) in permutations(G.neighbors(Y) - {Y}, 2):
                if (G.is_any_head(X, Y) and
                    G.is_any_head(Z, Y) and
                    not G.has_edge(X, Z)):
                    for W in (G.neighbors(X) & G.neighbors(Y) & G.neighbors(Z)) - {X, Y, Z}:
                        if (G.is_any_circle(X, W) and
                            G.is_any_circle(Z, W) and
                            G.is_any_circle(W, Y)):
                            G.set_endpoint(W, Y, Endpoints.HEAD)
                            is_closed = False
        return is_closed

    def _R4(self, G: PAG) -> bool:
        is_closed = True
        for Y in G.V:
            for Z in G.neighbors(Y) - {Y}:
                if G.is_any_circle(Z, Y):
                    for W in G.V - {Y, Z}:
                        for p in G.paths(W, Z):
                            if G.is_discriminating_path(p, Y):
                                if Y in self._dsep[(W, Z)]:
                                    G.set_endpoint(Z, Y, Endpoints.TAIL)
                                    G.set_endpoint(Y, Z, Endpoints.HEAD)
                                else:
                                    X = p[-3]
                                    G.set_endpoint(X, Y, Endpoints.HEAD)
                                    G.set_endpoint(Y, Z, Endpoints.HEAD)
                                    G.set_endpoint(Z, Y, Endpoints.HEAD)
                                    G.set_endpoint(Y, Z, Endpoints.HEAD)
                                is_closed = False
                                break
        return is_closed

    def transform(
        self,
        G: PAG,
        blacklist: Optional[Iterable[Tuple[str, str]]] = None,
        whitelist: Optional[Iterable[Tuple[str, str]]] = None
    ) -> PAG:
        G = type(G)(G.V, G.E, Endpoints.CIRCLE, Endpoints.CIRCLE)

        self._KB(G, blacklist, whitelist, Endpoints.CIRCLE)

        self._R0(G)

        # If G is a timeseries graph
        if isinstance(G, tsPAG):
            for (X, Y) in G.E:
                if X.endswith(":0") and not Y.endswith(":0"):
                    # Orient any edge X *-* Y from past
                    # to future as X --> Y
                    G.set_endpoint(Y, X, Endpoints.TAIL)
                    G.set_endpoint(X, Y, Endpoints.HEAD)

        is_closed = False
        while not is_closed:
            is_closed = True
            is_closed &= self._R1(G)
            is_closed &= self._R2(G)
            is_closed &= self._R3(G)
            is_closed &= self._R4(G)

        return G
