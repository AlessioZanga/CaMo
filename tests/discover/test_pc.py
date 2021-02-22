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

O = pd.DataFrame({
    "ABILITY": [1.0, .62, .25, .16, -.10, .29, .18],
    "GPQ": [0, 1.0, .09, .28, .00, .25, .15],
    "PREPROD": [0, 0, 1.0, .07, .03, .34, .19],
    "QFJ": [0, 0, 0, 1.0, .10, .37, .41],
    "SEX": [0, 0, 0, 0, 1.0, .13, .43],
    "CITES": [0, 0, 0, 0, 0, 1.0, .55],
    "PUBS": [0, 0, 0, 0, 0, 0, 1.0]
})
O = camo.LinearGaussianSCM(V=O.columns, Beta=O.values)


FIT = []
for method in ["t_student", "z_fisher"]:
    FIT.append((M.sample(1000, seed=31), method, {("A", "B"), ("A", "D"), ("B", "D")}))
    FIT.append((N.sample(1000, seed=31), method, {("A", "B"), ("B", "C"), ("B", "D"), ("C", "E"), ("D", "E")}))

FIT_TRANSFORM = []
for method in ["t_student", "z_fisher"]:
    FIT_TRANSFORM.append((M.sample(100, seed=31), method, None, [("A", "B")], [("A", "B"), ("B", "D")]))


class TestPC:

    @pytest.mark.parametrize("data, method, T", FIT)
    def test_fit(self, data, method, T):
        G = camo.PC(method=method).fit(data)
        assert len(G.E) == len(T) and all(G.has_edge(*e) for e in T)

    @pytest.mark.parametrize("data, method, blacklist, whitelist, T", FIT_TRANSFORM)
    def test_fit_transform(self, data, method, blacklist, whitelist, T):
        G = camo.PC(method=method).fit_transform(data, blacklist, whitelist)
        for t in T:
            assert G.has_directed_edge(*t)
