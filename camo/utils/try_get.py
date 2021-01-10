from typing import Any, Dict


def _try_get(key: str, collection: Dict[str, Any]) -> Any:
    try:
        value = collection[key]
    except KeyError:
        raise ValueError(
            f"Value '{key}' not found, available values are {list(collection.keys())}."
        )
    return value
