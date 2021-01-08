from typing import List, Set, Tuple

from .backdoor_criterion import is_backdoor_adjustment_set
from ..structure import SCM


def is_frontdoor_adjustment_set(model: SCM, X: str, Y: str, Z: str = None) -> bool:
    Z = set([Z]) if isinstance(Z, str) else Z
    Z = set() if Z is None else set(Z)

    # A set of variables Z is said to satisfy the front-door criterion
    # relative to an ordered pair of variables (X, Y) if:

    # (i) Z intercepts all directed paths from X to Y;
    if not all(Z.intersection(path) for path in model.paths(X, Y)):
        return False

    # (ii) there is no unblocked back-door path from X to Z; and
    if not is_backdoor_adjustment_set(model, X, Z):
        return False

    # (iii) all back-door paths from Z to Y are blocked by X.
    if not all(is_backdoor_adjustment_set(model, z, Y, X) for z in Z):
        return False

    return True
