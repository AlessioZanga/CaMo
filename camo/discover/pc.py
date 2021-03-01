from collections import defaultdict
from functools import partial
from inspect import getmembers, isfunction
from itertools import combinations, permutations
from typing import Dict, Optional, Iterable, Set, Tuple

import pandas as pd

from ..backend import Endpoints, PAG, Graph, conditional_independence_test as ci
from ..utils import _as_set, _try_get

methods = dict(getmembers(ci, lambda x: isfunction(x) or isinstance(x, partial)))


class PC:

    _sepset: Dict[Tuple[str], Set[str]]

    def __init__(self, method: str = "t_student", alpha: float = 0.05):
        self._method = method if not isinstance(method, str) else _try_get(method, methods)
        self._alpha = alpha

    def fit(self, data: pd.DataFrame):
        self._sepset = defaultdict(set)
        # (Phase I - S1) Form the complete undirected graph G on the vertex set V.
        G = Graph.from_complete(data.columns)

        # Let Adjacencies(G,A) be the set of vertices adjacent to A in graph G.
        repeat, n = True, 0
        while repeat:
            repeat = False  # (***)
            Nb = {X: G.neighbors(X) for X in G.V}
            # select an (*) ordered pair of variables X and Y that are adjacent in G
            # such that Adjacencies(G,X)\{Y} has cardinality greater than or equal to n,
            for (X, Y) in G.E:
                # and a (**) subset S of Adjacencies(G,X)\{Y} of cardinality n,
                for S in combinations(Nb[X] - {Y}, n):
                    repeat = True   # (***)
                    # and if X and Y are d-separated given S delete edge X - Y
                    _, p_value, _ = self._method(data, X, Y, S)
                    if p_value > self._alpha:
                        G.del_edge(X, Y)
                        # and record S in Sepset(X,Y) and Sepset(Y,X);
                        self._sepset[(X, Y)].add(frozenset(S))
                        self._sepset[(Y, X)].add(frozenset(S))
                        break
            # until [*] all ordered pairs of adjacent variables X and Y such that
            # Adjacencies(G,X)\{Y} has cardinality greater than or equal to n and
            # all subsets [**] S of Adjacencies(G,X)\{Y} of cardinality n have been
            # tested for d-separation;
            n += 1
        # until [***] for each ordered pair of adjacent vertices X, Y,
        # Adjacencies(G,X)\{Y} is of cardinality less than n.

        return G

    def fit_transform(
        self,
        data: pd.DataFrame,
        blacklist: Optional[Iterable[Tuple[str, str]]] = None,
        whitelist: Optional[Iterable[Tuple[str, str]]] = None
    ):
        return self.transform(self.fit(data), blacklist, whitelist)

    def _R0(self, G: PAG) -> bool:
        is_closed = True
        for (X, Y, Z) in permutations(G.V, 3):
            # such that the pair X, Y and the pair Y, Z are each adjacent in G
            # but the pair X, Z are not adjacent in G,
            if (G.is_tail_tail(X, Y) and
                G.is_tail_tail(Y, Z) and
                not G.has_edge(X, Z)):
                # orient X - Y - Z as X -> Y <- Z if and only if Y is not in Sepset(X,Z).
                if {Y} not in self._sepset[(X, Z)]:
                    G.set_endpoint(X, Y, Endpoints.HEAD)
                    G.set_endpoint(Z, Y, Endpoints.HEAD)
                    is_closed = False
        return is_closed

    def _R1(self, G: PAG) -> bool:
        is_closed = True
        # MEEK RULE R1: If X -> Y, Y and Z are adjacent, X and Z are not adjacent,
        # and there is no arrowhead at Y, then orient Y - Z as Y -> Z.
        for (X, Y, Z) in permutations(G.V, 3):
            if (G.is_tail_head(X, Y) and
                G.is_tail_tail(Y, Z) and
                not G.has_edge(X, Z)):
                G.set_endpoint(Y, Z, Endpoints.HEAD)
                is_closed = False
        return is_closed

    def _R2(self, G: PAG) -> bool:
        is_closed = True
        # MEEK RULE R2: If X -> Y, Y -> Z, X and Z are adjacent,
        # and there is no arrowhead at Z, then orient X - Z as X -> Z.
        for (X, Y, Z) in permutations(G.V, 3):
            if (G.is_tail_head(X, Y) and
                G.is_tail_head(Y, Z) and
                G.is_tail_tail(X, Z)):
                G.set_endpoint(X, Z, Endpoints.HEAD)
                is_closed = False
        return is_closed

    def _R3(self, G: PAG) -> bool:
        is_closed = True
        # MEEK RULE R3: If X - Y, Y - Z, Y - W, X -> W
        # and Z -> W, then orient Y - W as Y -> W.
        for (X, Y, Z, W) in permutations(G.V, 4):
            if (G.is_tail_tail(X, Y) and
                G.is_tail_tail(Y, Z) and
                G.is_tail_tail(Y, W) and
                G.is_tail_head(X, W) and
                G.is_tail_head(Z, W)):
                G.set_endpoint(Y, W, Endpoints.HEAD)
                is_closed = False
        return is_closed

    def _R4(self, G: PAG) -> bool:
        is_closed = True
        # MEEK RULE R4: If X - Y, Y - Z, (Y - W or Y -> W or W -> Y), W -> X
        # and Z -> W, then orient X - Y as Y -> X.
        for (X, Y, Z, W) in permutations(G.V, 4):
            if (G.is_tail_tail(X, Y) and
                G.is_tail_tail(Y, Z) and
                G.is_tail_head(W, X) and
                G.is_tail_head(Z, W) and
                G.has_edge(Y, W)):
                G.set_endpoint(Y, X, Endpoints.HEAD)
                is_closed = False
        return is_closed

    def _KB(
        self,
        G: PAG,
        blacklist: Optional[Iterable[Tuple[str, str]]] = None,
        whitelist: Optional[Iterable[Tuple[str, str]]] = None,
        endpoint: int = Endpoints.TAIL
    ):
        B, W = _as_set(blacklist), _as_set(whitelist)
        if B:
            for (X, Y) in B:
                if G.has_edge(X, Y):
                    if (Y, X) not in blacklist:
                        # If only one direction is blacklisted, orient edge.
                        G.set_endpoint(X, Y, Endpoints.TAIL)
                        G.set_endpoint(Y, X, Endpoints.HEAD)
                    else:
                        # Else if both directions are blacklisted, delete edge.
                        G.del_edge(X, Y)
                        B.remove((Y, X))
        if W:
            for (X, Y) in W:
                if not G.has_edge(X, Y):
                    # Add edge if not present
                    G.add_edge(X, Y, endpoint)
                if (Y, X) not in W:
                    # If only one direction is blacklisted, orient edge.
                    G.set_endpoint(X, Y, Endpoints.HEAD)
                    G.set_endpoint(Y, X, Endpoints.TAIL)
                else:
                    # Else if both directions are whitelisted, do nothing.
                    W.remove((Y, X))
        # Orient edges in whitelist and black list and close graph w.r.t. to Meek rules.

    def transform(
        self,
        G: Graph,
        blacklist: Optional[Iterable[Tuple[str, str]]] = None,
        whitelist: Optional[Iterable[Tuple[str, str]]] = None
    ):
        G = PAG(G.V, G.E)

        # Apply knowledge base (blacklist, whitelist)
        self._KB(G, blacklist, whitelist)

        # (Phase I - S2) For each triple of vertices X, Y, Z
        self._R0(G)

        # (Phase II') Close graph w.r.t. to Meek rules.
        is_closed = False
        while not is_closed:
            is_closed = True
            is_closed &= self._R1(G)
            is_closed &= self._R2(G)
            is_closed &= self._R3(G)
            is_closed &= self._R4(G)
        # until no more edges can be oriented.

        return G
