import camo
import pytest


M = camo.LinearGaussianSCM(
    V=["A", "B", "C", "D"],
    Beta=[[0, 2, 0, 0], [0, 0, 0, 4], [0, 0, 0, 0], [0, 0, 0, 0]]
)

FIT = [
    (M.sample(100, seed=31), method, {("A", "B"), ("B", "D")})
    for method in ["t_student", "z_fisher"]
]
FIT_TRANSFORM =  [
    (M.sample(100, seed=31), method, None, [("A", "B")], [("A", "B"), ("B", "D")])
    for method in ["t_student", "z_fisher"]
]


class TestPC:

    @pytest.mark.parametrize("data, method, T", FIT)
    def test_fit(self, data, method, T):
        G = camo.PC(method=method).fit(data)
        assert len(G.E) == len(T) and all(G.has_edge(*e) for e in T)

    @pytest.mark.parametrize("data, method, blacklist, whitelist, T", FIT_TRANSFORM)
    def test_fit_transform(self, data, method, blacklist, whitelist, T):
        G = camo.PC(method=method).fit_transform(data, blacklist, whitelist)
        assert all(G.has_directed_edge(*t) for t in T)
