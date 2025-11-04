import unittest
import itertools
import ir_measures
import pandas as pd

class TestRuntime(unittest.TestCase):

    def test_non_doc_qrels(self):
        # source: https://thecleverprogrammer.com/2022/07/27/longest-common-prefix-using-python/
        def longestCommonPrefix(strs):
            l = len(strs[0])
            for i in range(1, len(strs)):
                length = min(l, len(strs[i]))
                while length > 0 and strs[0][0:length] != strs[i][0:length]:
                    length = length - 1
                    if length == 0:
                        return 0
            return strs[0][0:length]

        LenMeasure = ir_measures.define_byquery(lambda qrels, run: len(run.iloc[0]["qanswer"]))
        LCSMeasure = ir_measures.define_byquery(lambda qrels, run: len(longestCommonPrefix(
            [qrels.iloc[0]["gold_answer"],
            run.iloc[0]["qanswer"]]
        )))
        
        prefix = 'professor proton mixed the '
        test_answer = prefix + 'reactants'
        gold_answer = prefix + 'chemicals'
        df_res = pd.DataFrame([['q1', test_answer]], columns=['query_id', 'qanswer'])
        df_gold = pd.DataFrame([['q1', gold_answer]], columns=['query_id', 'gold_answer'])
        measurements = ir_measures.iter_calc([LenMeasure, LCSMeasure], df_gold, df_res)
        for m in measurements:
            if m.measure == LenMeasure:
                self.assertEqual(len(test_answer), m.value)
            elif m.measure == LCSMeasure:
                self.assertEqual(len(prefix), m.value)
            else:
                raise Exception()

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

        # check empty lists
        result = list((MyS@2).iter_calc(qrels, []))
        result = list((MyS@2).iter_calc([], run))
        result = list((MyS@2).iter_calc([], []))

    def test_run_qrel_inputs(self):
        def a(qrels, run):
            ...
        def b(qrels, run):
            ...
        A = ir_measures.define(a, run_inputs=['query_id'], qrel_inputs=['query_id', 'doc_id', 'x'])
        B = ir_measures.define(b)
        provider = ir_measures.providers.RuntimeProvider()
        inputs = provider.run_inputs([A, B])
        self.assertEqual(set(inputs), {'query_id', 'doc_id', 'score'})
        inputs = provider.run_inputs([A])
        self.assertEqual(set(inputs), {'query_id'})
        inputs = provider.run_inputs([B])
        self.assertEqual(set(inputs), {'query_id', 'doc_id', 'score'})
        inputs = ir_measures.DefaultPipeline.run_inputs([A, B])
        self.assertEqual(set(inputs), {'query_id', 'doc_id', 'score'})
        inputs = ir_measures.DefaultPipeline.run_inputs([A])
        self.assertEqual(set(inputs), {'query_id'})
        inputs = ir_measures.DefaultPipeline.run_inputs([A, ir_measures.P@5])
        self.assertEqual(set(inputs), {'query_id', 'doc_id', 'score'})

        inputs = provider.qrel_inputs([A, B])
        self.assertEqual(set(inputs), {'query_id', 'doc_id', 'relevance', 'x'})
        inputs = provider.qrel_inputs([A])
        self.assertEqual(set(inputs), {'query_id', 'doc_id', 'x'})
        inputs = provider.qrel_inputs([B])
        self.assertEqual(set(inputs), {'query_id', 'doc_id', 'relevance'})
        inputs = ir_measures.DefaultPipeline.qrel_inputs([A, B])
        self.assertEqual(set(inputs), {'query_id', 'doc_id', 'relevance', 'x'})
        inputs = ir_measures.DefaultPipeline.qrel_inputs([A])
        self.assertEqual(set(inputs), {'query_id', 'doc_id', 'x'})
        inputs = ir_measures.DefaultPipeline.qrel_inputs([A, ir_measures.P@5])
        self.assertEqual(set(inputs), {'query_id', 'doc_id', 'relevance', 'x'})



if __name__ == '__main__':
    unittest.main()
