from typing import Set

import pandas as pd

from .ci import CI
from ..backend import PAG
from ..utils import _powerset


class FCI(CI):

    def fit(self, data: pd.DataFrame):
        G = super().fit(data)

        V = sorted(G.V)
        G = PAG(G.V, G.E)

        self._R0(G, V)

        def _pos_d_sep(X: str, Y: str) -> Set[str]:
            pds = set()
            for Z in G.V:
                if Z not in (X, Y):
                    for p in G.paths(X, Z):
                        if all(
                            G.is_collider(S, W, T) \
                            or (not G.is_non_collider(S, W, T) \
                            and G.has_edge(S, W) \
                            and G.has_edge(W, T) \
                            and G.has_edge(S, T))
                            for (S, W, T) in zip(p, p[1:], p[2:])
                        ):
                            pds.add(Z)
            return pds

        for (X, Y) in G.E:
            for S in _powerset((_pos_d_sep(X, Y) | _pos_d_sep(Y, X))):
                _, p_value, _ = self._method(data, X, Y, S)
                if p_value > self._alpha:
                    G.del_edge(X, Y)
                    self._sepset[(X, Y)].add(S)
                    self._sepset[(Y, X)].add(S)
                    break

        return G
