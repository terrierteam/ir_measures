import pandas as pd
import unittest
import itertools
import ir_measures
from ir_measures import *
from pandas.testing import assert_frame_equal

class TestUtil(unittest.TestCase):

    def test_parse_trec_measure(self):
        cases = {
            'map': [AP],
            'P_5': [P@5],
            'P_5,10': [P@5, P@10],
            'P.5': [P@5],
            'P.5,10': [P@5, P@10],
            'P': [P@5, P@10, P@15, P@20, P@30, P@100, P@200, P@500, P@1000],
            'ndcg': [nDCG],
            'ndcg_cut.10': [nDCG@10],
            'ndcg_cut.5,10': [nDCG@5, nDCG@10],
            'ndcg_cut_10': [nDCG@10],
            'ndcg_cut_5,10': [nDCG@5, nDCG@10],
            'ndcg_cut': [nDCG@5, nDCG@10, nDCG@15, nDCG@20, nDCG@30, nDCG@100, nDCG@200, nDCG@500, nDCG@1000],
            'set_P': [SetP],
            'set_recall': [SetR],
            'set_F': [SetF],
            'set_relative_P': [SetRelP],
            'set_map': [SetAP],
            'set_F.1.0,0.5,2.4': [SetF, SetF(beta=0.5), SetF(beta=2.4)],
            'official': [P@5, P@10, P@15, P@20, P@30, P@100, P@200, P@500, P@1000, Rprec, Bpref, IPrec@0.0, IPrec@0.1, IPrec@0.2, IPrec@0.3, IPrec@0.4, IPrec@0.5, IPrec@0.6, IPrec@0.7, IPrec@0.8, IPrec@0.9, IPrec@1.0, AP, NumQ, NumRel, NumRelRet, NumRet, RR],
        }
        for case in cases:
            with self.subTest(case):
                self.assertEqual(ir_measures.parse_trec_measure(case), cases[case])

    def test_parse_measure(self):
        tests = {
            'AP': AP,
            AP: AP,
            'MAP': AP,
            MAP: MAP,
            'P@10': P@10,
            P@10: P@10,
            'nDCG@10': nDCG@10,
            'P(rel=2)@10': P(rel=2)@10,
            'nDCG(dcg="exp-log2")@10': nDCG(dcg='exp-log2')@10,
            'nDCG(dcg="exp-log2", cutoff=20)@10': nDCG(dcg='exp-log2')@10,
            'nDCG(dcg="exp-log2", cutoff=20)': nDCG(dcg='exp-log2')@20,
            'IPrec@0.2': IPrec@0.2,
            'IPrec(rel=2)@0.2': IPrec(rel=2)@0.2,
            'IPrec(rel=2, recall=0.4)@0.2': IPrec(rel=2)@0.2,
            'IPrec(rel=2, recall=0.4)': IPrec(rel=2)@0.4,
            IPrec(rel=2)@0.4: IPrec(rel=2)@0.4,
        }
        for key, value in tests.items():
            with self.subTest(key):
                self.assertEqual(ir_measures.parse_measure(key), value)

    def test_qrels_converter(self):
        qrels_list = [
            ir_measures.Qrel('1', 'A', 1),
            ir_measures.Qrel('1', 'B', 0),
            ir_measures.Qrel('2', 'A', 0),
            ir_measures.Qrel('2', 'C', 1),
        ]
        qrels_df = pd.DataFrame(qrels_list)
        qrels_df_noit = qrels_df.drop(columns='iteration')
        qrels_dict = {
            '1': {'A': 1, 'B': 0},
            '2': {'A': 0, 'C': 1}
        }
        sources = {
            'qrels_nt_list': lambda: qrels_list,
            'qrels_nt_iter': lambda: iter(qrels_list),
            'qrels_df': lambda: qrels_df,
            'qrels_df_noit': lambda: qrels_df_noit,
            'qrels_dict': lambda: qrels_dict
        }
        for n, fn in sources.items():
            with self.subTest(n):
                self.assertEqual(ir_measures.util.QrelsConverter(fn()).as_dict_of_dict(), qrels_dict)
                self.assertEqual(list(ir_measures.util.QrelsConverter(fn()).as_namedtuple_iter()), qrels_list)
                assert_frame_equal(ir_measures.util.QrelsConverter(fn()).as_pd_dataframe(), qrels_df)

        bad_df = pd.DataFrame([
            {'query_id': '0', 'docno': 'A', 'relevance': 1}
        ])
        with self.assertRaises(ValueError) as context:
            ir_measures.util.QrelsConverter(bad_df).as_dict_of_dict()

        self.assertEqual(context.exception.args[0], "unknown qrels format: DataFrame missing columns: ['doc_id'] (found ['query_id', 'docno', 'relevance'])")

        with self.assertRaises(ValueError) as context:
            ir_measures.util.QrelsConverter(object()).as_dict_of_dict()

        self.assertEqual(context.exception.args[0], "unknown qrels format: unexpected format; please provide either: (1) an iterable of namedtuples (fields ('query_id', 'doc_id', 'relevance'), e.g., from ir_measures.Qrel); (2) a pandas DataFrame with columns ('query_id', 'doc_id', 'relevance'); or (3) a dict-of-dict")

    def test_run_converter(self):
        run_list = [
            ir_measures.ScoredDoc('1', 'A', 1.2),
            ir_measures.ScoredDoc('1', 'B', 0.9),
            ir_measures.ScoredDoc('2', 'A', 3.5),
            ir_measures.ScoredDoc('2', 'C', 0.3),
        ]
        run_df = pd.DataFrame(run_list)
        run_dict = {
            '1': {'A': 1.2, 'B': 0.9},
            '2': {'A': 3.5, 'C': 0.3}
        }
        sources = {
            'run_nt_list': lambda: run_list,
            'run_nt_iter': lambda: iter(run_list),
            'run_df': lambda: run_df,
            'run_dict': lambda: run_dict
        }
        for n, fn in sources.items():
            with self.subTest(n):
                self.assertEqual(ir_measures.util.RunConverter(fn()).as_dict_of_dict(), run_dict)
                self.assertEqual(list(ir_measures.util.RunConverter(fn()).as_namedtuple_iter()), run_list)
                assert_frame_equal(ir_measures.util.RunConverter(fn()).as_pd_dataframe(), run_df)

        bad_df = pd.DataFrame([
            {'query_id': '0', 'docno': 'A', 'score': 1.2}
        ])
        with self.assertRaises(ValueError) as context:
            ir_measures.util.RunConverter(bad_df).as_dict_of_dict()

        self.assertEqual(context.exception.args[0], "unknown run format: DataFrame missing columns: ['doc_id'] (found ['query_id', 'docno', 'score'])")

        with self.assertRaises(ValueError) as context:
            ir_measures.util.RunConverter(object()).as_dict_of_dict()

        self.assertEqual(context.exception.args[0], "unknown run format: unexpected format; please provide either: (1) an iterable of namedtuples (fields ('query_id', 'doc_id', 'score'), e.g., from ir_measures.ScoredDoc); (2) a pandas DataFrame with columns ('query_id', 'doc_id', 'score'); or (3) a dict-of-dict")


if __name__ == '__main__':
    unittest.main()
