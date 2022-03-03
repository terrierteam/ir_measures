from itertools import zip_longest
import unittest
import ir_measures
from ir_measures.measures import Accuracy

class TestMeasures(unittest.TestCase):

    def test_accuracy(self):
        qrels = list(ir_measures.read_trec_qrels('''
0 0 C0_1 0
0 0 B0_1 1
0 0 A0_1 2

1 0 A1_1 2
1 0 A1_2 2
1 0 B1_1 1
1 0 C1_2 0

2 0 B1_1 1
'''))
        run = list(ir_measures.read_trec_run('''
0 0 C0_1 1 0.4 run
0 0 A0_1 2 0.3 run
0 0 C0_2 3 0.2 run
0 0 C0_3 4 0.1 run

1 0 C1_1 1 0.8 run
1 0 A1_1 2 0.7 run
1 0 C1_2 3 0.6 run
1 0 B1_1 4 0.5 run
1 0 C1_3 5 0.4 run

2 0 B1_1 2 0.2 run 
2 0 C1_1 3 0.1 run
'''))
        provider = ir_measures.accuracy

        accuracy_1 = Accuracy(rel=1)
        results_1 = [('0', 2./3.), ('1', .5 * (2/3. + 1./3)), ('2', 1.)]
        expected_results = [
            [accuracy_1, results_1],
            [Accuracy(rel=2), [('0', 2./3), ('1', 0.75)]],
        ]
        for measure, expected in expected_results:
            with self.subTest(measure=measure):
                self.assertTrue(provider.supports(measure))
                results = list(provider.iter_calc([measure], qrels, run))
                self.assertEqual(len(results), len(expected), "result lists length differ")

                for result, (query_id, value) in zip(results, expected):
                    self.assertEqual(result.query_id, query_id)
                    self.assertAlmostEqual(result.value, value, delta=1e-9, msg=f"for query {query_id}")

        expected = sum(value for _, value in results_1) / len(results_1)
        self.assertAlmostEqual(provider.calc_aggregate([accuracy_1], qrels, run)[accuracy_1], expected, delta=1e-9)


if __name__ == '__main__':
    unittest.main()
