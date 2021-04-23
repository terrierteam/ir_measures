import unittest
import itertools
import ir_measures
from ir_measures import AP, P, nDCG, NumRel, NumRelRet, Bpref, NumQ, RR, Rprec, NumRet, IPrec

class TestConvertTrecName(unittest.TestCase):

    def test_convert_trec_name(self):
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
            'official': [P@5, P@10, P@15, P@20, P@30, P@100, P@200, P@500, P@1000, Rprec, Bpref, IPrec@0.0, IPrec@0.1, IPrec@0.2, IPrec@0.3, IPrec@0.4, IPrec@0.5, IPrec@0.6, IPrec@0.7, IPrec@0.8, IPrec@0.9, IPrec@1.0, AP, NumQ, NumRel, NumRelRet, NumRet, RR],
        }
        for case in cases:
            with self.subTest(case):
                self.assertEqual(ir_measures.convert_trec_name(case), cases[case])


if __name__ == '__main__':
    unittest.main()
