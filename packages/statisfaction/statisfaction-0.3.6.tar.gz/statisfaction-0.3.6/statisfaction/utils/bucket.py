import numpy as np
import pandas as pd

from .._constants import observation_id_column, group_id_column, min_observations
from ..core import ObservationSet


def bucket(observations, bucket_size, group_equality=True):
    """
     Aggregate observations into bigger observations by averaging values.

    :param observations: The ObservationSet
    :param bucket_size: the multiplier for the granularity
    :param group_equality: Whether we want all groups to have the same number of observations. Default is True.
    :type observations: ObservationSet
    :type bucket_size: integer
    :type group_equality: boolean
    :return: The ObservationSet
    :rtype: ObservationSet

    """

    min_observations_in_a_group = observations.data.groupby(group_id_column).size().min()
    max_bucket_count = max(min_observations_in_a_group // bucket_size, min_observations)

    if bucket_size * max_bucket_count > min_observations_in_a_group:
        largest_size = min_observations_in_a_group // min_observations
        raise ValueError(('Select fewer observations per bucket!'
                          ' The smallest group is too small to have {}+ buckets with {} observations.'
                          ' The largest possible number of observations in a bucket is {}.'
                          ).format(min_observations, bucket_size, largest_size))

    if group_equality:
        new_data = _bucket(observations, bucket_size, bucket_count=max_bucket_count)
    else:
        new_data = _bucket(observations, bucket_size)

    return ObservationSet(data=new_data, granularity=observations.granularity * bucket_size,
                          value_columns=observations.value_columns)


def _bucket(observations, bucket_size, bucket_count=None):
    """
    Changes the observation_ids into buckets for each group of an ObservationSet

    :param observations: The ObservationSet
    :param bucket_size: the multiplier for the granularity
    :param bucket_count: the number of bucket to build
    :type observations: ObservationSet
    :type bucket_size: integer
    :type bucket_count: integer
    :return: The concatenated DataFrame of all the groups
    :rtype: DataFrame

    """
    dfs = []
    for group_value in observations.data[group_id_column].unique():
        group_df = observations.data.loc[observations.data[group_id_column] == group_value]
        if bucket_count is None:
            this_group_bucket_count = len(group_df) // bucket_size
        else:
            this_group_bucket_count = bucket_count
        dfs.append(_build_bucket_in_group(group_df, bucket_size, this_group_bucket_count, observations.value_columns))
    return pd.concat(dfs, axis=0)


def _build_bucket_in_group(df, bucket_size, bucket_count, value_columns):
    """
    Turns the observation_id column of a DataFrame into a bucket_id column.

    :param df: The DataFrame
    :param bucket_size: the size of the buckets to build
    :param bucket_count: the number of buckets to build
    :type df: DataFrame
    :type bucket_size: integer
    :type bucket_count: integer
    :return: The DataFrame with the bucket column
    :rtype: DataFrame

    """
    buckets = -1 * np.ones((len(df),), dtype=int)
    buckets[:(bucket_size * bucket_count)] = np.tile(np.arange(bucket_count), (1, bucket_size))
    np.random.shuffle(buckets)
    df['bucket'] = buckets
    df = df.loc[df['bucket'] != -1]
    agg_var = {**{c: 'mean' for c in value_columns}, group_id_column: 'min'}
    df = df.groupby('bucket').agg(agg_var)
    df.reset_index(drop=False, inplace=True)
    return df.rename(columns={'bucket': observation_id_column})

