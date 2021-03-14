from .abstract_estimator import AbstractEstimator
from .g_formula import GFormula
from .propensity_score import PropensityScore
from .inverse_probability_weighting import InverseProbabilityWeighting

AdjustmentFormula = GFormula
IPW = InverseProbabilityWeighting

ESTIMATORS = {
    "g_formula": GFormula,
    "ipw": InverseProbabilityWeighting,
}
