from .._constants import *
from ..core import ObservationSet
import numpy as np



def validate(data, observation_id_col, group_id_col, value_cols):

    """
    1/ Validates that the column names inputed by the user in the I/O function are present in the data.
    2/ Renames the columns of the DataFrame using names referenced in utils/constants.py
    3/ Then turns the data into an ObservationSet of granularity 1

    :param data: The data to validate
    :param observation_id_col: The name of the observation_id column
    :param group_id_col: The name of the group_id column
    :param value_cols: The name of the value columns
    :type data: DataFrame
    :type observation_id_col: string
    :type group_id_col: string
    :type value_cols: array

    :return: The validated ObservationSet
    :rtype: ObservationSet

    """

    if observation_id_col not in data.columns:
        raise ValueError('{} column, called "{}", is not in data'.format(observation_id_column, observation_id_col))
    if group_id_col not in data.columns:
        raise ValueError('{} column, called "{}", is not in data'.format(group_id_column, group_id_col))
    for col in value_cols:
        if col not in data.columns:
            raise ValueError('Value column, called "{}", is not in data'.format(col))
    if (data.groupby([observation_id_col, group_id_col]).count()[value_cols[0]] > 1).any():
        raise ValueError('There are duplicates {} x {} in your data!'.format(observation_id_col, group_id_col))
    data = data.rename(columns={
        observation_id_col: observation_id_column,
        group_id_col: group_id_column
    })
    columns = [observation_id_column, group_id_column] + value_cols
    data = data[columns]
    return ObservationSet(data=data, granularity=1, value_columns=value_cols)
