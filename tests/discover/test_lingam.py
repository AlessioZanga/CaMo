import numpy as np
import pandas as pd

import camo


samples = 1000
np.random.seed(31)
x0 = np.random.uniform(size=samples)
x1 = 2.0 * x0 + np.random.uniform(size=samples)
x2 = np.random.uniform(size=samples)
x3 = 4.0 * x1 + np.random.uniform(size=samples)
data = np.array([x0, x1, x2, x3])
data = pd.DataFrame(data.T, columns=["x0", "x1", "x2", "x3"])


def test_ica_lingam():
    B = camo.discover.ICALiNGAM().fit_transform(data)

    assert B[1, 0] > 1.9
    assert B[3, 1] > 3.9


def test_direct_lingam():
    B = camo.discover.DirectLiNGAM().fit_transform(data)

    assert B[1, 0] > 1.9
    assert B[3, 1] > 3.9
