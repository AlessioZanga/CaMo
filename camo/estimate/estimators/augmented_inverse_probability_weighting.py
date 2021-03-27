from typing import Any, Set

import numpy as np
import pandas as pd

from .propensity_score import PropensityScore
from ...utils import _as_set


class AugmentedInverseProbabilityWeighting(PropensityScore):

    def predict(self, data: pd.DataFrame, X: str, Y: str, Z: Set[str]) -> Any:
        Z = _as_set(Z)
        # Compute the propensity score
        eZ = super().predict(data, X, Y, Z)
        #
        f = f"{Y} ~ {X}"
        f = f if not Z else f + " + " + " + ".join(Z)
        self._estimator = self._model(f, data).fit()
        #
        Y1 = self._estimator.predict(data.assign(**{X: 1}))
        Y0 = self._estimator.predict(data.assign(**{X: 0}))
        #
        Y1 = data[X] * (data[Y] - Y1) / eZ + Y1
        Y0 = data[X] * (data[Y] - Y0) / eZ + Y0
        return Y1, Y0
