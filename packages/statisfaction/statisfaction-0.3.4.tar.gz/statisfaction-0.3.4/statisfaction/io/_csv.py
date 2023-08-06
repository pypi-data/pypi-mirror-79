import pandas as pd

from ._validation import validate


def read_csv(filename, observation_id_col='observation_id', group_id_col='group_id', value_cols=['value'], csv_kwargs={}):
    """
    Turns data contained in a csv file into an ObservationSet.
    Your data must contain at least the following columns:
        * an observation_id column, that contains a unique identifier for each line - or observation - in the data
        * a group_id column, that attaches one observation to a group, typically the control or the treatment(s) group
        * one or several value columns, depending on the type of statistical tests that you want to run, ie univariate or multivariate


    :param filename: The file path of your csv file
    :param observation_id_col: The name of the observation_id column
    :param group_id_col: The name of the group_id column
    :param value_cols: The name of the value columns stored in an array
    :type filename: str
    :type observation_id_col: str
    :type group_id_col: str
    :type value_cols: array

    :return: The ObservationSet
    :rtype: ObservationSet

    """
    data = pd.read_csv(filename, **csv_kwargs)
    return validate(data, observation_id_col, group_id_col, value_cols)
