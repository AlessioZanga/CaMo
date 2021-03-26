from .conditional_independence_test import *
from .directed_graph import *
from .directed_markov_graph import *
from .graph import *
from .partial_ancestral_graph import *
from .partial_correlation import *
from .ts_partial_ancetral_graph import tsPartialAncestralGraph

PAG = PartialAncestralGraph
tsPAG = tsPartialAncestralGraph

CONDITIONAL_INDEPENDENCE_TESTS = {
    "chi_squared": ChiSquared,
    "fisher_z": FisherZ,
    "student_t": StudentT,
    "fast_fisher_z": FastFisherZ,
    "fast_student_t": FastStudentT,
}
