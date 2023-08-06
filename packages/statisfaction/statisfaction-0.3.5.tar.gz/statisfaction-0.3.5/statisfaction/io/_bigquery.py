import pandas as pd

from ._validation import validate


def read_gbq(query, project_id, private_key=None, observation_id_col='observation_id', group_id_col='group_id',
             value_cols=['value'], gbq_kwargs={}):
    """
    Runs the inputed query on Google BigQuery and outputs an ObservationSet.
    Your query must return at least the following columns:
        * an observation_id column, that contains a unique identifier for each line - or observation - in the data
        * a group_id column, that attaches one observation to a group, typically the control or the treatment(s) group
        * one or several value columns, depending on the type of statistical tests that you want to run, ie univariate or multivariate


    :param query: The query returning your test observations
    :param private_key: The private key. Can be file path or string content.
    :param project_id: The project_id
    :param observation_id_col: The name of the observation_id column
    :param group_id_col: The name of the group_id column
    :param value_cols: The name of the value columns stored in an array
    :param gbq_kwargs: The parameters to make your query dynamic
    :type query: str
    :type private_key: str
    :type project_id: str
    :type observation_id_col: str
    :type group_id_col: str
    :type value_cols: array
    :type gbq_kwargs: dict

    :return: The ObservationSet
    :rtype: ObservationSet

    """
    gbq_kwargs_with_standard_sql = {'dialect': 'standard', **gbq_kwargs}
    data = pd.read_gbq(query=query, project_id=project_id, private_key=private_key,
                       **gbq_kwargs_with_standard_sql)
    return validate(data, observation_id_col, group_id_col, value_cols)
