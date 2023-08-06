import pandas as pd
import vertica_python as v

from ._validation import validate


def read_vertica(query, connection=None, connection_params=None,
                 observation_id_col='observation_id', group_id_col='group_id', value_cols=['value'],
                 sql_params={}):
    """
    Runs the inputed query on Vertica and outputs an ObservationSet.
    Your query must return at least the following columns:
        * an observation_id column, that contains a unique identifier for each line - or observation - in the data
        * a group_id column, that attaches one observation to a group, typically the control or the treatment(s) group
        * one or several value columns, depending on the type of statistical tests that you want to run, ie univariate or multivariate


    :param query: The query returning your test observations
    :param connection: The name of the observation_id column
    :param connection_params: The connection parameters in a dict
    :param observation_id_col: The name of the observation_id column
    :param group_id_col: The name of the group_id column
    :param value_cols: The name of the value columns stored in an array
    :param sql_params: The parameters to make your query dynamic
    :type query: string
    :type connection: SQLAlchemy connectable(engine/connection) or database string URI
    :type connection_params: dict
    :type observation_id_col: string
    :type group_id_col: string
    :type value_cols: array
    :type sql_params: dict

    :return: The ObservationSet
    :rtype: ObservationSet

    """
    if connection is not None:
        data = pd.read_sql(query, connection, **sql_params)
    elif connection_params is not None:
        with v.connect(**connection_params) as connection:
            data = pd.read_sql(query, connection, **sql_params)
    else:
        raise ValueError('You must specify either "connection" or "connection_params"')
    return validate(data, observation_id_col, group_id_col, value_cols)
