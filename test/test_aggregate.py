import unittest
import itertools
import ir_measures


class TestMeasures(unittest.TestCase):

    def test_P(self):
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
1 0 D0 5 0.1 run
'''))
        measure = ir_measures.P@5
        result = measure.calc_aggregate(qrels, run)
        self.assertEqual(result, 0.5)


if __name__ == '__main__':
    unittest.main()
