from typing import Iterable, Set, Union

def _as_set(Z: Union[str, Iterable[str]] = None) -> Set[str]:
    Z = set([Z]) if isinstance(Z, str) else Z
    Z = set(Z) if Z is not None else set()
    return Z
