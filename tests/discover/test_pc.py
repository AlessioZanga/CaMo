import numpy as np
import pandas as pd

import camo


samples = 1000
np.random.seed(31)
x0 = np.random.normal(size=samples)
x1 = 2.0 * x0
x2 = np.random.normal(size=samples)
x3 = 4.0 * x1
data = np.array([x0, x1, x2, x3])
data = pd.DataFrame(data.T, columns=["x0", "x1", "x2", "x3"])


def test_pc():
    G = camo.discover.PC().fit_transform(data)

    E = G.edges
    assert ("x0", "x1") in E or ("x1", "x0") in E
    assert ("x0", "x3") in E or ("x3", "x0") in E
    assert ("x1", "x3") in E or ("x3", "x1") in E
