import unittest
import itertools
import ir_measures


class TestRuntime(unittest.TestCase):

    def test_define_byquery(self):
        def my_p(qrels, run):
            run = run.merge(qrels, 'left', on=['doc_id'])
            return (run['relevance'] > 0).sum() / len(run)
        def my_s(qrels, run):
            run = run.merge(qrels, 'left', on=['doc_id'])
            return 1. if (run['relevance'] > 0).sum() else 0.
        MyP = ir_measures.define_byquery(my_p)
        MyS = ir_measures.define_byquery(my_s)
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

        result = list((MyP@1).iter_calc(qrels, run))
        self.assertEqual(result[0].query_id, "0")
        self.assertEqual(result[0].value, 0.)
        self.assertEqual(result[1].query_id, "1")
        self.assertEqual(result[1].value, 0.)
        self.assertEqual((MyP@1).calc_aggregate(qrels, run), 0.0)

        result = list((MyP@2).iter_calc(qrels, run))
        self.assertEqual(result[0].query_id, "0")
        self.assertEqual(result[0].value, 0.5)
        self.assertEqual(result[1].query_id, "1")
        self.assertEqual(result[1].value, 0.)
        self.assertEqual((MyP@2).calc_aggregate(qrels, run), 0.25)

        result = list((MyP@3).iter_calc(qrels, run))
        self.assertEqual(result[0].query_id, "0")
        self.assertEqual(result[0].value, 0.6666666666666666)
        self.assertEqual(result[1].query_id, "1")
        self.assertEqual(result[1].value, 0.)
        self.assertEqual((MyP@3).calc_aggregate(qrels, run), 0.3333333333333333)

        result = list((MyS@2).iter_calc(qrels, run))
        self.assertEqual(result[0].query_id, "0")
        self.assertEqual(result[0].value, 1.)
        self.assertEqual(result[1].query_id, "1")
        self.assertEqual(result[1].value, 0.)
        self.assertEqual((MyS@2).calc_aggregate(qrels, run), 0.5)

    def test_define(self):
        def my_p(qrels, run):
            run = run.merge(qrels, 'left', on=['query_id', 'doc_id'])
            for qid, df in run.groupby('query_id'):
                yield qid, (df['relevance'] > 0).sum() / len(df)
        def my_s(qrels, run):
            run = run.merge(qrels, 'left', on=['query_id', 'doc_id'])
            for qid, df in run.groupby('query_id'):
                yield qid, 1. if (df['relevance'] > 0).sum() else 0.
        MyP = ir_measures.define(my_p)
        MyS = ir_measures.define(my_s)
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
        result = list((MyP@1).iter_calc(qrels, run))
        self.assertEqual(result[0].query_id, "0")
        self.assertEqual(result[0].value, 0.)
        self.assertEqual(result[1].query_id, "1")
        self.assertEqual(result[1].value, 0.)
        self.assertEqual((MyP@1).calc_aggregate(qrels, run), 0.0)

        result = list((MyP@2).iter_calc(qrels, run))
        self.assertEqual(result[0].query_id, "0")
        self.assertEqual(result[0].value, 0.5)
        self.assertEqual(result[1].query_id, "1")
        self.assertEqual(result[1].value, 0.)
        self.assertEqual((MyP@2).calc_aggregate(qrels, run), 0.25)

        result = list((MyP@3).iter_calc(qrels, run))
        self.assertEqual(result[0].query_id, "0")
        self.assertEqual(result[0].value, 0.6666666666666666)
        self.assertEqual(result[1].query_id, "1")
        self.assertEqual(result[1].value, 0.)
        self.assertEqual((MyP@3).calc_aggregate(qrels, run), 0.3333333333333333)

        result = list((MyS@2).iter_calc(qrels, run))
        self.assertEqual(result[0].query_id, "0")
        self.assertEqual(result[0].value, 1.)
        self.assertEqual(result[1].query_id, "1")
        self.assertEqual(result[1].value, 0.)
        self.assertEqual((MyS@2).calc_aggregate(qrels, run), 0.5)


if __name__ == '__main__':
    unittest.main()
