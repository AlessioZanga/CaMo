from typing import List, Set, Tuple

from ..structure import SCM
from ..utils import powerset


def is_backdoor_adjustment_set(model: SCM, X: str, Y: str, Z: str = None) -> bool:
    Z = set([Z]) if isinstance(Z, str) else Z
    Z = set() if Z is None else set(Z)

    Z |= {X}
    
    return all(model.is_d_separated(p, Y, Z) for p in model.parents(X))


def backdoor_all_adjustment_sets(model: SCM, X: str, Y: str) -> List[Set[str]]:
    if is_backdoor_adjustment_set(model, X, Y):
        return []
    
    adjustment_variables = model.endogenous_variables - {X, Y, *model.descendants(X)}

    adjustment_sets = [
        set(S)
        for S in powerset(adjustment_variables)
        if is_backdoor_adjustment_set(model, X, Y, S)
    ]

    return adjustment_sets

def backdoor_minimal_adjustment_sets(model: SCM, X: str, Y: str) -> List[Set[str]]:
    if is_backdoor_adjustment_set(model, X, Y):
        return []
    
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
    pass
