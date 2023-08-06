from unittest import TestCase
import pandas as pd
import numpy as np

from statisfaction import read_pandas
from statisfaction.utils.bucket import bucket


class TestBucket(TestCase):

    def build_example(self):
        data = pd.concat([
            pd.Series(np.arange(1000)).rename('observation_id'),
            pd.Series(np.concatenate([np.zeros(300), np.ones(700)])).rename('group_id'),
            pd.Series(np.zeros(1000)).rename('value')
        ], axis=1)
        return read_pandas(data)

    def test_too_big_observation_size(self):
        observations = self.build_example()
        with self.assertRaises(ValueError):
            bucket(observations, 16)

    def test_right_size_group_inequality(self):
        observations = self.build_example()
        self.assertTrue(len(bucket(observations, 15, group_equality=False).data) == 66)

    def test_right_size_group_equality(self):
        observations = self.build_example()
        self.assertTrue(len(bucket(observations, 15, group_equality=True).data) == 40)

    def test_granularity_composition(self):
        observations = self.build_example()
        self.assertTrue(bucket(bucket(observations, 2), 3).granularity == 6)
