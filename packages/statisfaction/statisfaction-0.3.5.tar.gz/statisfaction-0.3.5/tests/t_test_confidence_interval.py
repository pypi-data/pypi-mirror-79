from unittest import TestCase
import pandas as pd
import numpy as np

from statisfaction import read_pandas
from statisfaction.univariate import uplift_t_confidence_interval_from_aggregates
from statisfaction.utils.input import get_value_column_from_univariate


class TestTTestConfidenceInterval(TestCase):
    """
    Module tested: univariate.ttest.py
    >> Functions tested:
    a. statisfaction.univariate.uplift_t_confidence_interval_from_aggregates

    The goal is to verify the two modes of computation of CIs: with pooled variance or unequal variance.
    """

    def generate_dataset(self):
        np.random.seed(42)
        n = 100
        df = pd.DataFrame()
        df['observation_id'] = np.arange(n)
        df['group_id'] = np.where(np.random.rand(n) <= 0.3, 'control', 'treatment')
        df['value'] = np.where(df['group_id'] == 'treatment', 0.0855, 0.0) + np.random.rand(n)
        return read_pandas(df)

    def test_ttest_confidence_interval_equal_variance(self):

        # truth values come from this library. Maybe use it all the way in the function?
        # import statsmodels.stats.api as sms
        #
        # cm = sms.CompareMeans(sms.DescrStatsW(t_data), sms.DescrStatsW(c_data))
        # lower_bound, upper_bound = cm.tconfint_diff(usevar='pooled')

        observations = self.generate_dataset()

        value_column = get_value_column_from_univariate(observations)

        c_data = observations._get_series('control', value_column)
        t_data = observations._get_series('treatment', value_column)

        treatment_group_mean = t_data.mean()
        control_group_mean = c_data.mean()
        treatment_group_std = t_data.std()
        control_group_std = c_data.std()
        treatment_group_size = len(t_data)
        control_group_size = len(c_data)

        d = uplift_t_confidence_interval_from_aggregates(
            control_group_size, treatment_group_size,
            control_group_mean, treatment_group_mean,
            control_group_std, treatment_group_std,
            alpha=0.05, equal_variance=True
        )

        self.assertAlmostEqual(d['lower_bound'], -0.030775192541087418, places=7)
        self.assertAlmostEqual(d['upper_bound'], 0.21603918698314162, places=7)

    def test_ttest_confidence_interval_unequal_variance(self):

        # truth values come from this library. Maybe use it all the way in the function?
        # import statsmodels.stats.api as sms
        #
        # cm = sms.CompareMeans(sms.DescrStatsW(t_data), sms.DescrStatsW(c_data))
        # lower_bound, upper_bound = cm.tconfint_diff(usevar='unequal')

        observations = self.generate_dataset()

        value_column = get_value_column_from_univariate(observations)

        c_data = observations._get_series('control', value_column)
        t_data = observations._get_series('treatment', value_column)

        treatment_group_mean = t_data.mean()
        control_group_mean = c_data.mean()
        treatment_group_std = t_data.std()
        control_group_std = c_data.std()
        treatment_group_size = len(t_data)
        control_group_size = len(c_data)

        d = uplift_t_confidence_interval_from_aggregates(
            control_group_size, treatment_group_size,
            control_group_mean, treatment_group_mean,
            control_group_std, treatment_group_std,
            alpha=0.05, equal_variance=False
        )

        self.assertAlmostEqual(d['lower_bound'], -0.03195483287601002, places=7)
        self.assertAlmostEqual(d['upper_bound'], 0.21721882731806424, places=7)
