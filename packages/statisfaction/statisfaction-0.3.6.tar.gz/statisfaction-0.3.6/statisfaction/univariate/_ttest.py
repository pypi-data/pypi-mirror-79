import scipy.stats as stats
from scipy.stats import t
import numpy as np
from ..core import ObservationSet
from .._constants import group_id_column
from ._interpretation import hypotheses_mean_comparison
from ..utils.input import get_value_column_from_univariate
from decimal import Decimal


"""
    ttest.py
    ======================

    This module contains the logic to run ttests over a univariate sample and get confidence intervals for the means and the uplift.

 """

def _t_test_pvalue(statistics, two_sided_pvalue, test_type):
    """
    Transforms a two_sided_pvalue into its correct value depending on the test_direction (or test_type here).

    :param statistics: The calculated t-statistic.
    :param two_sided_pvalue: The two-tailed p-value.
    :param test_type: The direction of the test. Can be 'two-sided', 'larger' or 'smalller'.
    :type statistics: float
    :type two_sided_pvalue: float
    :type test_type: string
    :return: The correct p-value depending on the type of test
    :rtype: float

    """
    if test_type == 'two-sided':
        return two_sided_pvalue
    elif test_type == 'larger':
        if statistics >= 0:
            return 0.5 * two_sided_pvalue
        else:
            return 1 - 0.5 * two_sided_pvalue
    elif test_type == 'smaller':
        if statistics <= 0:
            return 0.5 * two_sided_pvalue
        else:
            return 1 - 0.5 * two_sided_pvalue
    else:
        raise ValueError('Incorrect test type. Must be one of "two-sided", "smaller" or "larger"')


def t_test_from_aggregates(control_group_size,
    treatment_group_size,
    control_group_mean, treatment_group_mean, control_group_std, treatment_group_std, alpha=0.05,test_type='two-sided', equal_variance=False):
    """
    Runs a t-test over an observation set.

    Returns a dict containing the test results.

    :param control_group_size: The number of observations in the control group
    :param treatment_group_size: The number of observations in the treatment group
    :param control_group_mean: The control group mean
    :param treatment_group_mean: The treatment group mean
    :param control_group_std: The control group standard deviation
    :param treatment_group_std: The treatment group standard deviation
    :param alpha: The maximum type I error tolerated reject the null hypothesis
    :param test_type: The direction of the test. Can be 'two-sided', 'larger' or 'smalller'.
    :param equal_variance: Whether the control and treatment groups have the same variance. Default is False.
    :type control_group_size: int
    :type treatment_group_size: int
    :type control_group_mean: float
    :type treatment_group_mean: float
    :type control_group_std: float
    :type treatment_group_std: float
    :type alpha: float
    :type test_type: string
    :type equal_variance: boolean
    :return: The dict containing the test results
    :rtype: dict

    """

    if equal_variance:
        #We apply a Student's t-test
        df = treatment_group_size + control_group_size - 2
        pooled_var = ((treatment_group_size - 1) * (treatment_group_std ** 2) + (control_group_size - 1) * (control_group_std ** 2)) / df
        t_denominator = np.sqrt(pooled_var * (1 / treatment_group_size + 1 / control_group_size))
        statistics = (treatment_group_mean - control_group_mean) / t_denominator

    else:
        #We apply a Welch's t-test
        control_group_var = control_group_std ** 2
        treatment_group_var = treatment_group_std ** 2
        df = int((treatment_group_var / treatment_group_size + control_group_var / control_group_size)**2 / # Welch-Satterthwaite equation
            ((treatment_group_var / treatment_group_size)**2 / (treatment_group_size - 1) + (control_group_var / control_group_size)**2 / (control_group_size - 1)))
        statistics = (treatment_group_mean - control_group_mean) / np.sqrt(treatment_group_var / treatment_group_size + control_group_var / control_group_size)

    if stats.t.cdf(statistics, df) >= 0.5:
        two_sided_pvalue = stats.t.sf(statistics, df) * 2
    else:
        two_sided_pvalue = stats.t.cdf(statistics, df) * 2
    hypotheses = hypotheses_mean_comparison('control', 'treatment', test_type)
    pvalue = _t_test_pvalue(statistics, two_sided_pvalue, test_type)
    reject = pvalue < alpha

    return {
        'test': 'Student\'s T-test' if equal_variance else 'Welsh\'s T-test',
        'reject': reject,
        'winning_hypothesis': 'H1' if reject else 'H0',
        'statistics': statistics,
        'pvalue': pvalue,
        **hypotheses
    }


