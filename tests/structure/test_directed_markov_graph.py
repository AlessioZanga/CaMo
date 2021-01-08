from camo.data import primer


def test_is_chain():
    model = primer.figure_2_1
    assert model.is_chain("X", "Y", "Z")

def test_is_fork():
    model = primer.figure_2_2
    assert model.is_fork("X", "Y", "Z")

def test_is_collider():
    model = primer.figure_2_3
    assert model.is_collider("X", "Y", "Z")

def test_d_separation():
    model = primer.figure_2_7

    assert model.is_d_separated("Y", "Z")
    assert not model.is_d_separated("Y", "Z", "W")
    assert not model.is_d_separated("Y", "Z", "U")
    assert model.is_d_separated("Y", "Z", {"W", "X"})

    model = primer.figure_2_8

    dependent_sets = [
        "W",
        "U",
        {"W", "U"},
        {"W", "T"},
        {"U", "T"},
        {"W", "U", "T"},
        {"W", "X"},
        {"U", "X"}, 
        {"W", "U", "X"}
    ]

    assert all([
        not model.is_d_separated("Y", "Z", S)
        for S in dependent_sets
    ])

    independent_sets = [
        "T",
        {"X", "T"},
        {"W", "X", "T"},
        {"U", "X", "T"},
        {"W", "U", "X", "T"}
    ]

    assert all([
        model.is_d_separated("Y", "Z", S)
        for S in independent_sets
    ])
