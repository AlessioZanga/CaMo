import camo
import pandas as pd
import pytest


M = camo.LinearGaussianSCM(
    V=["A", "B", "C", "D"],
    Beta=[[0, 2, 0, 0], [0, 0, 0, 4], [0, 0, 0, 0], [0, 0, 0, 0]]
)

N = camo.LinearGaussianSCM.from_structure(
    V=["A", "B", "C", "D", "E"],
    E=[("A", "B"), ("B", "C"), ("B", "D"), ("C", "E"), ("D", "E")]
)


FIT = []
for method in ["t_student", "z_fisher"]:
    FIT.append((M.sample(1000, seed=31), method, {("A", "B"), ("B", "D")}))
    FIT.append((N.sample(1000, seed=31), method, {("A", "B"), ("B", "C"), ("B", "D"), ("C", "E"), ("D", "E")}))

FIT_TRANSFORM = []
for method in ["t_student", "z_fisher"]:
    FIT_TRANSFORM.append((M.sample(1000, seed=31), method, None, [("A", "B")], [("A", "B"), ("B", "D")]))


class TestPC:

    @pytest.mark.parametrize("data, method, T", FIT)
    def test_fit(self, data, method, T):
        G = camo.PC(method=method).fit(data)
        assert len(G.E) == len(T) and all(G.has_edge(*e) for e in T)

    @pytest.mark.parametrize("data, method, blacklist, whitelist, T", FIT_TRANSFORM)
    def test_fit_transform(self, data, method, blacklist, whitelist, T):
        G = camo.PC(method=method).fit_transform(data, blacklist, whitelist)
        for t in T:
            assert G.is_tail_head(*t)
