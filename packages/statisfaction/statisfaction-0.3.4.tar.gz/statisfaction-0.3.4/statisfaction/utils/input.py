def statsmodels_to_scipy_test_type(test_type):
    """
    Changes the value of the test direction (or here test_type) strings to comply with sci-py formulations.

    :param test_type: the type of the test. Can be 'two-sided', 'larger' or 'greater'
    :type test_type: str
    :return: The complying test direction (or here test_type)
    :rtype: str

    """
    if test_type == 'two-sided':
        return 'two-sided'
    elif test_type == 'larger':
        return 'greater'
    elif test_type == 'smaller':
        return 'less'
    else:
        raise ValueError('Incorrect test type. Must be one of "two-sided", "smaller" or "larger"')


def get_value_column_from_univariate(observations):
    """
    Gets the name of the value_column of a univariate ObservationSet.

    :param observations: The ObservationSet
    :type observations: ObservationSet
    :return: The name of the value column
    :rtype: str

    """
    if len(observations.value_columns) != 1:
        raise ValueError('The passed ObservationSet contains more than one variable column.'
                         ' Select a variable with observations.get_variable(...)')
    return observations.value_columns[0]
