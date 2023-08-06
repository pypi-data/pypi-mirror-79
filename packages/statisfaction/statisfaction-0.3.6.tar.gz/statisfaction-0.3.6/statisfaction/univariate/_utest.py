import scipy.stats as stats

from ._interpretation import hypotheses_u_test
from ..utils.input import get_value_column_from_univariate, statsmodels_to_scipy_test_type
from ..core import ObservationSet

"""
    utest.py
    ======================

    This module contains the logic to run a utest over a univariate sample.
    The U-test, aka Wilcoxon-Mann-Whitney test, is a non-parametric statistical test,
    ie a test that you can use when your data cannot be modelled by a normal distribution.

 """

def u_test_from_observations(observations, alpha=0.05, control_group='control', treatment_group='treatment',
           test_type='two-sided', use_continuity=True):
    """
    Runs a U-test over an observation set.

    Returns a dict containing the test results.

    :param observations: The observation set over which the U-test is computed
    :param alpha: The maximum type I error tolerated reject the null hypothesis
    :param control_group: The control group name
    :param treatment_group: The treatment group name
    :param test_type: The direction of the test. Can be 'two-sided', 'larger' or 'smalller'.
    :param use_continuity: Whether a continuity correction should be taken into account. Default is True.
    :type observations: ObservationSet
    :type alpha: float
    :type control_group: string
    :type treatment_group: string
    :type test_type: string
    :type use_continuity: boolean
    :return: The dict containing the test results
    :rtype: dict

    """
    if not isinstance(observations, ObservationSet):
        raise ValueError('observations should be an instance of class ObservationSet')
    value_column = get_value_column_from_univariate(observations)
    scipy_test_type = statsmodels_to_scipy_test_type(test_type)
    treatment_data = observations._get_series(treatment_group, value_column)
    control_data = observations._get_series(control_group, value_column)
    statistics, pvalue = stats.mannwhitneyu(
        treatment_data,
        control_data,
        use_continuity=use_continuity,
        alternative=scipy_test_type
    )
    hypotheses = hypotheses_u_test(control_group, treatment_group, test_type)
    reject = pvalue < alpha
    return {
        'test': 'Mann-Whitney\'s U-Test',
        'reject': reject,
        'winning_hypothesis': 'H1' if reject else 'H0',
        'statistics': statistics,
        'pvalue': pvalue,
        **hypotheses
    }
