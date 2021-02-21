import camo
import numpy as np
import statsmodels.formula.api as smf
import pytest


M = camo.SCM(
    V=["Z"],
    F={"Z": "Eq(Z, 2*X+Y)"},
    P={"X": "Uniform(X,0,1)", "Y": "Uniform(Y,0,1)"}
)

SAMPLE = [(M, "Z ~ X + Y", [0, 2, 1])]

DO_SAMPLE = [(M, {"Z": 3}, "Z ~ X + Y", [3, 0, 0])]


class TestSCM:

    @pytest.mark.parametrize("M, F, T", SAMPLE)
    def test_sample(self, M, F, T):
        ols = smf.ols(F, M.sample(100, seed=31)).fit()
        np.testing.assert_allclose(ols.params, T, atol=1e-8)
    
    @pytest.mark.parametrize("M, X, F, T", DO_SAMPLE)
    def test_do_sample(self, M, X, F, T):
        ols = smf.ols(F, M.do(**X).sample(100, seed=31)).fit()
        np.testing.assert_allclose(ols.params, T, atol=1e-8)
