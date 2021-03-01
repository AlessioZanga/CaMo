from itertools import permutations
from typing import Optional, Iterable, Tuple

from .pc import PC
from ..backend import Endpoints, PAG, Graph


class CI(PC):

    def _R0(self, G: PAG) -> bool:
        is_closed = True
        for (X, Y, Z) in permutations(G.V, 3):
            if (G.is_any_circle(X, Y) and
                G.is_any_circle(Z, Y) and
                not G.has_edge(X, Z)):
                if {Y} not in self._sepset[(X, Z)]:
                    G.set_endpoint(X, Y, Endpoints.HEAD)
                    G.set_endpoint(Z, Y, Endpoints.HEAD)
                else:
                    G.set_non_collider(X, Y, Z)
                is_closed = False
        return is_closed

    def _R1(self, G: PAG) -> bool:
        is_closed = True
        for (X, Y) in permutations(G.V, 2):
            for p in G.paths(X, Y):
                if (G.is_any_circle(X, Y) and
                    G.is_directed_path(p)):
                    G.set_endpoint(X, Y, Endpoints.HEAD)
                    is_closed = False
        return is_closed

    def _R2(self, G: PAG) -> bool:
        is_closed = True
        for (X, Z, Y) in permutations(G.V, 3):
            if (G.is_any_head(X, Z) and
                G.is_any_circle(Y, Z) and
                G.is_non_collider(X, Z, Y)):
                G.set_endpoint(Y, Z, Endpoints.TAIL)
                G.set_endpoint(Z, Y, Endpoints.HEAD)
                is_closed = False
        return is_closed

    def _R3(self, G: PAG) -> bool:
        is_closed = True
        for (X, Z, Y, S) in permutations(G.V, 4):
            if (G.is_any_circle(S, Z) and
                G.is_collider(X, Z, Y) and
                {S} in self._sepset[(X, Y)]):
                is_closed = False
        return is_closed

    def _R4(self, G: PAG) -> bool:
        is_closed = True
        for (S, Z, Y) in permutations(G.V, 3):
            for p in G.paths(S, Y):
                if G.is_discriminating_path(p, Z):
                    X = p[p.index(Z)-1]
                    if (G.has_edge(X, Y) and
                        G.is_any_circle(X, Z)):
                        if {Z} not in self._sepset[(S, Y)]:
                            G.set_endpoint(X, Z, Endpoints.HEAD)
                            G.set_endpoint(Y, Z, Endpoints.HEAD)
                        else:
                            G.set_non_collider(X, Z, Y)
                        is_closed = False
        return is_closed

    def transform(
        self,
        G: Graph,
        blacklist: Optional[Iterable[Tuple[str, str]]] = None,
        whitelist: Optional[Iterable[Tuple[str, str]]] = None
    ):
        G = PAG(G.V, G.E, Endpoints.CIRCLE)

        self._KB(G, blacklist, whitelist, Endpoints.CIRCLE)

        self._R0(G)

        is_closed = False
        while not is_closed:
            is_closed = True
            is_closed &= self._R1(G)
            is_closed &= self._R2(G)
            is_closed &= self._R3(G)
            is_closed &= self._R4(G)

        return G
