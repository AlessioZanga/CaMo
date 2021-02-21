import camo
import pytest


FIGURE_3_10_A = camo.data.primer.figure_3_10_a
FIGURE_3_10_B = camo.data.primer.figure_3_10_b

IS_FRONTDOOR = [
    (FIGURE_3_10_A, "Smoking", "LungCancer", None, False),
    (FIGURE_3_10_B, "Smoking", "LungCancer", None, False),
    (FIGURE_3_10_B, "Smoking", "LungCancer", "TarDeposits", True),
]


class TestFrontdoorCriterion:

    @pytest.mark.parametrize("M, X, Y, Z, T", IS_FRONTDOOR)
    def test_is_frontdoor_adjustment_set(self, M, X, Y, Z, T):
        assert camo.is_frontdoor_adjustment_set(M, X, Y, Z) == T
