from typing import List, Set, Tuple
from itertools import product

from .backdoor_criterion import is_backdoor_adjustment_set
from ..structure import CausalModel
from ..utils import _powerset, _as_set


def is_frontdoor_adjustment_set(G: CausalModel, X: str, Y: str, Z: str = None) -> bool:
    X, Y, Z = _as_set(X), _as_set(Y), _as_set(Z)

    # A set of variables Z is said to satisfy the front-door criterion
    # relative to an ordered pair of variables (X, Y) if:

    # (i) Z intercepts all directed paths from X to Y;
    if not all(Z.intersection(pi) for (x, y) in product(X, Y) for pi in G.paths(x, y)):
        return False

    # (ii) there is no unblocked back-door path from X to Z; and
    if not is_backdoor_adjustment_set(G, X, Z):
        return False

    # (iii) all back-door paths from Z to Y are blocked by X.
    if not is_backdoor_adjustment_set(G, Z, Y, X):
        return False

    return True


def all_frontdoor_adjustment_sets(G: CausalModel, X: str, Y: str) -> List[Set[str]]:
    X, Y = _as_set(X), _as_set(Y)

    adjustment_variables = G.V - X - Y - G.descendants(X)

    adjustment_sets = [
        set(S)
        for S in _powerset(adjustment_variables)
        if is_frontdoor_adjustment_set(G, X, Y, S)
    ]

    return adjustment_sets


def minimal_frontdoor_adjustment_sets(G: CausalModel, X: str, Y: str) -> List[Set[str]]:
    X, Y = _as_set(X), _as_set(Y)

    if is_frontdoor_adjustment_set(G, X, Y):
        return [set()]

    adjustment_variables = G.V - X - Y - G.descendants(X)

    adjustment_sets = []
    for S in _powerset(adjustment_variables):
        S = set(S)
        # An adjustment set is minimal if it is not
        # a super set of any smaller adjustment set
        is_super_set = any(S.issuperset(s) for s in adjustment_sets)
        if not is_super_set and is_frontdoor_adjustment_set(G, X, Y, S):
            adjustment_sets.append(S)

    return adjustment_sets


def frontdoor_paths(G: CausalModel, X: str, Y: str) -> Set[Tuple[str]]:
    X, Y = _as_set(X), _as_set(Y)

    return G.paths(X, Y)
