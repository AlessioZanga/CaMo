from camo.data import primer
from camo import is_backdoor_adjustment_set, backdoor_all_adjustment_sets


def test_backdoor_criterion():
    model = primer.figure_3_6
    assert(not is_backdoor_adjustment_set(model, "X", "Y", []))
    assert(is_backdoor_adjustment_set(model, "X", "Y", {"W"}))
    assert(backdoor_all_adjustment_sets(model, "X", "Y") == [{"W"}])

    """ TODO: Check deeper before adding this example
    model = primer.figure_3_7
    assert(not is_backdoor_adjustment_set(model, "X", "Y", []))

    adjustment_sets = [
        {"E", "Z"},
        {"A", "Z"},
        {"E", "Z", "A"}
    ]
    assert(all(
        is_backdoor_adjustment_set(model, "X", "Y", S)
        for S in adjustment_sets
    ))
    """