def t_test_from_observations(observations, alpha=0.05, control_group='control', treatment_group='treatment', test_type='two-sided', equal_variance=False):
    """
    Runs a t-test over an observation set.

    Returns a dict containing the test results.

    :param observations: The observation set over which the ttest is computed
    :param alpha: The maximum type I error tolerated to reject the null hypothesis
    :param control_group: The control group name
    :param treatment_group: The treatment group name
    :param test_type: The direction of the test. Can be 'two-sided', 'larger' or 'smalller'.
    :param equal_variance: Whether the control and treatment groups have the same variance. Default is False.
    :type observations: ObservationSet
    :type alpha: float
    :type control_group: string
    :type treatment_group: string
    :type test_type: string
    :type equal_variance: boolean
    :return: The dict containing the test results
    :rtype: dict

    """
    if not isinstance(observations, ObservationSet):
        raise ValueError('observations should be an instance of class ObservationSet')
    value_column = get_value_column_from_univariate(observations)
    treatment_data = observations._get_series(treatment_group, value_column)
    control_data = observations._get_series(control_group, value_column)
    statistics, two_sided_pvalue = stats.ttest_ind(
        treatment_data,
        control_data,
        axis=0,
        equal_var=equal_variance,
        nan_policy='raise'
    )
    hypotheses = hypotheses_mean_comparison(control_group, treatment_group, test_type)
    pvalue = _t_test_pvalue(statistics, two_sided_pvalue, test_type)
    reject = pvalue < alpha
    return {
        'test': 'Student\'s T-test' if equal_variance else 'Welsh\'s T-test',
        'reject': reject,
        'winning_hypothesis': 'H1' if reject else 'H0',
        'statistics': statistics,
        'pvalue': pvalue,
        **hypotheses
    }


def sample_mean_t_confidence_interval_from_aggregates(sample_size, sample_mean, sample_std, alpha=0.05):
    """
    Computes the confidence interval of the mean of one group (control group for example).

    Returns a dict containing the confidence interval bounds, center and standard error.

    :param sample_size: The number of observations
    :param sample_mean: The sample mean
    :param sample_std: The standard deviation
    :param alpha: The maximum type I error tolerated reject the null hypothesis
    :type sample_size: int
    :type sample_mean: float
    :type sample_std: float
    :type alpha: float
    :return: The dict containing the confidence interval bounds, center and standard error
    :rtype: dict

    """

    df = sample_size - 1

    talpha = t.ppf(1 - alpha / 2, df)

    std_error = talpha*np.sqrt(( sample_std ** 2) / sample_size)

    lower_bound = sample_mean - std_error
    upper_bound = sample_mean + std_error

    return  {
        'lower_bound': lower_bound,
        'upper_bound': upper_bound,
        'std_error': std_error,
        'sample_mean': sample_mean
    }


def sample_mean_t_confidence_interval_from_observations(observations, alpha=0.05, group='control'):
    """
    Computes the confidence interval of the mean of one group (control group for example).

    Returns a dict containing the confidence interval bounds, center and standard error.

    :param observations: The observation set over which the ttest is computed
    :param alpha: The maximum type I error tolerated reject the null hypothesis
    :param group: The group name
    :type observations: ObservationSet
    :type alpha: float
    :type group: string
    :return: The dict containing the confidence interval bounds, center and standard error
    :rtype: dict

    """
    if not isinstance(observations, ObservationSet):
        raise ValueError('observations should be an instance of class ObservationSet')
    value_column = get_value_column_from_univariate(observations)
    group_data = observations._get_series(group, value_column)

    sample_mean = group_data.mean()
    sample_std = group_data.std()
    sample_size = len(group_data)

    return  sample_mean_t_confidence_interval_from_aggregates(sample_size, sample_mean, sample_std, alpha)


