from typing import Any, Set

import numpy as np
import pandas as pd

from .propensity_score import PropensityScore


class InverseProbabilityWeighting(PropensityScore):

    def predict(self, data: pd.DataFrame, X: str, Y: str, Z: Set[str]) -> Any:
        # Compute the propensity score
        eZ = super().predict(data, X, Y, Z)
        # Estimate E[Y|do(X=1),Z] and E[Y|do(X=0),Z]
        mask = data[X]
        Y1 = mask * data[Y] / eZ
        Y0 = (1 - mask) * data[Y] / (1 - eZ)
        return Y1, Y0
