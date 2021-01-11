from typing import List, Set, Tuple

from ..structure import CausalModel
from ..utils import _powerset, _as_set


def is_backdoor_adjustment_set(G: CausalModel, X: str, Y: str, Z: str = None) -> bool:
    Z = _as_set(Z)

    Z |= {X}

    # A set of variables Z satisfies the back-door criterion
    # relative to an ordered pair of variables (X, Y) if:

    # (i) no node in Z is a descendant of X; and
    if Z & G.descendants(X):
        return False

    # (ii) Z blocks every path between X and Y that contains an arrow into X.
    if not all(G.is_d_separated(p, Y, Z) for p in G.parents(X)):
        return False

    return True


def all_backdoor_adjustment_sets(G: CausalModel, X: str, Y: str) -> List[Set[str]]:
    adjustment_variables = G.endogenous_variables - {X, Y, *G.descendants(X)}

    adjustment_sets = [
        set(S)
        for S in _powerset(adjustment_variables)
        if is_backdoor_adjustment_set(G, X, Y, S)
    ]

    return adjustment_sets


def minimal_backdoor_adjustment_sets(G: CausalModel, X: str, Y: str) -> List[Set[str]]:
    if is_backdoor_adjustment_set(G, X, Y):
        return [set()]

    adjustment_variables = G.endogenous_variables - {X, Y, *G.descendants(X)}

    adjustment_sets = []
    for S in _powerset(adjustment_variables):
        S = set(S)
        # An adjustment set is minimal if it is not
        # a super set of any smaller adjustment set
        is_super_set = any(S.issuperset(s) for s in adjustment_sets)
        if not is_super_set and is_backdoor_adjustment_set(G, X, Y, S):
            adjustment_sets.append(S)

    return adjustment_sets


def backdoor_paths(model: CausalModel, X: str, Y: str) -> List[Tuple[str]]:
    raise NotImplementedError()  # TODO
