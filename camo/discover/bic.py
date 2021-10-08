import numpy as np
import pandas as pd
from scipy.stats import norm
import statsmodels.formula.api as smf

from ..backend import PAG


class BIC:

    data: pd.DataFrame

    def __init__(self, data: pd.DataFrame):
        self.n = len(data)
        self.data = data.copy()

    def __call__(self, G: PAG) -> float:
        return sum(self.local_score(G, X) for X in G.V)

    def local_score(self, G: PAG, X: str) -> float:
        data = self.data[X]
        parents = [Y for Y in G.neighbors(X) if G.is_tail_head(Y, X)]

        k, mean, std = len(parents), 0, 0

        if k == 0:
            mean, std = np.repeat(data.mean(), self.n), data.std()
        else:
            # Quote special characters
            parents = [f"Q('{p}')" for p in parents]
            regression = smf.ols(f"Q('{X}') ~ {'+'.join(parents)}", self.data).fit()
            mean, std = regression.fittedvalues, regression.scale

        k += 2

        loglikelihood = np.vectorize(norm.pdf)(data, mean, std).sum()

        return - loglikelihood + 0.5 * k * np.log(self.n)
