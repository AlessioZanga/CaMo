from itertools import combinations, permutations
from typing import Dict, List, Optional, Iterable, Tuple

from .pc import PC
from ..backend import Endpoints, PartialAncestralGraph, Graph


class CI(PC):

    def __init__(self, method: str = "t_student", alpha: float = 0.05):
        super().__init__(method, alpha)

    def _R0(self, G: PartialAncestralGraph, V: List[str]) -> bool:
        is_closed = True
        for (X, Y, Z) in permutations(V, 3):
            if G.has_edge(X, Y) and G.has_edge(Y, Z) and not G.has_edge(X, Z):
                if {Y} not in self._sepset[(X, Z)]:
                    G.set_endpoint(X, Y, Endpoints.HEAD)
                    G.set_endpoint(Z, Y, Endpoints.HEAD)
                    is_closed = False
                else:
                    G.set_definite_non_collider(X, Y, Z)
        return is_closed

    def _R1(self, G: PartialAncestralGraph, V: List[str]) -> bool:
        is_closed = True
        for (X, Y) in permutations(V, 2):
            if G.is_any_circle(X, Y) and G.has_directed_path(X, Y):
                G.set_endpoint(X, Y, Endpoints.HEAD)
                is_closed = False
        return is_closed

    def _R2(self, G: PartialAncestralGraph, V: List[str]) -> bool:
        is_closed = True
        for (X, Z, Y) in permutations(V, 3):
            if G.is_any_head(X, Z) and G.is_any_circle(Y, Z) \
                and G.is_definite_non_collider(X, Z, Y):
                G.set_endpoint(Y, Z, Endpoints.TAIL)
                G.set_endpoint(Z, Y, Endpoints.HEAD)
                is_closed = False
        return is_closed

    def _R3(self, G: PartialAncestralGraph, V: List[str]) -> bool:
        is_closed = True
        for (X, Z, Y, S) in permutations(V, 4):
            if G.is_any_head(X, Z) and G.is_any_head(Y, Z) \
                and G.is_any_circle(S, Z) and {S} in self._sepset[(X, Y)]:
                G.set_endpoint(S, Z, Endpoints.HEAD)
                is_closed = False
        return is_closed

    def _R4(self, G: PartialAncestralGraph, V: List[str]) -> bool:
        is_closed = True
        for (S, Z, Y) in permutations(V, 3):
            for p in G.all_definite_discriminating_paths(S, Y, Z):
                X = p[p.index(Z)-1]
                if G.has_edge(X, Y) and G.has_edge(Y, Z) \
                    and not (G.is_any_head(X, Y) and G.is_any_head(Y, Z)):
                    if {Z} not in self._sepset[(S, Y)]:
                        G.set_endpoint(X, Z, Endpoints.HEAD)
                        G.set_endpoint(Y, Z, Endpoints.HEAD)
                    else:
                        G.set_definite_non_collider(X, Z, Y)
                    is_closed = False
        return is_closed

    def transform(
        self,
        G: Graph,
        blacklist: Optional[Iterable[Tuple[str, str]]] = None,
        whitelist: Optional[Iterable[Tuple[str, str]]] = None
    ):
        V = sorted(G.V)
        C = PartialAncestralGraph(G.V, G.E, Endpoints.CIRCLE)

        self._R0(C, V)

        is_closed = False
        while not is_closed:
            is_closed = self._R1(C, V) \
                and self._R2(C, V) \
                and self._R3(C, V) \
                and self._R4(C, V)

        return C
