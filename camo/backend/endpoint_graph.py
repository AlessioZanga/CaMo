from enum import IntEnum
from typing import Dict, Iterable, Optional, Tuple

from .graph import Graph


class Endpoints(IntEnum):
    ALL = 42        # *
    TAIL = 45       # -
    HEAD = 62       # >
    CIRCLE = 111    # o


class EndpointGraph(Graph):

    _endpoints: Dict[Tuple[str, str], int]

    def __init__(
        self,
        V: Optional[Iterable[str]] = None,
        E: Optional[Iterable[Tuple[str, str]]] = None
    ):
        super().__init__(V, E)
        # Initialize dict
        self._endpoints = {}
        # Set default endpoints
        for (u, v) in E:
            self.set_endpoint(u, v, Endpoints.ALL)
            self.set_endpoint(v, u, Endpoints.ALL)

    def add_edge(self, u: str, v: str) -> None:
        self._G.add_edge(u, v)
        self.set_endpoint(u, v, Endpoints.ALL)
        self.set_endpoint(v, u, Endpoints.ALL)

    def del_edge(self, u: str, v: str) -> None:
        self._G.remove_edge(u, v)
        self.unset_endpoint(u, v)
        self.unset_endpoint(v, u)

    def has_endpoint(self, u: str, v: str, endpoint: int) -> bool:
        return self._endpoints[(u, v)] == endpoint

    def set_endpoint(self, u: str, v: str, endpoint: int) -> None:
        self._endpoints[(u, v)] = endpoint

    def unset_endpoint(self, u: str, v: str) -> None:
        del self._endpoints[(u, v)]
    
    def has_undirected_edge(self, u: str, v: str) -> bool:
        return self.has_edge(u, v) \
            and not self.has_endpoint(u, v, Endpoints.HEAD) \
            and not self.has_endpoint(v, u, Endpoints.HEAD)
    
    def has_directed_edge(self, u: str, v: str) -> bool:
        return self.has_edge(u, v) \
            and self.has_endpoint(u, v, Endpoints.HEAD) \
            and not self.has_endpoint(v, u, Endpoints.HEAD)
