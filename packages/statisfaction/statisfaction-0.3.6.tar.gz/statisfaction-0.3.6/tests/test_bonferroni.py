from unittest import TestCase
import pandas as pd
import numpy as np

from statisfaction import read_pandas
from statisfaction.multivariate import multivariate_bonferroni
from statisfaction.univariate import t_test_from_observations
from statisfaction.duration import t_test_power_from_observations


t_test_from_observations.__test__ = False
t_test_power_from_observations.__test__ = False


class TestBonferroni(TestCase):

    def build_example(self):
        data = pd.concat([
            pd.Series(np.arange(1000)).rename('observation_id'),
            pd.Series(np.concatenate([np.zeros(300), np.ones(700)])).rename('group_id'),
            pd.Series(np.random.randn(1000)).rename('value0'),
            pd.Series(np.random.randn(1000)).rename('value1'),
            pd.Series(np.random.randn(1000)).rename('value2')
        ], axis=1)
        return read_pandas(data, value_cols=["value0", "value1", "value2"])

    def test_ttest(self):
        observations = self.build_example()
        res = multivariate_bonferroni(observations, t_test_from_observations, alpha=0.09, control_group=0, treatment_group=1)
        keys = res.keys()
        self.assertEqual(len(keys),3)
        self.assertTrue("value0" in keys)
        self.assertTrue("value1" in keys)
        self.assertTrue("value2" in keys)

    def test_ttest_power(self):
        observations = self.build_example()
        res = multivariate_bonferroni(observations, t_test_power_from_observations,
            alpha=0.09, control_group=0, treatment_group=1,
            minimum_detectable_effect=0.1,
            share_in_control_group='from_ratio_param',
            ratio=0.5)
        keys = res.keys()
        self.assertEqual(len(keys),3)
        self.assertTrue("value0" in keys)
        self.assertTrue("value1" in keys)
        self.assertTrue("value2" in keys)
        self.assertEqual(res['value0']['alpha'], 0.03)
        self.assertEqual(res['value1']['alpha'], 0.03)
        self.assertEqual(res['value2']['alpha'], 0.03)
