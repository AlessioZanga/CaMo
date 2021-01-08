from typing import List, Set, Tuple

from ..structure import SCM
from ..utils import powerset


def is_backdoor_adjustment_set(model: SCM, X: str, Y: str, Z: str = None) -> bool:
    Z = set([Z]) if isinstance(Z, str) else Z
    Z = set() if Z is None else set(Z)

    Z |= {X}

    # A set of variables Z satisfies the back-door criterion
    # relative to an ordered pair of variables (X, Y) if:

    # (i) no node in Z is a descendant of X; and
    if Z & model.descendants(X):
        return False

    # (ii) Z blocks every path between X and Y that contains an arrow into X.
    if not all(model.is_d_separated(p, Y, Z) for p in model.parents(X)):
        return False
    
    return True


def all_backdoor_adjustment_sets(model: SCM, X: str, Y: str) -> List[Set[str]]:
    adjustment_variables = model.endogenous_variables - {X, Y, *model.descendants(X)}

    adjustment_sets = [
        set(S)
        for S in powerset(adjustment_variables)
        if is_backdoor_adjustment_set(model, X, Y, S)
    ]

    return adjustment_sets

def minimal_backdoor_adjustment_sets(model: SCM, X: str, Y: str) -> List[Set[str]]:
    adjustment_variables = model.endogenous_variables - {X, Y, *model.descendants(X)}

    adjustment_sets = []
    for S in powerset(adjustment_variables):
        S = set(S)
        # An adjustment set is minimal if it is not
        # a super set of any smaller adjustment set
        is_super_set = any(S.issuperset(s) for s in adjustment_sets)
        if not is_super_set and is_backdoor_adjustment_set(model, X, Y, S):
            adjustment_sets.append(S)

    return adjustment_sets


def backdoor_paths(model: SCM, X: str, Y: str) -> List[Tuple[str]]:
    raise NotImplementedError()
