import statsmodels.stats.power as smp
import math as m

from ..univariate._interpretation import hypotheses_mean_comparison
from ..utils.input import get_value_column_from_univariate
from .._constants import group_id_column
from ..core import ObservationSet

"""
    ttest.py
    ======================
    This module contains the logic to calculate one of the three following parameters given the two others:
        -minimum detectable effect
        -sample size
        -share in control group

    >> Testing file: test_t_test_power.py
 """

def standard_deviation_bernoulli(mean):
    """
    Returns the standard deviation of a Bernoulli distribution given its mean
    """
    if not (0 < mean < 1):
        raise ValueError('The mean has to be strictly between 0 and 1')
    return m.sqrt( mean * (1 - mean) )


def t_test_power_from_aggregates(control_standard_deviation,
                                 control_mean,
                                 minimum_detectable_effect = None,
                                 sample_size = None,
                                 share_in_control_group = None,
                                 test_type = 'two-sided',
                                 alpha = 0.05,
                                 power = 0.8,
                                 control_group = 'control',
                                 treatment_group = 'treatment'):
    """
    Calculates one of the three following parameters given the two others for a two-sample t-test:
        -minimum_detectable_effect
        -sample_size
        -share_in_control_group (if empty, we try to maximize it. assumption to be checked that there is a symetry and we can use '1 - share_in_control_group' if wanted)

    The standard deviation and the mean of the control group are needed to run the power calculation.

    :param control_standard_deviation: The standard deviation of the control group. It is needed to run the power calculation
    :param control_mean: The mean of the control group. It is needed to run the power calculation
    :param minimum_detectable_effect: One of the three key parameters of the function. It is either:
        -empty (None) when computing its value based on the two other parameters (sample_size and share_in_control_group)
        -filled when computing the value of one of the two other parameters (sample_size and share_in_control_group)
    :param sample_size: One of the three key parameters of the function. It is either:
        -empty (None) when computing its value based on the two other parameters (minimum_detectable_effect and share_in_control_group)
        -filled when computing the value of one of the two other parameters (minimum_detectable_effect and share_in_control_group)
    :param share_in_control_group: One of the three key parameters of the function. It is either:
        -empty (None) when computing its value based on the two other parameters (minimum_detectable_effect and sample_size).
        In this situation, we maximize the share_in_control_group (it is ok to change the share in control group and treatment group afterwards)
        -filled when computing the value of one of the two other parameters (minimum_detectable_effect and sample_size)
    :param test_type: The type of t-test used to run the power calculation. It has to be set as one of the following values:
        -two-sided
        -larger
        -smaller
    :param alpha: The significance level used to run the power calculation
    :param power: The power used to run the power calculation
    :param control_group: The name of the control group. It is used only to display the hypotheses
    :param treatment_group: The name of the treatment group. It is used only to display the hypotheses
    :type control_standard_deviation: float
    :type control_mean: float
    :type minimum_detectable_effect: float
    :type sample_size: int
    :type share_in_control_group: float
    :type test_type: string
    :type alpha: float
    :type power: float
    :type control_group: string
    :type treatment_group: string
    :return: The dict containing all the parameters and the result of the power calculation
    """

    # errors
    if control_standard_deviation <= 0:
        raise ValueError('control_standard_deviation has to be strictly positive')
    if (minimum_detectable_effect is None and sample_size is None) or (minimum_detectable_effect is None and share_in_control_group is None) or (sample_size is None and share_in_control_group is None):
        raise ValueError('You have to fill exactly two of these three parameters:\nminimum_detectable_effect,\sample_size,\nshare_in_control_group')
    if not (minimum_detectable_effect is None) and not (sample_size is None) and not (share_in_control_group is None):
        raise ValueError('You have to leave exactly one of these three parameters blank:\nminimum_detectable_effect,\sample_size,\nshare_in_control_group')

    # minimum_detectable_effect missing
    if minimum_detectable_effect is None:
        effect_size = smp.TTestIndPower().solve_power(
            effect_size = None,
            nobs1 = sample_size * share_in_control_group,
            ratio = (1 - share_in_control_group) / share_in_control_group,
            alpha = alpha,
            power = power,
            alternative = test_type
        )
        minimum_detectable_effect = effect_size * control_standard_deviation

    # sample_size missing
    elif sample_size is None:
        nobs1 = smp.TTestIndPower().solve_power(
            effect_size = minimum_detectable_effect / control_standard_deviation,
            nobs1 = None,
            ratio = (1 - share_in_control_group) / share_in_control_group,
            alpha = alpha,
            power = power,
            alternative = test_type
        )
        sample_size = m.ceil(nobs1 / share_in_control_group)

    # share_in_control_group missing
    elif share_in_control_group is None:
        control_size = sample_size / 2 # as a start we assign half the population to the control_size
        iteration_marging = 2
        i=0
        while iteration_marging > 0.05: # we iterate until we don't manage to further increase the control_size
            ratio = smp.TTestIndPower().solve_power(
                effect_size = minimum_detectable_effect / control_standard_deviation,
                nobs1 = control_size,
                ratio=None,
                alpha = alpha,
                power = power,
                alternative = test_type
            )
            if ratio >= 1: # in this case we would have treatment_size > control_size, and therefore treatment_size + control_size > sample_size , this is not possible
                raise ValueError('The experiment cannot be conducted under the given parameters')
            treatment_size = control_size * ratio # this is how the ratio is defined - http://www.statsmodels.org/dev/generated/statsmodels.stats.power.TTestIndPower.solve_power.html#statsmodels.stats.power.TTestIndPower.solve_power
            control_size_new = sample_size - treatment_size # we assigned all "remaining members to the treatment group"
            iteration_marging = (control_size_new / control_size) - 1 # we check how much we have increased the control_size
            control_size = control_size_new # we update the control_size
        share_in_control_group = control_size / sample_size # we have increased the control_group as big as possible

    # we return a dictionary with the three parameters filled
    relative_minimum_detectable_effect = minimum_detectable_effect / abs(control_mean)
    hypotheses = hypotheses_mean_comparison(control_group, treatment_group, test_type)
    return {
        'test': 'Student\'s T-test',  # TODO: verify this is not a Welsh's t-test
        'control_standard_deviation': control_standard_deviation,
        'control_mean': control_mean,
        'minimum_detectable_effect': minimum_detectable_effect,
        'relative_minimum_detectable_effect': relative_minimum_detectable_effect,
        'sample_size': sample_size,
        'share_in_control_group': share_in_control_group,
        'alpha': alpha,
        'power': power,
        'test_type': test_type,
        **hypotheses
    }


