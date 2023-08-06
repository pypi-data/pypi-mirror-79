import numpy as np
from scipy import stats

from ..core import ObservationSet
from .._constants import group_id_column
from ..multivariate._interpretation import hypotheses_mean_comparison


def t2_test(observations, alpha=0.05, control_group='control', treatment_group='treatment'):

    if not isinstance(observations, ObservationSet):
        raise ValueError('observations should be an instance of class ObservationSet')

    c_matrix = observations.data.loc[observations.data[group_id_column] == control_group,
                                     observations.value_columns].values.T
    t_matrix = observations.data.loc[observations.data[group_id_column] == treatment_group,
                                     observations.value_columns].values.T

    c_mean = np.atleast_2d(c_matrix.mean(axis=1)).T
    t_mean = np.atleast_2d(t_matrix.mean(axis=1)).T

    c_covariance = np.cov(c_matrix)
    t_covariance = np.cov(t_matrix)

    _, c_n = c_matrix.shape
    p, t_n = t_matrix.shape

    pooled_covariance = ((c_n - 1) * c_covariance + (t_n - 1) * t_covariance) / (c_n + t_n - 2)

    constant = c_n * t_n / (c_n + t_n) * (c_n + t_n - p - 1) / (c_n + t_n - 2) / p
    statistics = constant * (t_mean - c_mean).T.dot(np.linalg.solve(pooled_covariance, t_mean - c_mean))[0, 0]

    pvalue = stats.f.sf(statistics, p, c_n + t_n - p - 1)
    reject = pvalue < alpha
    hypotheses = hypotheses_mean_comparison(control_group, treatment_group)

    return {
        'test': 'Hotelling\'s T2-test',
        'reject': reject,
        'winning_hypothesis': 'H1' if reject else 'H0',
        'statistics': statistics,
        'pvalue': pvalue,
        **hypotheses
    }
