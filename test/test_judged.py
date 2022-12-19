import unittest
import ir_measures
from ir_measures.measures import Judged


class TestMeasures(unittest.TestCase):

    def test_judged(self):
        qrels = list(ir_measures.read_trec_qrels('''
0 0 D0 0
0 0 D1 1
0 0 D2 1
0 0 D3 2
0 0 D4 0
1 0 D0 1
1 0 D3 2
1 0 D5 2
'''))
        run = list(ir_measures.read_trec_run('''
0 0 D0 1 0.8 run
0 0 D2 2 0.7 run
0 0 D1 3 0.3 run
0 0 D3 4 0.4 run
0 0 D4 5 0.1 run
1 0 D1 1 0.8 run
1 0 D3 2 0.7 run
1 0 D4 3 0.3 run
1 0 D2 4 0.4 run
'''))
        provider = ir_measures.judged

        expected_results = [
            [Judged, [('0', 1.0), ('1', 1.0 / 4.0)]],
            [Judged(cutoff=1000), [('0', 1.0), ('1', 1.0 / 4.0)]],
            [Judged(cutoff=10), [('0', 1.0), ('1', 1.0 / 4.0)]],
            [Judged(cutoff=3), [('0', 1.0), ('1', 1.0 / 3.0)]],
            [Judged(cutoff=1), [('0', 1.0), ('1', 0.0)]],
        ]
        for measure, expected in expected_results:
            with self.subTest(measure=measure):
                self.assertTrue(provider.supports(measure))
                results = list(provider.iter_calc([measure], qrels, run))
                for result, (query_id, value) in zip(results, expected):
                    self.assertAlmostEqual(result.query_id, query_id, delta=0.0001)
                    self.assertAlmostEqual(result.value, value, delta=0.0001)


if __name__ == '__main__':
    unittest.main()
