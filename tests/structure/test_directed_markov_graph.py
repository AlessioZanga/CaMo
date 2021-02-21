import camo
import pytest


FIGURE_2_1 = camo.data.primer.figure_2_1
FIGURE_2_2 = camo.data.primer.figure_2_2
FIGURE_2_3 = camo.data.primer.figure_2_3
FIGURE_2_7 = camo.data.primer.figure_2_7
FIGURE_2_8 = camo.data.primer.figure_2_8

IS_CHAIN = [(FIGURE_2_1, "X", "Y", "Z", True)]
IS_FORK = [(FIGURE_2_2, "X", "Y", "Z", True)]
IS_COLLIDER = [(FIGURE_2_3, "X", "Y", "Z", True)]

IS_D_SEPARATED = [
    (FIGURE_2_7, "Y", "Z", None, True),
    (FIGURE_2_7, "Y", "Z", "W", False),
    (FIGURE_2_7, "Y", "Z", "U", False),
    (FIGURE_2_7, "Y", "Z", {"W", "X"}, True),
    (FIGURE_2_8, "Y", "Z", "W", False),
    (FIGURE_2_8, "Y", "Z", "U", False),
    (FIGURE_2_8, "Y", "Z", {"W", "U"}, False),
    (FIGURE_2_8, "Y", "Z", {"W", "T"}, False),
    (FIGURE_2_8, "Y", "Z", {"U", "T"}, False),
    (FIGURE_2_8, "Y", "Z", {"W", "U", "T"}, False),
    (FIGURE_2_8, "Y", "Z", {"W", "X"}, False),
    (FIGURE_2_8, "Y", "Z", {"U", "X"}, False),
    (FIGURE_2_8, "Y", "Z", {"W", "U", "X"}, False),
    (FIGURE_2_8, "Y", "Z", "T", True),
    (FIGURE_2_8, "Y", "Z", {"X", "T"}, True),
    (FIGURE_2_8, "Y", "Z", {"W", "X", "T"}, True),
    (FIGURE_2_8, "Y", "Z", {"U", "X", "T"}, True),
    (FIGURE_2_8, "Y", "Z", {"W", "U", "X", "T"}, True),
]


class TestDirectedMarkovGraph:

    @pytest.mark.parametrize("M, X, Y, Z, T", IS_CHAIN)
    def test_is_chain(self, M, X, Y, Z, T):
        assert M.is_chain(X, Y, Z) == T

    @pytest.mark.parametrize("M, X, Y, Z, T", IS_FORK)
    def test_is_fork(self, M, X, Y, Z, T):
        assert M.is_fork(X, Y, Z) == T

    @pytest.mark.parametrize("M, X, Y, Z, T", IS_COLLIDER)
    def test_is_collider(self, M, X, Y, Z, T):
        assert M.is_collider(X, Y, Z) == T

    @pytest.mark.parametrize("M, X, Y, Z, T", IS_D_SEPARATED)
    def test_is_dseparated(self, M, X, Y, Z, T):
        assert M.is_d_separated(X, Y, Z) == T
