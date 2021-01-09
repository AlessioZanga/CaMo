import camo
import numpy as np
import statsmodels.formula.api as smf


def test_sample():
    model = camo.SCM(
        V=["Z"],
        F={"Z": "Eq(Z, 2*X+Y)"},
        P={"X": "Uniform(X,0,1)", "Y": "Uniform(Y,0,1)"}
    )
    ols = smf.ols("Z ~ X + Y", model.sample(100)).fit()
    assert np.allclose(ols.params, np.array([0, 2, 1]))


def test_do_sample():
    model = camo.SCM(
        V=["Z"],
        F={"Z": "Eq(Z, 2*X+Y)"},
        P={"X": "Uniform(X,0,1)", "Y": "Uniform(Y,0,1)"}
    )
    ols = smf.ols("Z ~ X + Y", model.do(Z=3).sample(100)).fit()
    assert np.allclose(ols.params, np.array([3, 0, 0]))
