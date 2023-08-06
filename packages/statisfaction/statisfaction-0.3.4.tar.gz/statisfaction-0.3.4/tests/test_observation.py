from unittest import TestCase
import pandas as pd
import numpy as np

from statisfaction import read_pandas
from statisfaction.utils import bucket


class TestObservation(TestCase):

    def build_example(self):
        data = pd.concat([
            pd.Series(np.arange(1000)).rename('observation_id'),
            pd.Series(np.concatenate([np.zeros(300), np.ones(700)])).rename('group_id'),
            pd.Series(np.zeros(1000)).rename('value')
        ], axis=1)
        return read_pandas(data)

    def test_right_count(self):
        observations = self.build_example()
        count = observations.count()
        self.assertEqual(count[0], 300)
        self.assertEqual(count[1], 700)
