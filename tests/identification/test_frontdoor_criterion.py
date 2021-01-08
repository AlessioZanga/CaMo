from camo.data import primer
from camo import is_frontdoor_adjustment_set


def test_frontdoor_criterion_figure_3_10_a_b():
    model = primer.figure_3_10_a
    assert not is_frontdoor_adjustment_set(model, "Smoking", "LungCancer")

    model = primer.figure_3_10_b
    assert not is_frontdoor_adjustment_set(model, "Smoking", "LungCancer")
    assert is_frontdoor_adjustment_set(model, "Smoking", "LungCancer", "TarDeposits")
