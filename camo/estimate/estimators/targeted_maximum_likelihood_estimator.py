from typing import Any, Set

import numpy as np
import pandas as pd

import statsmodels.formula.api as smf

from scipy.special import expit, logit  # pylint: disable=no-name-in-module

from .g_formula import GFormula
from .propensity_score import PropensityScore


class TargetedMaximumLikelihoodEstimator(GFormula):

    def predict(self, data: pd.DataFrame, X: str, Y: str, Z: Set[str]) -> Any:
        # Compute adjustment formula
        Y1, Y0 = super().predict(data, X, Y, Z)
        YX = self._estimator.predict(data)
        # Compute propensity score
        eZ = PropensityScore().fit_predict(data, X, Y, Z)
        H1, H0, mask = 1/eZ, -1/(1-eZ), data[X]
        HX = mask * H1 + (1 - mask) * H0
        # Compute delta coefficient using regression
        data = data.assign(**{X: HX})
        # logit(D[*,Y]) := logit(YX) + delta * HX
        delta = self._model(f"{Y} ~ {X}", data, offset=YX)
        delta = delta.fit().params[X]
        # Compute targeted estimates
        Y1 = expit(logit(Y1) + delta * H1)
        Y0 = expit(logit(Y0) + delta * H0)
        return Y1, Y0
