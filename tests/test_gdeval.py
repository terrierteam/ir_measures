import unittest
import itertools
import ir_measures


class TestPytrecEval(unittest.TestCase):

    def test_nDCG(self):
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
        provider = ir_measures.gdeval
        measure = ir_measures.nDCG@20
        result = list(provider.iter_calc([measure], qrels, run))
        self.assertEqual(result[0].query_id, "0")
        self.assertEqual(result[0].value, 0.6201)
        self.assertEqual(result[1].query_id, "1")
        self.assertEqual(result[1].value, 0.35099)
        self.assertEqual(provider.calc_aggregate([measure], qrels, run)[measure], 0.485545)
        self.assertEqual(provider.evaluator([measure], qrels).calc_aggregate(run)[measure], 0.485545)

        measure = ir_measures.nDCG@2
        result = list(provider.iter_calc([measure], qrels, run))
        self.assertEqual(result[0].query_id, "0")
        self.assertEqual(result[0].value, 0.17377)
        self.assertEqual(result[1].query_id, "1")
        self.assertEqual(result[1].value, 0.38685)
        self.assertEqual(provider.calc_aggregate([measure], qrels, run)[measure], 0.28031)

        ev = provider.evaluator([ir_measures.nDCG@20, ir_measures.nDCG@2], qrels)
        res = ev.calc_aggregate(run)
        self.assertEqual(res[ir_measures.nDCG@20], 0.485545)
        self.assertEqual(res[ir_measures.nDCG@2], 0.28031)
        res = ev.calc_aggregate(run)
        self.assertEqual(res[ir_measures.nDCG@20], 0.485545)
        self.assertEqual(res[ir_measures.nDCG@2], 0.28031)

    def test_ERR(self):
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
        provider = ir_measures.gdeval
        measure = ir_measures.ERR@20
        result = list(provider.iter_calc([measure], qrels, run))
        self.assertEqual(result[0].query_id, "0")
        self.assertEqual(result[0].value, 0.10175)
        self.assertEqual(result[1].query_id, "1")
        self.assertEqual(result[1].value, 0.09375)
        self.assertEqual(provider.calc_aggregate([measure], qrels, run)[measure], 0.09775)

        measure = ir_measures.ERR@2
        result = list(provider.iter_calc([measure], qrels, run))
        self.assertEqual(result[0].query_id, "0")
        self.assertEqual(result[0].value, 0.03125)
        self.assertEqual(result[1].query_id, "1")
        self.assertEqual(result[1].value, 0.09375)
        self.assertEqual(provider.calc_aggregate([measure], qrels, run)[measure], 0.0625)

    def test_non_numeric_qids(self):
        qrels = {'Q0': {'D0': 0, 'D1': 1}, 'Q1': {'D0': 0, 'D3': 2}}
        run = {'Q0': {'D0': 1.2, 'D1': 1.0}, 'Q1': {'D0': 2.4, 'D3': 3.6}}
        measure = ir_measures.ERR@10
        with self.assertWarns(UserWarning):
            result = list(ir_measures.gdeval.iter_calc([measure], qrels, run))
        self.assertEqual([(r.query_id, r.value) for r in result], [('Q0', 0.03125), ('Q1', 0.1875)])

    def test_max_judgment(self):
        qrels = {'Q0': {'D0': 0, 'D1': 5}}
        run = {'Q0': {'D0': 1.2, 'D1': 1.0}}
        with self.assertRaises(ValueError):
            ir_measures.gdeval.calc_aggregate([ir_measures.ERR@10], qrels, run)


if __name__ == '__main__':
    unittest.main()
