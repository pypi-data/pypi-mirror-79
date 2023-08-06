import pandas as pd
import statsmodels.formula.api as smf
from .._constants import group_id_column
from ..core import ObservationSet
from ..utils.input import get_value_column_from_univariate


"""
    diffindiff.py
    ======================

    This module contains the logic to run difference-in-difference estimations.

"""

def hypotheses_diff_in_diff(pre_control_group, post_control_group,
                            pre_treatment_group, post_treatment_group):
    h0 = 'The introduction of a treatment between "{}" and "{}" did not result in any significant change when comparing to "{}" and "{}"'.format(pre_treatment_group, post_treatment_group, pre_control_group, post_control_group)
    h1 = 'The introduction of a treatment between "{}" and "{}" resulted in any significant change when comparing to "{}" and "{}"'.format(pre_treatment_group, post_treatment_group, pre_control_group, post_control_group)
    return {'H0': h0, 'H1': h1}

def diff_in_diff_test_from_observations(observations, alpha=0.05,
                                        pre_control_group='pre-control', post_control_group='post-control',
                                        pre_treatment_group='pre-treatment', post_treatment_group='post-treatment'):
    """
    Runs a difference-in-difference over an observation set.

    The test groups are adapted to represent the four cases: {pre|post}-{control|treatment}
    Returns a dict containing the test results.

    :param observations: The observation set over which the ttest is computed
    :param alpha: The maximum type I error tolerated reject the null hypothesis
    :param pre_control_group: The pre-intervention control group name
    :param post_control_group: The post-intervention control group name
    :param pre_treatment_group: The pre-intervention treatment group name
    :param post_treatment_group: The post-intervention treatment group name
    :type observations: ObservationSet
    :type alpha: float
    :type pre_control_group: string
    :type post_control_group: string
    :type pre_treatment_group: string
    :type post_treatment_group: string
    :return: The dict containing the test results
    :rtype: dict

    """

    if not isinstance(observations, ObservationSet):
        raise ValueError('observations should be an instance of class ObservationSet')
    value_column = get_value_column_from_univariate(observations)

    data_copy = observations.data.copy()

    data_copy['treatment'] = (
        (data_copy[group_id_column] == pre_treatment_group)
        | (data_copy[group_id_column] == post_treatment_group)
    )
    data_copy['post'] = (
        (data_copy[group_id_column] == post_control_group)
        | (data_copy[group_id_column] == post_treatment_group)
    )

    results = smf.ols('{} ~ treatment * post'.format(value_column), data=data_copy).fit()

    absolute_effect = results.params['treatment[T.True]:post[T.True]']
    relative_effect = absolute_effect / (
        results.params['Intercept']
        + results.params['treatment[T.True]']
        + results.params['post[T.True]']
        )

    pvalue = results.pvalues['treatment[T.True]:post[T.True]']
    reject = pvalue < alpha

    hypotheses = hypotheses_diff_in_diff(pre_control_group, post_control_group,
                                         pre_treatment_group, post_treatment_group)

    return {
        'test': 'Difference-in-Difference Estimation',
        'reject': reject,
        'winning_hypothesis': 'H1' if reject else 'H0',
        'effect': absolute_effect,
        'relative_effect': relative_effect,
        'pvalue': pvalue,
        **hypotheses
    }


def diff_in_diff_confidence_interval_from_observations(observations, alpha=0.05,
                                                       pre_control_group='pre-control', post_control_group='post-control',
                                                       pre_treatment_group='pre-treatment', post_treatment_group='post-treatment'):
    """
    Computes the confidence interval of the effect measured in a difference-in-difference experiment.

    Returns a dict containing the effect and its confidence interval bounds.

    :param observations: The observation set over which the ttest is computed
    :param alpha: The maximum type I error tolerated reject the null hypothesis
    :param pre_control_group: The pre-intervention control group name
    :param post_control_group: The post-intervention control group name
    :param pre_treatment_group: The pre-intervention treatment group name
    :param post_treatment_group: The post-intervention treatment group name
    :type observations: ObservationSet
    :type alpha: float
    :type pre_control_group: string
    :type post_control_group: string
    :type pre_treatment_group: string
    :type post_treatment_group: string
    :return: The dict containing the effect and its confidence interval bounds.
    :rtype: dict

    """

    if not isinstance(observations, ObservationSet):
        raise ValueError('observations should be an instance of class ObservationSet')
    value_column = get_value_column_from_univariate(observations)

    data_copy = observations.data.copy()

    data_copy['treatment'] = (
        (data_copy[group_id_column] == pre_treatment_group)
        | (data_copy[group_id_column] == post_treatment_group)
    )
    data_copy['post'] = (
        (data_copy[group_id_column] == post_control_group)
        | (data_copy[group_id_column] == post_treatment_group)
    )

    results = smf.ols('{} ~ treatment * post'.format(value_column), data=data_copy).fit()

    absolute_effect = results.params['treatment[T.True]:post[T.True]']

    conf_int = results.conf_int(alpha=alpha, cols=None).loc['treatment[T.True]:post[T.True]']

    return {
        'lower_bound': conf_int[0],
        'upper_bound': conf_int[1],
        'effect': absolute_effect
    }

