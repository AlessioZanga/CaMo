import camo
import pytest


FIGURE_3_6 = camo.data.primer.figure_3_6
FIGURE_3_7 = camo.data.primer.figure_3_7
FIGURE_3_10_A = camo.data.primer.figure_3_10_a
FIGURE_3_10_B = camo.data.primer.figure_3_10_b

IS_BACKDOOR = [
    (FIGURE_3_6, "X", "Y", None, False),
    (FIGURE_3_6, "X", "Y", "W", True),
    (FIGURE_3_7, "X", "Y", None, False),
    (FIGURE_3_7, "X", "Y", {"A", "Z"}, True),
    (FIGURE_3_7, "X", "Y", {"E", "Z"}, True),
    (FIGURE_3_7, "X", "Y", {"A", "E", "Z"}, True),
    (FIGURE_3_10_A, "Smoking", "LungCancer", None, False),
    (FIGURE_3_10_B, "Smoking", "LungCancer", None, False),
]

ALL_BACKDOOR = [
    (FIGURE_3_6, "X", "Y", [{"W"}]),
    (FIGURE_3_10_A, "Smoking", "LungCancer", []),
    (FIGURE_3_10_B, "Smoking", "LungCancer", []),
]


class TestBackdoorCriterion:

    @pytest.mark.parametrize("M, X, Y, Z, T", IS_BACKDOOR)
    def test_is_backdoor_adjustment_set(self, M, X, Y, Z, T):
        assert camo.is_backdoor_adjustment_set(M, X, Y, Z) == T

    @pytest.mark.parametrize("M, X, Y, T", ALL_BACKDOOR)
    def test_all_backdoor_adjustment_sets(self, M, X, Y, T):
        assert camo.all_backdoor_adjustment_sets(M, X, Y) == T
