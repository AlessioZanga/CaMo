from copy import deepcopy
from ..backend import PAG, Endpoints
from .pc import PC


def dag_from_cpdag(G: PAG):
    """
        Causal inference and causal explanation with background knowledge
    """
    out = deepcopy(G)
    # Orient remaining edges
    orient = PC()
    is_oriented = False
    while not is_oriented:
        is_oriented = True
        for X, Y in out.E:
            if out.is_tail_tail(X, Y):
                is_oriented = False
                # Orient X --- Y as X --> Y
                out.set_endpoint(X, Y, Endpoints.HEAD)
                # Apply Meek rules
                is_closed = False
                while not is_closed:
                    is_closed = True
                    is_closed &= orient._R1(out)
                    is_closed &= orient._R2(out)
                    is_closed &= orient._R3(out)
                    is_closed &= orient._R4(out)
                break
    return out
