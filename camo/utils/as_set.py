from typing import Iterable, Set, Union

def _as_set(Z: Union[str, Iterable[str]] = None) -> Set[str]:
    Z = set([Z]) if isinstance(Z, str) else Z
    Z = set() if Z is None else set(Z)
    return Z
