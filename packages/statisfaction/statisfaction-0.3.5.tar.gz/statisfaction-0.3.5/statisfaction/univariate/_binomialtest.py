import scipy.stats as stats
import numpy as np
from ..core import ObservationSet
from ._interpretation import hypotheses_binomial_test


"""
    groupAllocation.py
    ======================

    This module contains the logic to test the allocation of observations in each group of your test.

 """

def binomial_test_from_aggregates(control_group_sample_size, treatment_group_sample_size, target_treatment_share=0.5,
                                  alpha=0.05, control_group='control', treatment_group='treatment'):
    """
    Computes the probability of observing a given allocation of the observations in each group of a test, given a target distribution.

    :param control_group_sample_size: The number of observations in the control group since the beginning of the test
    :param treatment_group_sample_size: The number of observations in the treatment group since the beginning of the test
    :param target_treatment_share: The theoretical share of observations in the treatment group
    :param alpha: The maximum type I error tolerated reject the null hypothesis
    :param control_group: The control group name
    :param treatment_group: The treatment group name
    :type control_group_sample_size: int
    :type treatment_group_sample_size: int
    :type target_treatment_share: float
    :type alpha: float
    :type control_group: string
    :type treatment_group: string
    :return: The dict containing the test results
    :rtype: dict

    """

    total_observation_number = control_group_sample_size + treatment_group_sample_size
    pvalue = stats.binom_test(treatment_group_sample_size, total_observation_number, target_treatment_share)
    observed_allocation = treatment_group_sample_size / (control_group_sample_size + treatment_group_sample_size)
    reject = pvalue < alpha
    hypotheses = hypotheses_binomial_test(control_group, treatment_group, target_treatment_share)
    return {
        'control_sample_size': control_group_sample_size,
        'treatment_sample_size': treatment_group_sample_size,
        'observed_allocation': observed_allocation,
        'pvalue': pvalue,
        'test': 'Binomial test',
        'reject': reject,
        'winning_hypothesis': 'H1' if reject else 'H0',
        **hypotheses
    }


def binomial_test_from_observations(observation, target_treatment_share=0.5,
                                    alpha=0.05, control_group='control', treatment_group='treatment'):
    """
    Computes the probability of observing a given allocation of the observations in each group of a test, given a target distribution.

    :param control_group_sample_size: The number of observations in the control group since the beginning of the test
    :param treatment_group_sample_size: The number of observations in the treatment group since the beginning of the test
    :param target_treatment_share: The theoretical share of observations in the treatment group
    :param alpha: The maximum type I error tolerated reject the null hypothesis
    :param control_group: The control group name
    :param treatment_group: The treatment group name
    :type control_group_sample_size: int
    :type treatment_group_sample_size: int
    :type target_treatment_share: float
    :type alpha: float
    :type control_group: string
    :type treatment_group: string
    :return: The dict containing the test results
    :rtype: dict

    """
    control_group_sample_size = len(observation._get_series(control_group, observation.value_columns))
    treatment_group_sample_size = len(observation._get_series(treatment_group, observation.value_columns))
    observed_allocation = treatment_group_sample_size / (control_group_sample_size + treatment_group_sample_size)
    return binomial_test_from_aggregates(control_group_sample_size, treatment_group_sample_size, target_treatment_share)

