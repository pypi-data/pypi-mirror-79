from ._validation import validate


def read_pandas(df, observation_id_col='observation_id', group_id_col='group_id', value_cols=['value']):
    """
    Turns a DataFrame into an ObservationSet.
    Your DataFrame must contain at least the following columns:
        * an observation_id column, that contains a unique identifier for each line - or observation - in the data
        * a group_id column, that attaches one observation to a group, typically the control or the treatment(s) group
        * one or several value columns, depending on the type of statistical tests that you want to run, ie univariate or multivariate


    :param df: The dataframe containing your test observations
    :param observation_id_col: The name of the observation_id column
    :param group_id_col: The name of the group_id column
    :param value_cols: The name of the value columns stored in an array
    :type df: DataFrame
    :type observation_id_col: str
    :type group_id_col: str
    :type value_cols: array

    :return: The ObservationSet
    :rtype: ObservationSet

    """
    return validate(df, observation_id_col, group_id_col, value_cols)

