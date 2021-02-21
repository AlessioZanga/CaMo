import camo
import pytest


M = camo.LinearGaussianSCM(
    V=["A", "B", "C", "D"],
    Beta=[[0, 2, 0, 0], [0, 0, 0, 4], [0, 0, 0, 0], [0, 0, 0, 0]]
)
M = [
    (M.sample(1000, seed=31), method, {("A", "B"), ("A", "D"), ("B", "D")})
    for method in ["t_student", "z_fisher"]
]


class TestPC:

    @pytest.mark.parametrize("data, method, T", M)
    def test_skeleton(self, data, method, T):
        G = camo.PC().fit(data, method)
        assert len(G.E) == len(T) and all(G.has_edge(*e) for e in T)
