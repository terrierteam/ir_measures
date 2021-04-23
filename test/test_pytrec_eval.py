import unittest
import itertools
import ir_measures


class TestPytrecEval(unittest.TestCase):

    def test_NumRet(self):
        qrels = list(ir_measures.util.parse_trec_qrels('''
0 0 D0 0
0 0 D1 1
0 0 D2 1
0 0 D3 2
0 0 D4 0
1 0 D0 1
1 0 D3 2
1 0 D5 2
'''))
        run = list(ir_measures.util.parse_trec_run('''
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
        provider = ir_measures.providers.PytrecEvalProvider()
        measure = ir_measures.NumRet
        result = list(provider.iter_calc([measure], qrels, run))
        self.assertEqual(result[0].query_id, "0")
        self.assertEqual(result[0].value, 5)
        self.assertEqual(result[1].query_id, "1")
        self.assertEqual(result[1].value, 4)
        self.assertEqual(provider.calc_aggregate([measure], qrels, run)[measure], 9)

        measure = ir_measures.NumRet(rel=1)
        result = list(provider.iter_calc([measure], qrels, run))
        self.assertEqual(result[0].query_id, "0")
        self.assertEqual(result[0].value, 3)
        self.assertEqual(result[1].query_id, "1")
        self.assertEqual(result[1].value, 1)
        self.assertEqual(provider.calc_aggregate([measure], qrels, run)[measure], 4)

        measure = ir_measures.NumRet(rel=2)
        result = list(provider.iter_calc([measure], qrels, run))
        self.assertEqual(result[0].query_id, "0")
        self.assertEqual(result[0].value, 1)
        self.assertEqual(result[1].query_id, "1")
        self.assertEqual(result[1].value, 1)
        self.assertEqual(provider.calc_aggregate([measure], qrels, run)[measure], 2)

        measure = ir_measures.NumRet(rel=3)
        result = list(provider.iter_calc([measure], qrels, run))
        self.assertEqual(result[0].query_id, "0")
        self.assertEqual(result[0].value, 0)
        self.assertEqual(result[1].query_id, "1")
        self.assertEqual(result[1].value, 0)
        self.assertEqual(provider.calc_aggregate([measure], qrels, run)[measure], 0)

    def test_NumQ(self):
        qrels = list(ir_measures.util.parse_trec_qrels('''
0 0 D0 0
0 0 D1 1
0 0 D2 1
0 0 D3 2
0 0 D4 0
1 0 D0 1
1 0 D3 2
1 0 D5 2
'''))
        run = list(ir_measures.util.parse_trec_run('''
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
        provider = ir_measures.providers.PytrecEvalProvider()
        measure = ir_measures.NumQ
        result = list(provider.iter_calc([measure], qrels, run))
        self.assertEqual(result[0].query_id, "0")
        self.assertEqual(result[0].value, 1)
        self.assertEqual(result[1].query_id, "1")
        self.assertEqual(result[1].value, 1)
        self.assertEqual(provider.calc_aggregate([measure], qrels, run)[measure], 2)


if __name__ == '__main__':
    unittest.main()
