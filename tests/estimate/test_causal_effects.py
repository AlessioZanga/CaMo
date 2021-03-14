import camo
import numpy as np
import pytest

TEST_G_FORMULA = [
    (
        camo.data.cd4,
        "T",
        "CD4",
        ["Insurance", "ViralLoad", "Income", "Education"],
        0.4968077996596586
    ),
]

TEST_IPW = [
    (
        camo.data.cd4,
        "T",
        "CD4",
        ["Insurance", "ViralLoad", "Income", "Education"],
        0.4917151858666866
    ),
]


class TestAverageCausalEffect:

    @pytest.mark.parametrize("data, X, Y, Z, T", TEST_G_FORMULA)
    def test_g_formula(self, data, X, Y, Z, T):
        ace = camo.ACE("g_formula").fit_predict(data, X, Y, Z)
        np.testing.assert_allclose(ace, T)
    
    @pytest.mark.parametrize("data, X, Y, Z, T", TEST_IPW)
    def test_ipw(self, data, X, Y, Z, T):
        ace = camo.ACE("ipw").fit_predict(data, X, Y, Z)
        np.testing.assert_allclose(ace, T)
