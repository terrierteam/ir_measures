import unittest
import itertools
import ir_measures


class TestRuntime(unittest.TestCase):

    def test_define_byquery(self):
        try:
            def my_p2(qrels, run):
                run = run.iloc[:2].merge(qrels, 'left', on=['doc_id'])
                return (run['relevance'] > 0).sum() / 2.
            def my_s2(qrels, run):
                run = run.iloc[:2].merge(qrels, 'left', on=['doc_id'])
                return 1. if (run['relevance'] > 0).sum() else 0.
            MyP2 = ir_measures.define_byquery('MyP2', my_p2)
            MyS2 = ir_measures.define_byquery('MyS2', my_s2)
            qrels = list(ir_measures.read_trec_qrels('''
0 0 D0 0
0 0 D1 1
0 0 D2 1
0 0 D3 2
0 0 D4 0
1 0 D0 1
1 0 D3 0
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
            result = list(MyP2.iter_calc(qrels, run))
            self.assertEqual(result[0].query_id, "0")
            self.assertEqual(result[0].value, 0.5)
            self.assertEqual(result[1].query_id, "1")
            self.assertEqual(result[1].value, 0.)
            self.assertEqual(MyP2.calc_aggregate(qrels, run), 0.25)

            result = list(MyS2.iter_calc(qrels, run))
            self.assertEqual(result[0].query_id, "0")
            self.assertEqual(result[0].value, 1.)
            self.assertEqual(result[1].query_id, "1")
            self.assertEqual(result[1].value, 0.)
            self.assertEqual(MyS2.calc_aggregate(qrels, run), 0.5)
        finally:
            del ir_measures.measures.registry['MyP2']
            del ir_measures.measures.registry['MyS2']

    def test_define(self):
        try:
            def my_p2(qrels, run):
                run = run.merge(qrels, 'left', on=['query_id', 'doc_id'])
                for qid, df in run.groupby('query_id'):
                    yield qid, (df.iloc[:2]['relevance'] > 0).sum() / 2.
            def my_s2(qrels, run):
                run = run.merge(qrels, 'left', on=['query_id', 'doc_id'])
                for qid, df in run.groupby('query_id'):
                    yield qid, 1. if (df.iloc[:2]['relevance'] > 0).sum() else 0.
            MyP2 = ir_measures.define('MyP2', my_p2)
            MyS2 = ir_measures.define('MyS2', my_s2)
            qrels = list(ir_measures.read_trec_qrels('''
0 0 D0 0
0 0 D1 1
0 0 D2 1
0 0 D3 2
0 0 D4 0
1 0 D0 1
1 0 D3 0
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
            result = list(MyP2.iter_calc(qrels, run))
            self.assertEqual(result[0].query_id, "0")
            self.assertEqual(result[0].value, 0.5)
            self.assertEqual(result[1].query_id, "1")
            self.assertEqual(result[1].value, 0.)
            self.assertEqual(MyP2.calc_aggregate(qrels, run), 0.25)

            result = list(MyS2.iter_calc(qrels, run))
            self.assertEqual(result[0].query_id, "0")
            self.assertEqual(result[0].value, 1.)
            self.assertEqual(result[1].query_id, "1")
            self.assertEqual(result[1].value, 0.)
            self.assertEqual(MyS2.calc_aggregate(qrels, run), 0.5)
        finally:
            del ir_measures.measures.registry['MyP2']
            del ir_measures.measures.registry['MyS2']


if __name__ == '__main__':
    unittest.main()
