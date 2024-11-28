import unittest
import itertools
import ir_measures
from ir_measures import *


class BaseMeasureTest(unittest.TestCase):
	def assertMetrics(self, a, b, places=4, not_equal=False):
		a = sorted(a)
		b = sorted(b)
		self.assertEqual(len(a), len(b))
		for m0, m1 in zip(a, b):
			self.assertEqual(m0.query_id, m1.query_id)
			self.assertEqual(m0.measure, m1.measure)
			if not_equal:
				self.assertNotAlmostEqual(m0.value, m1.value)
			else:
				self.assertAlmostEqual(m0.value, m1.value, places=places)