def t_test_power_from_observations(observations,
                                   minimum_detectable_effect=None,
                                   sample_size=None,
                                   share_in_control_group=None,
                                   ratio=None,
                                   test_type='two-sided',
                                   alpha=0.05,
                                   power=0.8,
                                   control_group='control',
                                   treatment_group='treatment'):
    """
    Calculates one of the three following parameters given the two others for a two sample t-test:
        -minimum detectable effect
        -sample size
        -share in control group
    The observation set is used to compute the standard deviation and the mean of the control group, which are needed to run the power calculation.

    :param observations: The observation set used to compute the standard deviation and the mean of the control group.
    It is needed to run the power calculation
    :param minimum_detectable_effect: One of the three key parameters of the function. It is either:
        -empty (None) when computing its value based on the two other parameters (sample_size and share_in_control_group)
        -filled when computing the value of one of the two other parameters (sample_size and share_in_control_group)
    :param sample_size: One of the three key parameters of the function. It is either:
        -empty (None) when computing its value based on the two other parameters (minimum_detectable_effect and share_in_control_group)
        -filled when computing the value of one of the two other parameters (minimum_detectable_effect and share_in_control_group)
    :param share_in_control_group: One of the three key parameters of the function. It is either:
        -empty (None) when computing its value based on the two other parameters (minimum_detectable_effect and sample_size).
        In this situation, we maximize the share_in_control_group (it is ok to change the share in control group and treatment group afterwards)
        -filled when computing the value of one of the two other parameters (minimum_detectable_effect and sample_size)
        This parameter can take two values depending of what is needed:
            -'same_as_observations' when the share in control group to run the power calculation is the same as the one in the observations parameter
            -'from_ratio_param' when we want to input the share in control group to run the power calculation
    :param ratio: The ratio used as the share in control group when share_in_control_group = 'from_ratio_param'
    :param test_type: The type of t-test used to run the power calculation. It has to be set as one of the following values:
        -two-sided
        -larger
        -smaller
    :param alpha: The significance level used to run the power calculation
    :param power: The power used to run the power calculation
    :param control_group: The name of the control group. It is used to compute the standard deviation and the mean of the control group, and to display the hypotheses
    :param treatment_group: The name of the treatment group. It is used to compute the standard deviation and the mean of the control group, and to display the hypotheses
    :type observations: ObservationSet
    :type minimum_detectable_effect: float
    :type sample_size: int
    :type share_in_control_group: string
    :type ratio: float
    :type test_type: string
    :type alpha: float
    :type power: float
    :type control_group: string
    :type treatment_group: string
    :return: The dict containing all the parameters and the result of the power calculation
    """

    # errors
    if not isinstance(observations, ObservationSet):
        raise ValueError('observations should be an instance of class ObservationSet')
    if observations.granularity != 1:
        raise ValueError('The function doesn\'t work when observations.granularity doesn\'t equal 1')
    if not share_in_control_group in [None, 'same_as_observations', 'from_ratio_param']:
        raise ValueError('share_in_control_group can only take one of these values: [None, \'same_as_observations\', \'from_ratio_param\']')

    # computation of standard deviation and control mean
    value_column = get_value_column_from_univariate(observations)
    control_standard_deviation = observations._get_series(control_group, value_column).std()
    control_mean = observations._get_series(control_group, value_column).mean()

    # computation of share in control group depending of its value
    if share_in_control_group is None:
        computed_share_in_control_group = None
    elif share_in_control_group == 'same_as_observations':
        nb_observations_in_control = len(observations._get_series(control_group, value_column))
        nb_observations_in_treatment = len(observations._get_series(treatment_group, value_column))
        computed_share_in_control_group = nb_observations_in_control / (nb_observations_in_control + nb_observations_in_treatment)
    elif share_in_control_group == 'from_ratio_param':
        computed_share_in_control_group = ratio

    # we can now use duration.t_test_power
    result = t_test_power_from_aggregates(
        control_standard_deviation = control_standard_deviation,
        control_mean = control_mean,
        minimum_detectable_effect = minimum_detectable_effect,
        sample_size = sample_size,
        share_in_control_group = computed_share_in_control_group,
        test_type = test_type,
        alpha = alpha,
        power = power,
        control_group = control_group,
        treatment_group = treatment_group)
    return {
        ** result
    }
