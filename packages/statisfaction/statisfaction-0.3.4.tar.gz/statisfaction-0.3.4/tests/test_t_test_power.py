from unittest import TestCase
import pandas as pd
import numpy as np

from statisfaction import read_pandas
from statisfaction.duration._ttest import standard_deviation_bernoulli
from statisfaction.duration import t_test_power_from_aggregates
from statisfaction.duration import t_test_power_from_observations

t_test_power_from_observations.__test__ = False
t_test_power_from_aggregates.__test__ = False

class TestTTestPower(TestCase):
    """
    Module tested: duration.ttest.py
    >> Functions tested:
    a. statisfaction.duration.standard_deviation_bernoulli
    b. statisfaction.duration.t_test_power_from_aggregates
    c. statisfaction.duration.t_test_power_from_observations

    The dataset used in the test comes from https://www.evanmiller.org/ab-testing/sample-size.html
    conversion rate = 20%
    mde = 5% (absolute)
    sample size = 2060 (= 1,030 * 2)
    (alpha = 5%)
    (power = 80%)
    (standard deviation = sqrt( 0.2 * (1-0.2) ) = 0.4 > this is a Bernoulli distribution)
    """

    #TODO: set up test with share_in_control_group <> 0.5
    #> How to find/build data for such test? I haven't found the possibility to set share_in_control_group <> 0.5 (while controlling the other parameters) online
    #In particular, we would like to test one dataset with share_in_control_group <> 0.5 and missing in the input list,
    #and check the output of t_test_power_from_aggregates and t_test_power_from_observations

    def test_standard_deviation_bernoulli(self):
        std = standard_deviation_bernoulli(0.2)
        self.assertEqual(std,0.4)


    # Test t_test_power_from_aggregates

    def test_missing_mde(self):
        res = t_test_power_from_aggregates(control_standard_deviation = 0.4,
                                           control_mean = 0.2,
                                           minimum_detectable_effect = None,
                                           sample_size = 2060,
                                           share_in_control_group = 0.5)
        self.assertTrue(0.95 <= res['minimum_detectable_effect']/0.05 <= 1.05) # we tolerate a relative +/-5% variation

    def test_missing_mss(self):
        res = t_test_power_from_aggregates(control_standard_deviation = 0.4,
                                           control_mean = 0.2,
                                           minimum_detectable_effect = 0.05,
                                           sample_size = None,
                                           share_in_control_group = 0.5)
        self.assertTrue(0.95 <= res['sample_size']/2060 <= 1.05) # we tolerate a relative +/-5% variation

    def test_missing_scg(self):
        res = t_test_power_from_aggregates(control_standard_deviation = 0.4,
                                           control_mean = 0.2,
                                           minimum_detectable_effect = 0.05,
                                           sample_size = 2060,
                                           share_in_control_group = None)
        self.assertTrue(0.95 <= res['share_in_control_group']/0.5 <= 1.05) # we tolerate a relative +/-5% variation


    # Test t_test_power_from_observations

    def build_observations(self):
        data = pd.concat([
            pd.Series(np.arange(1000)).rename('observation_id'),
            pd.Series(np.concatenate([np.zeros(500), np.ones(500)])).rename('group_id'),
            pd.Series(np.concatenate([np.ones(100), np.zeros(400), np.ones(125), np.zeros(375)])).rename('value'),
        ], axis=1)
        return read_pandas(data, value_cols=['value'])
