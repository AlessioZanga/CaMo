import camo
import numpy as np


data = camo.data.generated.estimate
args = ("T", "CD4", ["Insurance", "ViralLoad", "Income", "Education"])


def test_average_causal_effect_g_formula():
    ace = camo.ACE(data, *args, method="g_formula", estimator="ols")
    assert np.allclose(ace, 0.4968077996596586)


def test_average_causal_effect_inverse_probability_weighting():
    ace = camo.ACE(data, *args, method="ipw", estimator="logit")
    assert np.allclose(ace, 0.4917151858666866)
