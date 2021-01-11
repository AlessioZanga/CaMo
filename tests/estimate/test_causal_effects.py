import camo
import numpy as np


def test_average_causal_effect():
    data = camo.data.generated.estimate
    ace = camo.ACE(data, "T", "CD4", ["Insurance", "ViralLoad", "Income", "Education"])
    assert np.allclose(ace, 0.4968077996596586)
