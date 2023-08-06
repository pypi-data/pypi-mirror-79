from statisfaction.duration import peeking_alpha_boundaries
from unittest import TestCase


class TestPeeking(TestCase):
	"""
	Module tested: duration.peeking.py
	>> Functions tested:
	statisfaction.duration.peeking_alpha_boundaries

	We will test that the function returns the right alpha boundaries values (according to this cource: https://onlinecourses.science.psu.edu/stat509/node/80)
	For the test we will test for 3 peekings, for obrien method
	"""
	def test_obrien(self):
		ref = [0.0006, 0.0151, 0.0471]
		alpha_df = peeking_alpha_boundaries(alpha=0.05, nb_peek=3, method='obrien')
		res = list(alpha_df.alpha_boundary)
		self.assertEqual(res,ref)

