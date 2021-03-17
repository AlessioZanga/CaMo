from itertools import chain, combinations
from typing import Any, Iterable


def _powerset(iterable: Iterable[Any]):
    s = list(iterable)
    return (
        set(c)
        for c in chain.from_iterable(
            combinations(s, r) for r in range(len(s)+1)
        )
    )
