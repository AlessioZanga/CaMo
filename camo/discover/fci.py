from collections import defaultdict
from itertools import combinations
from typing import Dict, Set, Tuple

import pandas as pd

from .ci import CI
from ..backend import Endpoints, PAG


class FCI(CI):

    _pdsep: Dict[Tuple[str, str], Set[str]]

    def __init__(self, method: str = "t_student", alpha: float = 0.05):
        super().__init__(method, alpha)
        self._pdsep = defaultdict(set)

    def fit(self, data: pd.DataFrame):
        G = super().fit(data)
        G = PAG(G.V, G.E, Endpoints.CIRCLE)

        self._R0(G)

        def _possible_d_sep(G: PAG, X: str, Y: str = None) -> Set[str]:
            pds = set()
            for Z in G.V - {X, Y}:
                for p in G.paths(X, Z):
                    if all(
                        G.is_collider(P, Q, R) or G.has_edge(P, R)
                        for (P, Q, R) in zip(p, p[1:], p[2:])
                    ):
                        pds.add(Z)
                        break
            return pds

        for X in G.V:
            self._pdsep[X] = _possible_d_sep(G, X)
            for Y in G.neighbors(X) - {X}:
                repeat, n = True, 0
                while repeat:
                    repeat = False
                    for S in combinations(self._pdsep[X] - {Y}, n):
                        repeat = True
                        _, p_value, _ = self._method(data, X, Y, S)
                        if p_value > self._alpha:
                            G.del_edge(X, Y)
                            self._dsep[(X, Y)] = set(S)
                            self._dsep[(Y, X)] = set(S)
                            repeat = False
                            break
                    n += 1

        return G
