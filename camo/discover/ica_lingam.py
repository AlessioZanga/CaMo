from itertools import permutations
from typing import Optional

import numpy as np
import pandas as pd
from scipy.optimize import linear_sum_assignment as hungarian
from sklearn.decomposition import FastICA
from sklearn.linear_model import LassoLarsIC, LinearRegression

from ..structure import LinearNonGaussianSCM


class ICALiNGAM:

    # Define Adaptive Lasso regression.
    def _apply_adaptive_lasso(self, data, target, regressors, gamma=1.0):
        target, regressors = data.iloc[:, target], data.iloc[:, regressors]
        w = LinearRegression().fit(regressors, target).coef_
        w = LassoLarsIC(criterion="bic").fit(
            regressors * np.power(np.abs(w), gamma),
            target
        ).coef_ * w
        return w

    def fit(self, data: pd.DataFrame, seed: Optional[int] = None):
        # Given a d-dimensional random vector x and its (d,n) observed data matrix X,
        # apply an ICA algorithm to obtain an estimate of A.
        d = len(data.columns)
        B = FastICA(random_state=seed).fit(data).components_
        # Find the unique permutation of the rows of W = A^-1 that yields a matrix W'
        # without any zeros on the main diagonal. The permutation is sought by minimizing
        # sum_i (1/|W'_ii|). This minimization problem is the classical linear assignment
        # problem, and here the Hungarian algorithm (Kuhn, 1955) is used.
        _, K = hungarian(1 / np.abs(B))
        B = B.take(K, 0)
        # Divide each row of W' by its corresponding diagonal element in order to
        # yield a new matrix W'' with a diagonal consisting entirely of 1s.
        B /= B.diagonal()[..., None]
        # Compute an estimate B' of B by using B' = I - W''.
        B = np.identity(d) - B
        # Finally, to estimate a causal order k(i), determine the permutation matrix
        # K of B', obtaining the matrix B' = PB'K^T that is as close as possible
        # to having a strictly lower triangular structure.
        K = None
        if d < 8:
            # For a small number of variables, i.e., fewer than 8, the lower triangularity
            # of B' can be measured by using the sum of squared bij in its upper triangular
            # section sum_i<=j (b'_ij^2). In addition, an exhaustive search over all possible
            # permutations is feasible and is hence performed.
            vmin = np.inf
            for p in permutations(range(d)):
                score = np.sum(np.square(np.triu(B.take(p, 0))))
                if score < vmin:
                    vmin = score
                    K = p
            K = np.array(K)
        else:
            # For higher-dimensional data, the following approximate algorithm is used,
            # which sets small absolute valued elements in B' to zero, and whereby it can be
            # determined whether it is possible to permute the resulting matrix to become
            # strictly lower triangular:
            # (a) Set the d(d+1)/2 smallest (in absolute value) elements of B' to zero.
            i = round(d*(d+1)/2)
            pmin = np.argsort(np.abs(np.ravel(B)))
            B.flat[pmin[:i]] = 0
            # (b) Repeat
            while K is None:
                # i. Determine whether B' can be permuted to become strictly lower triangular.
                # If this is possible, stop and return the permuted B'.
                K, A, L = np.zeros(d, int), np.arange(d), B
                while len(A) > 0:
                    # Find a row where all elements are zero, if any.
                    j = np.where(np.sum(np.abs(L), axis=1) == 0)
                    # If there is no row with zero elements, exit.
                    if len(j[0]) == 0:
                        K = None
                        break
                    # Select the first row with zero elements.
                    j = j[0][0]
                    # Add original index to permutation matrix.
                    K[d-len(A)] = A[j]
                    A = np.delete(A, j)
                    # Remove selected row and columns.
                    mask = np.delete(np.arange(len(L)), j)
                    L = L[mask][:, mask]
                # ii. In addition, set the next smallest (in absolute value) element of Bb to zero.
                if K is None:
                    B.flat[pmin[i]] = 0
                    i += 1

        return K

    def fit_transform(self, data: pd.DataFrame, seed: Optional[int] = None):
        return self.transform(data, self.fit(data, seed))

    def transform(self, data: pd.DataFrame, K):
        # Estimate B applying Adaptive Lasso over the causal order K incrementally.
        d = len(K)
        B = np.zeros((d, d))
        for i in range(1, d):
            B[K[i], K[:i]] = self._apply_adaptive_lasso(data, K[i], K[:i])

        # Workaround to remove subnormal numbers.
        EPS = np.finfo(float).eps
        B[B < EPS] = 0

        return LinearNonGaussianSCM(data.columns, B)
