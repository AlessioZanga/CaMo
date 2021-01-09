from itertools import chain, combinations
from typing import Any, Iterable


def _powerset(iterable: Iterable[Any]):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))
