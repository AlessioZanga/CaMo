from typing import Any, Dict, Iterable, Tuple

import pandas as pd
from sympy import solve, stats
from sympy.parsing.sympy_parser import parse_expr

from ..backend import DirectedGraph, topological_sort
from .causal_model import CausalModel


class StructuralCausalModel(CausalModel):

    _F: Dict[str, Any]
    _P: Dict[str, Any]

    def __init__(
        self,
        V: Iterable[str] = None,
        U: Iterable[str] = None,
        F: Dict[str, Any] = None,
        P: Dict[str, Any] = None,
    ):
        self._V = set(V) if V else set()
        self._U = set(U) if U else set()

        self._F = dict(F) if F else {v: None for v in self._V}
        self._P = dict(P) if P else {u: None for u in self._U}

        E = [
            (u.name, v)
            for (v, f) in self._parse_expr(
                dict(self._P, **self._F)
            ).items()
            if v in self._V
            for u in f.rhs.atoms()
            if u.is_Symbol
        ]

        super().__init__(self._V, self._U, E)

    def copy(self):
        return StructuralCausalModel(
            self._V, self._U, self._F, self._P
        )

    def _parse_expr(self, expr: Dict[str, str]) -> Dict[str, Any]:
        out = {}
        symbols = {}
        global_symbols = {}
        # Load global symbols adding stats
        exec('from sympy import *; from sympy.stats import *', global_symbols)
        # Begin parsing
        for (k, v) in expr.items():
            # Parse argument
            out[k] = parse_expr(
                v,
                symbols,
                global_dict=global_symbols,
                evaluate=False
            )
            # Add discovered symbols
            for atom in out[k].atoms():
                if atom.is_Symbol:
                    symbols[atom.name] = atom
        return out

    def do(self, **kwargs):
        # Check if v is endogenous
        if not (kwargs.keys() & self._V):
            raise ValueError()
        # Copy model
        intervened = self.copy()
        # Set intervened variables
        for (v, k) in kwargs.items():
            # Fix v variable to constant k
            intervened._F[v] = f"Eq(Symbol('{v}'), {k})"
            # Remove incoming edges
            for u in intervened.parents(v):
                intervened.del_edge(u, v)
        return intervened

    def sample(self, size: int) -> pd.DataFrame:
        # Parse the symbolic expression of the system
        system = self._parse_expr(dict(self._P, **self._F))
        # Pre-compute solving order
        order = [v for v in topological_sort(self) if v in self._V]
        # Pre-sample from exogenous distribution
        P = {u: stats.sample_iter(system[u]) for u in self._U}
        # Sample from equation system
        samples = []
        for _ in range(size):
            sample = {u: next(s) for u, s in P.items()}
            for v in order:
                sample[v] = float(solve(system[v].subs(sample), v)[0])
            samples.append(sample)
        return pd.DataFrame(samples)

    @classmethod
    def from_structure(
        cls,
        V: Iterable[str],
        E: Iterable[Tuple[str, str]],
    ):
        V, U = set(V), set()

        # Check if both vertices are in a vertex set
        # else, add to exogenous variables
        for (u, v) in E:
            if u not in V:
                U.add(u)
            if v not in V:
                U.add(v)

        # Build the functional graph
        G = DirectedGraph(V | U, E)

        # Build the function set given the graph
        F = {
            v: f"""Eq(Symbol('{v}'), Function(Symbol('f_{v}'))({
                ', '.join([f"Symbol('{p}')" for p in G.parents(v)])
            }))"""
            for v in topological_sort(G)
            if v in V
        }

        # Build the probability set given the variables
        P = {u: f"Uniform(Symbol('{u}'), 0, 1)" for u in U}

        return cls(V, U, F, P)

    def __repr__(self):
        return f"{self.__class__.__name__}(V={self._V}, U={self._U}, F={self._F}, P={self._P})"
