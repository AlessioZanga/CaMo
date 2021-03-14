from typing import Any, Set

import numpy as np
import pandas as pd

from .propensity_score import PropensityScore


class InverseProbabilityWeighting(PropensityScore):

    def predict(self, data: pd.DataFrame, X: str, Y: str, Z: Set[str] = None) -> Any:
        # Compute the propensity score
        e_Z = super().predict(data, X, Y, Z)
        # Estimate E[Y|do(X=1),Z] and E[Y|do(X=0),Z]
        mask = (data[X] == 1)
        Y1 = mask * data[Y] / e_Z
        Y0 = (1 - mask) * data[Y] / (1 - e_Z)
        return Y1, Y0
