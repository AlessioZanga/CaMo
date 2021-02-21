import camo
import numpy as np
import pytest


class TestAverageCausalEffect:

    @pytest.mark.parametrize("data, X, Y, Z, T", [
        (camo.data.cd4, "T", "CD4", ["Insurance", "ViralLoad", "Income", "Education"], 0.4968077996596586)
    ])
    def test_g_formula(self, data, X, Y, Z, T):
        ace = camo.ACE(data, X, Y, Z, method="g_formula", estimator="ols")
        np.testing.assert_allclose(ace, T)
    
    @pytest.mark.parametrize("data, X, Y, Z, T", [
        (camo.data.cd4, "T", "CD4", ["Insurance", "ViralLoad", "Income", "Education"], 0.4917151858666866)
    ])
    def test_ipw(self, data, X, Y, Z, T):
        ace = camo.ACE(data, X, Y, Z, method="ipw", estimator="logit")
        np.testing.assert_allclose(ace, T)
