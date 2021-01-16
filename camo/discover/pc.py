from collections import defaultdict
from itertools import combinations, permutations

import pandas as pd

from ..backend import Graph, DirectedGraph
from ..backend import chi_square    # pylint: disable=no-name-in-module


def pc(data: pd.DataFrame, alpha: float = 0.01):
    # Init the Sepset container
    sepset = defaultdict(set)

    # (A) Form the complete undirected graph C on the vertex set V.
    V = set(data.columns)
    C = Graph.from_complete(V)

    # (B) Let Adjacencies(C,A) be the set of vertices adjacent to A in graph C.
    repeat, n = True, 0
    while repeat:
        repeat = False  # (***)
        # select an (*) ordered pair of variables X and Y that are adjacent in C
        # such that Adjacencies(C,X)\{Y} has cardinality greater than or equal to n,
        for (X, Y) in combinations(V, 2):
            if C.has_edge(X, Y):
                # and a (**) subset S of Adjacencies(C,X)\{Y} of cardinality n,
                for S in combinations(C.neighbors(X) - {Y}, n + 1):
                    # Check if edge has not been removed yet.
                    if C.has_edge(X, Y):
                        repeat = True   # (***)
                        # and if X and Y are d-separated given S delete edge X - Y
                        _, p_value, _ = chi_square(data, X, Y, S)
                        if p_value > alpha:
                            C.del_edge(X, Y)
                            # and record S in Sepset(X,Y) and Sepset(Y,X);
                            sepset[(X, Y)].add(frozenset(S))
                            sepset[(Y, X)].add(frozenset(S))
        # until [*] all ordered pairs of adjacent variables X and Y such that
        # Adjacencies(C,X)\{Y} has cardinality greater than or equal to n and
        # all subsets [**] S of Adjacencies(C,X)\{Y} of cardinality n have been
        # tested for d-separation;
        n += 1
    # until [***] for each ordered pair of adjacent vertices X, Y,
    # Adjacencies(C,X)\{Y} is of cardinality less than n.

    # TODO: Until a partially-directed graph class is implemented,
    # orient the graph by duplicating edges, one for each direction.
    C = DirectedGraph.from_undirected(C)

    # (C) For each triple of vertices X, Y, Z
    for (X, Y, Z) in permutations(V, 3):
        # such that the pair X, Y and the pair Y, Z are each adjacent in C
        # but the pair X, Z are not adjacent in C,
        # TODO: Fix when partially-directed graph class is implemented.
        if  (C.has_edge(X, Y) and C.has_edge(Y, X)) and \
            (C.has_edge(Y, Z) and C.has_edge(Z, Y)) and \
            not (C.has_edge(X, Z) or C.has_edge(Z, X)):
            # orient X - Y - Z as X -> Y <- Z if and only if Y is not in Sepset(X,Z).
            if {Y} not in sepset[(X, Z)]:
                C.del_edge(Y, X)
                C.del_edge(Y, Z)

    # (D)
    repeat = True
    while repeat:
        repeat = False  # (****)
        for (X, Y, Z) in permutations(V, 3):
            # If X -> Y, Y and Z are adjacent, X and Z are not adjacent,
            # and there is no arrowhead at Y, then orient Y - Z as Y -> Z.
            # TODO: Fix when partially-directed graph class is implemented.
            if  C.has_edge(X, Y) and \
                (C.has_edge(Y, Z) and C.has_edge(Z, Y)) and \
                not (C.has_edge(X, Z) or C.has_edge(Z, X)):
                C.del_edge(Z, Y)
                repeat = True   # (****)
            # If there is a directed path from X to Y, and an edge between
            # X and Y, then orient X - Y as X -> Y.
            # TODO: Fix when partially-directed graph class is implemented.
            if (C.has_edge(X, Y) and C.has_edge(Y, X)) and \
                C.has_path(X, Y):
                C.del_edge(Y, X)
                repeat = True   # (****)
        # until [****] no more edges can be oriented.
    
    return C
