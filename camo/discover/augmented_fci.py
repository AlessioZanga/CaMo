from itertools import permutations
from typing import Optional, Iterable, Tuple

from .fci import FCI
from ..backend import Endpoints, PAG


class AugmentedFCI(FCI):

    def _R5(self, G: PAG):
        is_close = True
        for X in G.V:
            for Y in G.neighbors(X) - {X}:
                if G.is_circle_circle(X, Y):
                    for p in G.paths(X, Y):
                        if (len(p) > 3 and
                            not G.has_edge(Y, p[1]) and
                            not G.has_edge(X, p[-2]) and
                            all(    # circle path
                                G.is_circle_circle(u, v)
                                for (u, v) in zip(p, p[1:])
                            ) and G.is_uncovered_path(p)):
                            for (u, v) in zip(p, p[1:]):
                                G.set_endpoint(v, u, Endpoints.TAIL)
                                G.set_endpoint(u, v, Endpoints.TAIL)
                            G.set_endpoint(X, Y, Endpoints.TAIL)
                            G.set_endpoint(Y, X, Endpoints.TAIL)
                            is_close = False
        return is_close

    def _R6(self, G: PAG):
        is_close = True
        for Y in G.V:
            for (X, Z) in permutations(G.neighbors(Y) - {Y}, 2):
                if (G.is_tail_tail(X, Y) and
                    G.is_any_circle(Z, Y)):
                    G.set_endpoint(Z, Y, Endpoints.TAIL)
                    is_close = False
        return is_close

    def _R7(self, G: PAG):
        is_close = True
        for Y in G.V:
            for (X, Z) in permutations(G.neighbors(Y) - {Y}, 2):
                if (not G.has_edge(X, Z) and
                    G.is_tail_circle(X, Y) and
                    G.is_any_circle(Z, Y)):
                    G.set_endpoint(Z, Y, Endpoints.TAIL)
                    is_close = False
        return is_close

    def _R8(self, G: PAG):
        is_close = True
        for Y in G.V:
            for X in G.neighbors(Y) - {Y}:
                for Z in (G.neighbors(X) & G.neighbors(Y)) - {X, Y}:
                    if (G.is_circle_head(X, Z) and
                        G.is_tail_head(Y, Z) and
                        (G.is_tail_head(X, Y) or G.is_tail_circle(X, Y))):
                        G.set_endpoint(Z, X, Endpoints.TAIL)
                        is_close = False
        return is_close

    def _R9(self, G: PAG):
        is_close = True
        for X in G.V:
            for Y in G.neighbors(X) - {X}:
                if G.is_circle_head(X, Y):
                    for p in G.paths(X, Y):
                        if (len(p) > 3 and
                            not G.has_edge(Y, p[1]) and
                            G.is_uncovered_path(p) and
                            G.is_potentially_directed_path(p)):
                            G.set_endpoint(Y, X, Endpoints.TAIL)
                            is_close = False
                            break
        return is_close

    def _R10(self, G: PAG):
        is_close = True
        for W in G.V:
            for (X, Y, Z) in permutations(G.neighbors(W) - {W}, 3):
                if (G.is_circle_head(X, W) and
                    G.is_tail_head(Y, W) and
                    G.is_tail_head(Z, W)):
                    done = False
                    for p1 in G.paths(X, Y):
                        if (G.is_uncovered_path(p1) and
                            G.is_potentially_directed_path(p1)):
                            for p2 in G.paths(X, Z):
                                if (G.is_uncovered_path(p2) and
                                    G.is_potentially_directed_path(p2)):
                                    u, v = p1[1], p2[1]
                                    if (u != v and not G.has_edge(u, v)):
                                        G.set_endpoint(W, X, Endpoints.TAIL)
                                        is_close = False
                                        done = True
                                        break
                            if done:
                                break
        return is_close

    def transform(
        self,
        G: PAG,
        blacklist: Optional[Iterable[Tuple[str, str]]] = None,
        whitelist: Optional[Iterable[Tuple[str, str]]] = None
    ):
        G = super().transform(G, blacklist, whitelist)

        is_closed = False
        while not is_closed:
            is_closed = True
            is_closed &= self._R5(G)
            is_closed &= self._R6(G)
            is_closed &= self._R7(G)
        
        is_closed = False
        while not is_closed:
            is_closed = True
            is_closed &= self._R8(G)
            is_closed &= self._R9(G)
            is_closed &= self._R10(G)

        return G
