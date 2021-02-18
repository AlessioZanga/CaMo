from typing import List, Set, Tuple

from ..structure import CausalModel
from ..utils import _powerset, _as_set


def is_backdoor_adjustment_set(G: CausalModel, X: str, Y: str, Z: str = None) -> bool:
    X, Y, Z = _as_set(X), _as_set(Y), _as_set(Z)

    # A set of variables Z satisfies the back-door criterion
    # relative to an ordered pair of variables (X, Y) if:

    # (i) no node in Z is a descendant of X; and
    if Z & G.descendants(X):
        return False

    # (ii) Z blocks every path between X and Y that contains an arrow into X.
    return G.is_d_separated(G.parents(X), Y, Z | X)


def all_backdoor_adjustment_sets(G: CausalModel, X: str, Y: str) -> List[Set[str]]:
    X, Y = _as_set(X), _as_set(Y)

    adjustment_variables = G.V - X - Y - G.descendants(X)

    adjustment_sets = [
        set(S)
        for S in _powerset(adjustment_variables)
        if is_backdoor_adjustment_set(G, X, Y, S)
    ]

    return adjustment_sets


def minimal_backdoor_adjustment_sets(G: CausalModel, X: str, Y: str) -> List[Set[str]]:
    X, Y = _as_set(X), _as_set(Y)

    if is_backdoor_adjustment_set(G, X, Y):
        return [set()]

    adjustment_variables = G.V - X - Y - G.descendants(X)

    adjustment_sets = []
    for S in _powerset(adjustment_variables):
        S = set(S)
        # An adjustment set is minimal if it is not
        # a super set of any smaller adjustment set
        is_super_set = any(S.issuperset(s) for s in adjustment_sets)
        if not is_super_set and is_backdoor_adjustment_set(G, X, Y, S):
            adjustment_sets.append(S)

    return adjustment_sets


def backdoor_paths(G: CausalModel, X: str, Y: str) -> Set[Tuple[str]]:
    X, Y = _as_set(X), _as_set(Y)

    return G.to_undirected().paths(X, Y) - G.paths(X, Y)