def uplift_t_confidence_interval_from_aggregates(
        control_group_size,  treatment_group_size, control_group_mean, treatment_group_mean,
        control_group_std, treatment_group_std, alpha=0.05, equal_variance=False):
    """
    Computes the confidence interval of the uplift between a control group and a treatment group.

    Returns a dict containing the confidence interval bounds, center and standard error.


    :param control_group_size: The number of observations in the control group
    :param treatment_group_size: The number of observations in the treatment group
    :param control_group_mean: The control group mean
    :param treatment_group_mean: The treatment group mean
    :param control_group_std: The control group standard deviation
    :param treatment_group_std: The treatment group standard deviation
    :param alpha: The maximum type I error tolerated reject the null hypothesis
    :type control_group_size: int
    :type treatment_group_size: int
    :type control_group_mean: float
    :type treatment_group_mean: float
    :type control_group_std: float
    :type treatment_group_std: float
    :type equal_variance: boolean
    :return: The dict containing the confidence interval bounds, center and standard error
    :rtype: dict

    """

    if equal_variance:

        df = treatment_group_size + control_group_size - 2
        pooled_var = ((treatment_group_size - 1) * (treatment_group_std ** 2) + (control_group_size - 1) * (control_group_std ** 2)) / df

        talpha = t.ppf(1 - alpha / 2, df)

        std_error = talpha * np.sqrt(pooled_var * (1 / treatment_group_size + 1 / control_group_size))
        sample_uplift = treatment_group_mean - control_group_mean

        lower_bound = sample_uplift - std_error
        upper_bound = sample_uplift + std_error

        return  {
            'lower_bound': lower_bound,
            'upper_bound': upper_bound,
            'std_error': std_error,
            'sample_uplift': sample_uplift
        }

    else:

        agg_var = control_group_std ** 2 / control_group_size + treatment_group_std ** 2 / treatment_group_size

        df = agg_var ** 2 / (  (control_group_std ** 2 / control_group_size) ** 2 / (control_group_size - 1)
                             + (treatment_group_std ** 2 / treatment_group_size) ** 2 / (treatment_group_size - 1))

        talpha = t.ppf(1 - alpha / 2, df)

        std_error = talpha * np.sqrt(agg_var)
        sample_uplift = treatment_group_mean - control_group_mean

        lower_bound = sample_uplift - std_error
        upper_bound = sample_uplift + std_error

        return  {
            'lower_bound': lower_bound,
            'upper_bound': upper_bound,
            'std_error': std_error,
            'sample_uplift': sample_uplift
        }

def uplift_t_confidence_interval_from_observations(observations, alpha=0.05, control_group='control', treatment_group='treatment',
                                                   equal_variance=False):
    """
    Computes the confidence interval of the uplift between a control group and a treatment group.

    Returns a dict containing the confidence interval bounds, center and standard error.

    :param observations: The observation set over which the ttest is computed
    :param alpha: The maximum type I error tolerated reject the null hypothesis
    :param control_group: The control group name
    :param treatment_group: The treatment group name
    :type observations: ObservationSet
    :type alpha: float
    :type control_group: string
    :type treatment_group: string
    :return: The dict containing the confidence interval bounds, center and standard error
    :rtype: dict

    """
    if not isinstance(observations, ObservationSet):
        raise ValueError('observations should be an instance of class ObservationSet')
    value_column = get_value_column_from_univariate(observations)

    c_data = observations._get_series(control_group, value_column)
    t_data = observations._get_series(treatment_group, value_column)

    treatment_group_mean = t_data.mean()
    control_group_mean = c_data.mean()
    treatment_group_std = t_data.std()
    control_group_std = c_data.std()
    treatment_group_size = len(t_data)
    control_group_size = len(c_data)

    return  uplift_t_confidence_interval_from_aggregates(control_group_size,
                                        treatment_group_size,
                                        control_group_mean,
                                        treatment_group_mean,
                                        control_group_std,
                                        treatment_group_std,
                                        alpha, equal_variance)




