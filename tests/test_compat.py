import os
import unittest
import itertools
import ir_measures
from ir_measures import *


class TestCompat(unittest.TestCase):

    def test_measures(self):
        qrels = list(ir_measures.read_trec_qrels(os.path.join(os.path.dirname(__file__), 'compat.qrels')))
        run = list(ir_measures.read_trec_run(os.path.join(os.path.dirname(__file__), 'compat.run')))
        provider = ir_measures.compat
        # based on a manual execution of https://github.com/claclark/Compatibility
        expected_results = [
            [Compat(p=0.95), [('31_1', 0.51779512165509), ('31_2', 0.018400100569017922)]],
            [Compat(p=0.9), [('31_1', 0.3761334522946854), ('31_2', 0.004344079941789211)]],
            [Compat(p=0.8), [('31_1', 0.16723008845234535), ('31_2', 0.00022806427320561776)]],
        ]
        for measure, expected in expected_results:
            with self.subTest(measure=measure):
                self.assertTrue(provider.supports(measure))
                results = list(provider.iter_calc([measure], qrels, run))
                for result, (query_id, value) in zip(results, expected):
                    self.assertAlmostEqual(result.query_id, query_id, delta=1e-9)
                    self.assertAlmostEqual(result.value, value, delta=1e-9)
        self.assertAlmostEqual(provider.calc_aggregate([Compat(p=0.95)], qrels, run)[Compat(p=0.95)], 0.268097611, delta=1e-9)


if __name__ == '__main__':
    unittest.main()
