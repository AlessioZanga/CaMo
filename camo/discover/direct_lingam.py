import numpy as np
import pandas as pd
from sklearn.preprocessing import scale

from .ica_lingam import ICALiNGAM


class DirectLiNGAM(ICALiNGAM):

    def fit(self, data: pd.DataFrame):
        # Given a d-dimensional random vector x, a set of its variable indices U and
        # a d x n data matrix of the random vector as X, initialize an ordered list
        # of variables K = [].
        d = len(data.columns)
        X, U, K = scale(data), np.arange(d), np.zeros(d, int)
        # The residual data matrix.
        def R(x, y): return x - np.cov(x, y)[0, 1] / np.var(y) * y
        R = np.vectorize(R, signature="(n),(n)->(m)")
        # TODO: Implement Kernel Generalized Variance as Mutual Information approximation.
        def MI(x, y): return 1 - np.cov(1/(1 + np.exp(-x)), y)[0, 1]
        MI = np.vectorize(MI, signature="(n),(n)->()")
        # Repeat until d-1 variable indices are appended to K:
        for i in range(d-1):
            # Perform least-squares regressions of xi on xj for all i in U\K (i!=j)
            # and compute the residual vectors r(j) and the residual data matrix
            # R(j) from the data matrix X, for all j in U\K. Find a variable xm
            # that is the most independent of its residuals.
            # MI(data.iloc[:, j], R[i, j])
            r = R(X.T, X.T[:, None])
            m = MI(X.T, r)
            np.fill_diagonal(m, 0)
            m = np.argmin(np.sum(m, 1))
            # Append m to the end of K.
            K[i] = U[m]
            U = np.delete(U, m)
            # Let x = r(m), X = R(m).
            X = np.delete(r, m, axis=0)[:, m].T
        # Add remaining index.
        K[d-1] = U[0]

        return K

    def fit_transform(self, data: pd.DataFrame):
        return self.transform(data, self.fit(data))
