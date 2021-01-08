from camo.data import primer
from camo import is_backdoor_adjustment_set, all_backdoor_adjustment_sets


def test_backdoor_criterion_figure_3_6():
    model = primer.figure_3_6
    assert not is_backdoor_adjustment_set(model, "X", "Y", [])
    assert is_backdoor_adjustment_set(model, "X", "Y", {"W"})
    assert all_backdoor_adjustment_sets(model, "X", "Y") == [{"W"}]

def test_backdoor_criterion_figure_3_7():
    model = primer.figure_3_7
    assert not is_backdoor_adjustment_set(model, "X", "Y", [])

    adjustment_sets = [
        {"E", "Z"},
        {"A", "Z"},
        {"E", "Z", "A"}
    ]
    assert all(
        is_backdoor_adjustment_set(model, "X", "Y", S)
        for S in adjustment_sets
    )

def test_backdoor_criterion_figure_3_10_a_b():
    for model in [primer.figure_3_10_a, primer.figure_3_10_b]:
        assert not is_backdoor_adjustment_set(model, "Smoking", "LungCancer")
        assert all_backdoor_adjustment_sets(model, "Smoking", "LungCancer") == []
