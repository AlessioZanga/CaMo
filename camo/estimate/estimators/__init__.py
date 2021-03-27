from .abstract_estimator import AbstractEstimator
from .g_formula import GFormula
from .propensity_score import PropensityScore
from .inverse_probability_weighting import InverseProbabilityWeighting as IPW
from .augmented_inverse_probability_weighting import AugmentedInverseProbabilityWeighting as AIPW
from .targeted_maximum_likelihood_estimator import TargetedMaximumLikelihoodEstimator as TMLE

ESTIMATORS = {
    "g_formula": GFormula,
    "ipw": IPW,
    "aipw": AIPW,
    "tmle": TMLE,
}
