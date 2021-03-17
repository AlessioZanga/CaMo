from typing import Iterable, Set, Union

def _as_set(Z: Union[str, Iterable[str]]) -> Set[str]:
    if Z is None:
        return set()
    if isinstance(Z, str):
        return set([Z])
    return set(Z)
