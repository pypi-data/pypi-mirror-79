from ..core import ObservationSet
import warnings

def multipopulation_bonferroni(observations, test_function, alpha=0.05, group_names=[''], **test_parameters):
    """
    Runs a multipopulation test with the selected test function using a bonferroni correction.

    In the case of a multipopulation test, this function calls the selected test function and runs the test for each
    pair of population. The bonferroni correction means that we are using an
    adjusted alpha which is equal to alpha divided by the number of population pairs being tested.

    Returns a dict containing a dictionary of test results for population pair.

    :param observations: The observation set over which the statistical tests will be computed
    :param test_function: The statistical test to be applied to the populations of the ObservationSet, e.g. univariate.t_test
    :param alpha: The significance level for the population pairs of the test. This means that if the null hypothesis is true for all population pairs,
                  there is a probability of less or equal than alpha that one of the tests outputs a false positive.
    :param test_parameters: additional parameters for `test_function`
    :type observations: ObservationSet
    :type alpha: float
    :type test_parameters: dict
    :return corrected_alpha: The corrected alpha applied in the test function
    :rtype corrected_alpha: float
    :return result_dict: The dict containing the test results for all populations. Key:  (population1, population2), value:
             the result of `test_function` applied to these populations
    :rtype result_dict: dict

    """
    if 'test_type' in test_parameters and test_parameters['test_type'] != 'two-sided':
        test_parameters['test_type'] = 'two-sided'
        warnings.warn("We replaced your test type. It's now 'two-sided', aka the only test type authorized for multipopulation testing")


    if not isinstance(observations, ObservationSet):
        raise ValueError('observations should be an instance of class ObservationSet')

    observation_group_names = observations.get_group_names()

    for group in group_names:
        if group not in observation_group_names:
            raise ValueError('Group {} is not in your ObservationSet.'.format(group)) 

    n = len(group_names)
    divisor = n*(n-1)/2
    corrected_alpha = alpha/divisor

    result_dict = {}
    for i in range(len(group_names)):
        for j in range(len(group_names)):
            result_dict[(group_names[i], group_names[j])] = test_function(observations = observations, alpha = corrected_alpha, control_group = group_names[i], treatment_group = group_names[j], **test_parameters)

    return corrected_alpha, result_dict