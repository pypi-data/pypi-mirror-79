from .._constants import group_id_column, observation_id_column

"""
    observation.py
    ======================

    This module contains the logic of the Class Observation.
 """

class ObservationSet(object):
    """
    The ObservationSet class is a wrapper around a DataFrame containing the observations collected during an A/B test
    In order to make it easily usable for statistical calculations, the data should be organized around three types of columns:
        * an observation_id column, that contains a unique identifier for each line - or observation - in the data
        * a group_id column, that attaches one observation to a group, typically the control or the treatment(s) group
        * one or several value columns, depending on the type of statistical tests that you want to run, ie univariate or multivariate


    """

    def __init__(self, data, granularity, value_columns):
        """
        Creates an instance of the ObservationSet Class.

        :param data: The data set containing our test observations.
        :param granularity: The number of observations aggregated to create one line in the data.
        :param value_columns: The name of the value columns
        :type data: DataFrame
        :type granularity: integer
        :type value_columns: array

        """
        self.data = data
        self.granularity = granularity
        self.value_columns = value_columns

    def _get_series(self, group, value_column):
        """
        Returns a Pandas Series containing the values of all the observations in the sample for a specific metrics/value/column

        :param group: The name of the targetted group.
        :param value_column: The name of the value column
        :type group: string
        :type value_column: string
        :return: The serie containing the values
        :rtype: Pandas Series

        """
        return self.data.loc[self.data[group_id_column] ==  group, value_column]

    def get_variable(self, value_column):
        """
        Returns an ObservationSet limited to one value. This is useful for multivariate ObservationSet.

        :param value_column: The name of the value column
        :type value_column: string
        :return: The ObservationSet limited to the chosen value
        :rtype: ObservationSet

        """

        if not value_column in self.value_columns:
            raise ValueError('Value column "{}" does not exist in this observation set'.format(value_column))
        columns = [observation_id_column, group_id_column, value_column]
        return ObservationSet(self.data[columns], self.granularity, [value_column])

    def get_group_names(self):
        group_names = self.data[group_id_column].unique()
        return group_names

    def count(self):
        """
        Count the number of observations in each group.

        :return: A Series containing in index the names of the group and as value the number of observation in the group
        :rtype: Pandas Series

        """
        return self.data.groupby(group_id_column).size()
