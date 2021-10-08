from copy import deepcopy
from ..backend import PAG, Endpoints
from .dag_from_cpdag import dag_from_cpdag


def mag_from_pag(G: PAG):
    """
        A Characterization of Markov Equivalence Classes for
        Directed Acyclic Graphs with Latent Variables
    """
    out = deepcopy(G)

    for X, Y in out.E:
        # Orient o-> as -->
        if out.is_circle_head(X, Y):
            out.set_endpoint(Y, X, Endpoints.TAIL)
        # Orient --o as -->
        elif out.is_tail_circle(X, Y):
            out.set_endpoint(X, Y, Endpoints.HEAD)
        # In the next step o-o are oriented as --> or <--
        # without adding any v-structure. Equivalently,
        # we could map o-o to ---, and apply Meek rules.
        elif out.is_circle_circle(X, Y):
            out.set_endpoint(X, Y, Endpoints.TAIL)
            out.set_endpoint(Y, X, Endpoints.TAIL)

    return dag_from_cpdag(out)
