import numpy as np
from scipy.stats import norm, chi2

from .._constants import group_id_column
from ..multivariate._interpretation import hypotheses_multinormal_test
from ..core import ObservationSet


def mardia_test(observations, alpha=0.05, group='control'):

    if not isinstance(observations, ObservationSet):
        raise ValueError('observations should be an instance of class ObservationSet')

    matrix = observations.data.loc[observations.data[group_id_column] == group, observations.value_columns].values.T

    k, n = matrix.shape

    covariance = np.cov(matrix)
    inverse_covariance = np.linalg.inv(covariance)
    mean = np.atleast_2d(matrix.mean(axis=1)).T

    all_products = (matrix - mean).T.dot(inverse_covariance.dot(matrix - mean))

    a = (all_products ** 3).sum() / (6 * n)

    b = np.sqrt(n / (8 * k * (k + 2))) * (np.sum(np.diag(all_products) ** 2) / n - k * (k + 2))

    dof = k * (k + 1) * (k + 2) / 6

    a_pvalue = 1 - chi2.cdf(a, dof)

    b_pvalue = 2 * norm.cdf(-abs(b))  # * 2 for two-tailed

    fisher_statistics = -2 * (np.log(a_pvalue) + np.log(b_pvalue))
    p_value = 1 - chi2.cdf(fisher_statistics, 4)  # not sure it is the right method

    hypotheses = hypotheses_multinormal_test(group)
    reject = p_value < alpha
    return {
        'test': 'Mardia\'s multinormality test',
        'reject': reject,
        'winning_hypothesis': 'H1' if reject else 'H0',
        'skewness_statistics': a,
        'kurtosis_statistics': b,
        'skewness_pvalue': a_pvalue,
        'kurtosis_pvalue': b_pvalue,
        'p_value': p_value,
        **hypotheses
    }
