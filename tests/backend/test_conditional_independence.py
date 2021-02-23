import camo
import pytest


ADULT = [
    (camo.data.adult, "Age", "Immigrant", None, False),
    (camo.data.adult, "Age", "Race", None, False),
    (camo.data.adult, "Age", "Sex", None, False),
    (camo.data.adult, "Education", "HoursPerWeek", ["Age", "Immigrant", "Race", "Sex"], False),
    (camo.data.adult, "Immigrant", "Sex", None, True),
    (camo.data.adult, "Education", "MaritalStatus", ["Age", "Sex"], False)
]


FIGURE_3_1 = camo.data.primer.figure_3_1
FIGURE_3_1 = [
    (FIGURE_3_1.sample(100, 31), X, Y, Z, FIGURE_3_1.is_d_separated(X, Y, Z))
    for Z in camo.utils._powerset(FIGURE_3_1.V)
    for X in FIGURE_3_1.V
    for Y in FIGURE_3_1.V
    if X != Y \
    and X not in Z \
    and Y not in Z
]


class TestConditionalIndependnece:

    @pytest.mark.parametrize("data, X, Y, Z, T", ADULT)
    def test_chi_square(self, data, X, Y, Z, T):
        _, p_value, _ = camo.backend.chi_squared(data, X, Y, Z)
        assert (p_value > 0.05) == T
    
    @pytest.mark.parametrize("data, X, Y, Z, T", FIGURE_3_1)
    def test_t_student(self, data, X, Y, Z, T):
        _, p_value, _ = camo.backend.t_student(data, X, Y, Z)
        assert (p_value > 0.05) == T
    
    @pytest.mark.parametrize("data, X, Y, Z, T", FIGURE_3_1)
    def test_z_fisher(self, data, X, Y, Z, T):
        _, p_value, _ = camo.backend.z_fisher(data, X, Y, Z)
        assert (p_value > 0.05) == T
