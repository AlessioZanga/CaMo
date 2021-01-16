import camo

adult = camo.data.adult


def test_conditional_independence():

    args = [
        (("Age", "Immigrant"), False),
        (("Age", "Race"), False),
        (("Age", "Sex"), False),
        (("Education", "HoursPerWeek", ["Age", "Immigrant", "Race", "Sex"]), False),
        (("Immigrant", "Sex"), True),
        (("Education", "MaritalStatus", ["Age", "Sex"]), False)
    ]

    for ci in [
        getattr(camo.backend, k)
        for k in camo.backend.CONDITIONAL_INDEPENDENCE_TESTS.keys()
    ]:
        for arg in args:
            _, p_value, _ = ci(adult, *arg[0])
            assert (p_value > 0.05) == arg[1]
