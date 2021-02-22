from collections import defaultdict
from inspect import getmembers, isfunction
from itertools import combinations, permutations
from typing import Dict, Optional, Iterable, Set, Tuple

import pandas as pd

from ..backend import Endpoints, EndpointGraph, Graph, conditional_independence_test
from ..utils import _try_get

methods = dict(getmembers(conditional_independence_test, isfunction))


class PC:

    _sepset: Dict[Tuple[str], Set[str]]

    def __init__(self, method: str = "t_student", alpha: float = 0.05):
        # Init the Sepset container
        self._sepset = defaultdict(set)
        self._method = method if not isinstance(method, str) else _try_get(method, methods)
        self._alpha = alpha

    def fit(self, data: pd.DataFrame):
        # (Phase I - S1) Form the complete undirected graph C on the vertex set V.
        V = sorted(set(data.columns))
        C = Graph.from_complete(V)

        # Let Adjacencies(C,A) be the set of vertices adjacent to A in graph C.
        repeat, n = True, 0
        while repeat:
            repeat = False  # (***)
            # select an (*) ordered pair of variables X and Y that are adjacent in C
            # such that Adjacencies(C,X)\{Y} has cardinality greater than or equal to n,
            for (X, Y) in combinations(V, 2):
                if C.has_edge(X, Y):
                    # and a (**) subset S of Adjacencies(C,X)\{Y} of cardinality n,
                    for S in combinations(C.neighbors(X) - {Y}, n):
                        repeat = True   # (***)
                        # and if X and Y are d-separated given S delete edge X - Y
                        _, p_value, _ = self._method(data, X, Y, S)
                        if p_value > self._alpha:
                            C.del_edge(X, Y)
                            # and record S in Sepset(X,Y) and Sepset(Y,X);
                            self._sepset[(X, Y)].add(frozenset(S))
                            self._sepset[(Y, X)].add(frozenset(S))
                            break
            # until [*] all ordered pairs of adjacent variables X and Y such that
            # Adjacencies(C,X)\{Y} has cardinality greater than or equal to n and
            # all subsets [**] S of Adjacencies(C,X)\{Y} of cardinality n have been
            # tested for d-separation;
            n += 1
        # until [***] for each ordered pair of adjacent vertices X, Y,
        # Adjacencies(C,X)\{Y} is of cardinality less than n.

        return C

    def fit_transform(
        self,
        data: pd.DataFrame,
        blacklist: Optional[Iterable[Tuple[str, str]]] = None,
        whitelist: Optional[Iterable[Tuple[str, str]]] = None
    ):
        return self.transform(self.fit(data), blacklist, whitelist)

    def transform(
        self,
        G: Graph,
        blacklist: Optional[Iterable[Tuple[str, str]]] = None,
        whitelist: Optional[Iterable[Tuple[str, str]]] = None
    ):
        V = sorted(G.V)
        C = EndpointGraph(G.V, G.E)

        # (Phase I - S2) For each triple of vertices X, Y, Z
        for (X, Y, Z) in permutations(V, 3):
            # such that the pair X, Y and the pair Y, Z are each adjacent in C
            # but the pair X, Z are not adjacent in C,
            if C.has_undirected_edge(X, Y) and C.has_undirected_edge(Y, Z) and not C.has_edge(X, Z):
                # orient X - Y - Z as X -> Y <- Z if and only if Y is not in Sepset(X,Z).
                if {Y} not in self._sepset[(X, Z)]:
                    C.set_endpoint(X, Y, Endpoints.HEAD)
                    C.set_endpoint(Z, Y, Endpoints.HEAD)

        # (Phase II') Apply Meek Rules until graph is closed.
        def _R1() -> bool:
            is_closed = True
            # MEEK RULE R1: If X -> Y, Y and Z are adjacent, X and Z are not adjacent,
            # and there is no arrowhead at Y, then orient Y - Z as Y -> Z.
            for (X, Y, Z) in permutations(V, 3):
                if C.has_directed_edge(X, Y) and C.has_undirected_edge(Y, Z) and not C.has_edge(X, Z):
                    C.set_endpoint(Y, Z, Endpoints.HEAD)
                    is_closed = False
            return is_closed

        def _R2() -> bool:
            is_closed = True
            # MEEK RULE R2: If X -> Y, Y -> Z, X and Z are adjacent,
            # and there is no arrowhead at Z, then orient X - Z as X -> Z.
            for (X, Y, Z) in permutations(V, 3):
                if C.has_directed_edge(X, Y) and C.has_directed_edge(Y, Z) and C.has_undirected_edge(X, Z):
                    C.set_endpoint(X, Z, Endpoints.HEAD)
                    is_closed = False
            return is_closed

        def _R3() -> bool:
            is_closed = True
            # MEEK RULE R3: If X - Y, Y - Z, Y - W, X -> W
            # and Z -> W, then orient Y - W as Y -> W.
            for (X, Y, Z, W) in permutations(V, 4):
                if C.has_undirected_edge(X, Y) and C.has_undirected_edge(Y, Z) and C.has_undirected_edge(Y, W) \
                        and C.has_directed_edge(X, W) and C.has_directed_edge(Z, W):
                    C.set_endpoint(Y, W, Endpoints.HEAD)
                    is_closed = False
            return is_closed

        def _R4() -> bool:
            is_closed = True
            # MEEK RULE R4: If X - Y, Y - Z, (Y - W or Y -> W or W -> Y), W -> X
            # and Z -> W, then orient X - Y as Y -> X.
            for (X, Y, Z, W) in permutations(V, 4):
                if C.has_undirected_edge(X, Y) and C.has_undirected_edge(Y, Z) and C.has_edge(Y, W) \
                        and C.has_directed_edge(W, X) and C.has_directed_edge(Z, W):
                    C.set_endpoint(Y, X, Endpoints.HEAD)
                    is_closed = False
            return is_closed

        # Close graph w.r.t. to Meek rules except R4.
        is_closed = False
        while not is_closed:
            is_closed = _R1() & _R2() & _R3() # (****)
        # until [****] no more edges can be oriented.

        # (Phase II'')
        # Check if graph is consistent with blacklist.
        if blacklist:
            for (X, Y) in blacklist:
                if C.has_directed_edge(X, Y):
                    raise ValueError(f"Graph contains forbidden edge ({X}->{Y}).")
        if whitelist:
            # Check if graph is consistent with whitelist.
            for (X, Y) in whitelist:
                if not C.has_edge(X, Y) or C.has_directed_edge(Y, X):
                    raise ValueError(f"Graph does not contain required edge ({X}->{Y}).")
            # Orient edges in whitelist and close graph w.r.t. to Meek rules.
            for (X, Y) in whitelist:
                C.set_endpoint(X, Y, Endpoints.HEAD)
                is_closed = False
                while not is_closed:
                    is_closed = _R1() & _R2() & _R3() & _R4()

        return C
