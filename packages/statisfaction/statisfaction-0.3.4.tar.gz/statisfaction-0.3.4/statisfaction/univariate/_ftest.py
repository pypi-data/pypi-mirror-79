import scipy.stats as stats

from ._interpretation import hypotheses_variance_comparison
from ..utils.input import get_value_column_from_univariate
from ..core import ObservationSet

"""
    ftest.py
    ======================

    This module contains the logic to run a f-test over a univariate sample.
    The F-test, aka Fischer test, is used to test the equality of variance between two normal distributions.

 """

def _f_test_pvalue(statistics, control_size, treatment_size, test_type):
    """
    Computes the p-value of the F-test.

    :param statistics: The calculated f-statistic.
    :param control_size: The size of the control group
    :param treatment_size: The size of the control group
    :param test_type: The direction of the test. Can be 'two-sided', 'larger' or 'smalller'.
    :type statistics: float
    :type control_size: integer
    :type treatment_size: integer
    :type test_type: string
    :return: The correct p-value of the F-test
    :rtype: float

    """
    larger_pvalue = stats.f.cdf(statistics, control_size - 1, treatment_size - 1)
    smaller_pvalue = stats.f.sf(statistics, control_size - 1, treatment_size - 1)
    if test_type == 'two-sided':
        return 2 * min(larger_pvalue, smaller_pvalue)
    elif test_type == 'larger':
        return larger_pvalue
    elif test_type == 'smaller':
        return smaller_pvalue
    else:
        raise ValueError('Incorrect test type. Must be one of "two-sided", "smaller" or "larger"')


def f_test_from_observations(observations, alpha=0.05, control_group='control', treatment_group='treatment', test_type='two-sided'):
    """
    Runs a F-test over an observation set.

    Returns a dict containing the test results.

    :param observations: The observation set over which the F-test is computed
    :param alpha: The maximum type I error tolerated reject the null hypothesis
    :param control_group: The control group name
    :param treatment_group: The treatment group name
    :param test_type: The direction of the test. Can be 'two-sided', 'larger' or 'smalller'.
    :type observations: ObservationSet
    :type alpha: float
    :type control_group: string
    :type treatment_group: string
    :type test_type: string
    :return: The dict containing the test results
    :rtype: dict

    """
    if not isinstance(observations, ObservationSet):
        raise ValueError('observations should be an instance of class ObservationSet')
    value_column = get_value_column_from_univariate(observations)
    treatment_data = observations._get_series(treatment_group, value_column)
    control_data = observations._get_series(control_group, value_column)
    statistics = control_data.var() / treatment_data.var()
    pvalue = _f_test_pvalue(statistics, len(control_data), len(treatment_data), test_type)
    hypotheses = hypotheses_variance_comparison(control_group, treatment_group, test_type)
    reject = pvalue < alpha
    return {
        'test': 'Fisher\'s F-Test',
        'reject': reject,
        'winning_hypothesis': 'H1' if reject else 'H0',
        'statistics': statistics,
        'pvalue': pvalue,
        **hypotheses
    }
