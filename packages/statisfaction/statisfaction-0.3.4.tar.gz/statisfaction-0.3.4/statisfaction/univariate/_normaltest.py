import scipy.stats as stats

from ..univariate._interpretation import hypotheses_normal_test
from ..utils.input import get_value_column_from_univariate
from ..core import ObservationSet

"""
    normaltest.py
    ======================

    This module contains the logic to run normality tests (d'Agostino or Shapiro) over a univariate sample.
    As its name indicates, a normal test is used to assess if a sample of observations follows a normal distribution.

 """

def dagostino_test_from_observations(observations, alpha=0.05, group='control'):
    """
    Runs a d'Agostino test over an observation set.

    Returns a dict containing the test results.

    :param observations: The observation set over which the ttest is computed
    :param alpha: The maximum type I error tolerated reject the null hypothesis
    :param group: The group name
    :type observations: ObservationSet
    :type alpha: float
    :type group: string
    :return: The dict containing the test results
    :rtype: dict

    """
    if not isinstance(observations, ObservationSet):
        raise ValueError('observations should be an instance of class ObservationSet')
    value_column = get_value_column_from_univariate(observations)
    group_data = observations._get_series(group, value_column)
    statistics, pvalue = stats.normaltest(
        group_data,
        nan_policy='raise'
    )
    hypotheses = hypotheses_normal_test(group)
    reject = pvalue < alpha
    return {
        'test': 'D\'Agostino and Pearson\'s normality test',
        'reject': reject,
        'winning_hypothesis': 'H1' if reject else 'H0',
        'statistics': statistics,
        'pvalue': pvalue,
        **hypotheses
    }


def shapiro_test_from_observations(observations, alpha=0.05, group='control'):
    """
    Runs a Shapiro test over an observation set.

    Returns a dict containing the test results.

    :param observations: The observation set over which the ttest is computed
    :param alpha: The maximum type I error tolerated reject the null hypothesis
    :param group: The group name
    :type observations: ObservationSet
    :type alpha: float
    :type group: string
    :return: The dict containing the test results
    :rtype: dict

    """
    if not isinstance(observations, ObservationSet):
        raise ValueError('observations should be an instance of class ObservationSet')
    value_column = get_value_column_from_univariate(observations)
    group_data = observations._get_series(group, value_column)
    statistics, pvalue = stats.shapiro(group_data)
    hypotheses = hypotheses_normal_test(group)
    reject = pvalue < alpha
    return {
        'test': 'Shapiro-Wilk\'s normality test',
        'reject': reject,
        'winning_hypothesis': 'H1' if reject else 'H0',
        'statistics': statistics,
        'pvalue': pvalue,
        **hypotheses
    }
