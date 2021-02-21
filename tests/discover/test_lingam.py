import camo
import pandas as pd
import pytest


M = camo.LinearNonGaussianSCM(
    V=["A", "B", "C", "D"],
    Beta=[[0, 2, 0, 0], [0, 0, 0, 4], [0, 0, 0, 0], [0, 0, 0, 0]]
)
M = [(M.sample(1000, seed=31), M.Beta.T)]


class TestLiNGAM:

    @pytest.mark.parametrize("data, B", M)
    def test_ica_lingam(self, data, B):
        M = camo.ICALiNGAM().fit_transform(data, seed=13)
        pd.testing.assert_frame_equal(M.Beta, B, check_dtype=False, atol=1e-1)

    @pytest.mark.parametrize("data, B", M)
    def test_direct_lingam(self, data, B):
        M = camo.DirectLiNGAM().fit_transform(data)
        pd.testing.assert_frame_equal(M.Beta, B, check_dtype=False, atol=1e-1)
