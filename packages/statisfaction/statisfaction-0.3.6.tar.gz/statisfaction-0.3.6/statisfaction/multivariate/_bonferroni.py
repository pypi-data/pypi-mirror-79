from ..core import ObservationSet


def multivariate_bonferroni(observations, test_function, alpha=0.05, **test_parameters):
    """
    Runs a multivariate test with the selected test function using a bonferroni correction.

    In the case of a multivariate test, this function calls the selected test function and runs the test for each
    variable (each variable is a column of value_columns). The bonferroni correction means that we are using an
    adjusted alpha which is equal to alpha divided by the number of variables being tested. (alpha being the
    significance level i.e. the threshold that the p-value needs to be under for the test to be positive)


    Returns a dict containing a dictionary of test results for each variable.

    :param observations: The observation set over which the statistical tests will be computed
    :param test_function: The statistical test to be applied to all variables of the ObservationSet, e.g. univariate.t_test
    :param alpha: The significance level for all the variables. This means that if the null hypothesis is true for all variables,
                  there is a probability of less or equal than alpha that one of the tests outputs a false positive.
    :param test_parameters: additional parameters for `test_function`
    :type observations: ObservationSet
    :type alpha: float
    :type test_parameters: dict
    :return: The dict containing the test results for all variables. Key: a variable, value:
             the result of `test_function` applied to this variable
    :rtype: dict

    """
    if not isinstance(observations, ObservationSet):
        raise ValueError('observations should be an instance of class ObservationSet')

    corrected_alpha = alpha / len(observations.value_columns)
    result_dict = {}
    for variable in observations.value_columns:
        result_dict[variable] = test_function(observations.get_variable(variable), alpha=corrected_alpha, **test_parameters)

    return result_dict
