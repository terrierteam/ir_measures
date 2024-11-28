import unittest
import itertools
import ir_measures
from ir_measures import Metric


class TestRanx(unittest.TestCase):

    def test_P(self):
        qrels = list(ir_measures.read_trec_qrels('''
0 0 D0 0
0 0 D1 1
0 0 D2 1
0 0 D3 2
0 0 D4 0
'''))
        run = list(ir_measures.read_trec_run('''
0 0 D0 1 0.8 run
0 0 D2 2 0.7 run
0 0 D1 3 0.3 run
0 0 D3 4 0.4 run
0 0 D4 5 0.1 run
'''))
        measure = ir_measures.P@5
        result = list(ir_measures.ranx.iter_calc([measure], qrels, run))
        self.assertEqual(result[0], Metric('0', measure, 0.6))
        measure = ir_measures.P(rel=2)@5
        result = list(ir_measures.ranx.iter_calc([measure], qrels, run))
        self.assertEqual(result[0], Metric('0', measure, 0.2))

        measure = ir_measures.SetP
        result = list(ir_measures.ranx.iter_calc([measure], qrels, run))
        self.assertEqual(result[0], Metric('0', measure, 0.6))
        measure = ir_measures.SetP(rel=2)@5
        result = list(ir_measures.ranx.iter_calc([measure], qrels, run))
        self.assertEqual(result[0], Metric('0', measure, 0.2))

        measure = ir_measures.R@5
        result = list(ir_measures.ranx.iter_calc([measure], qrels, run))
        self.assertEqual(result[0], Metric('0', measure, 1.0))
        measure = ir_measures.R(rel=2)@5
        result = list(ir_measures.ranx.iter_calc([measure], qrels, run))
        self.assertEqual(result[0], Metric('0', measure, 1.0))
        measure = ir_measures.R@2
        result = list(ir_measures.ranx.iter_calc([measure], qrels, run))
        self.assertEqual(result[0], Metric('0', measure, 0.3333333333333333))
        measure = ir_measures.R(rel=2)@2
        result = list(ir_measures.ranx.iter_calc([measure], qrels, run))
        self.assertEqual(result[0], Metric('0', measure, 0.0))

        measure = ir_measures.SetR
        result = list(ir_measures.ranx.iter_calc([measure], qrels, run))
        self.assertEqual(result[0], Metric('0', measure, 1.0))
        measure = ir_measures.SetR(rel=2)@5
        result = list(ir_measures.ranx.iter_calc([measure], qrels, run))
        self.assertEqual(result[0], Metric('0', measure, 1.0))

        measure = ir_measures.RR
        result = list(ir_measures.ranx.iter_calc([measure], qrels, run))
        self.assertEqual(result[0], Metric('0', measure, 0.5))
        measure = ir_measures.RR(rel=2)
        result = list(ir_measures.ranx.iter_calc([measure], qrels, run))
        self.assertEqual(result[0], Metric('0', measure, 0.3333333333333333))
        measure = ir_measures.RR@10
        result = list(ir_measures.ranx.iter_calc([measure], qrels, run))
        self.assertEqual(result[0], Metric('0', measure, 0.5))
        measure = ir_measures.RR(rel=2)@10
        result = list(ir_measures.ranx.iter_calc([measure], qrels, run))
        self.assertEqual(result[0], Metric('0', measure, 0.3333333333333333))
        measure = ir_measures.RR@2
        result = list(ir_measures.ranx.iter_calc([measure], qrels, run))
        self.assertEqual(result[0], Metric('0', measure, 0.5))
        measure = ir_measures.RR(rel=2)@2
        result = list(ir_measures.ranx.iter_calc([measure], qrels, run))
        self.assertEqual(result[0], Metric('0', measure, 0.))

        measure = ir_measures.AP
        result = list(ir_measures.ranx.iter_calc([measure], qrels, run))
        self.assertEqual(result[0], Metric('0', measure, 0.6388888888888888))
        measure = ir_measures.AP(rel=2)
        result = list(ir_measures.ranx.iter_calc([measure], qrels, run))
        self.assertEqual(result[0], Metric('0', measure, 0.3333333333333333))
        measure = ir_measures.AP@10
        result = list(ir_measures.ranx.iter_calc([measure], qrels, run))
        self.assertEqual(result[0], Metric('0', measure, 0.6388888888888888))
        measure = ir_measures.AP(rel=2)@10
        result = list(ir_measures.ranx.iter_calc([measure], qrels, run))
        self.assertEqual(result[0], Metric('0', measure, 0.3333333333333333))
        measure = ir_measures.AP@2
        result = list(ir_measures.ranx.iter_calc([measure], qrels, run))
        self.assertEqual(result[0], Metric('0', measure, 0.16666666666666666))
        measure = ir_measures.AP(rel=2)@2
        result = list(ir_measures.ranx.iter_calc([measure], qrels, run))
        self.assertEqual(result[0], Metric('0', measure, 0.0))

        measure = ir_measures.Success@10
        result = list(ir_measures.ranx.iter_calc([measure], qrels, run))
        self.assertEqual(result[0], Metric('0', measure, 1.))
        measure = ir_measures.Success(rel=2)@10
        result = list(ir_measures.ranx.iter_calc([measure], qrels, run))
        self.assertEqual(result[0], Metric('0', measure, 1.))
        measure = ir_measures.Success@2
        result = list(ir_measures.ranx.iter_calc([measure], qrels, run))
        self.assertEqual(result[0], Metric('0', measure, 1.))
        measure = ir_measures.Success(rel=2)@2
        result = list(ir_measures.ranx.iter_calc([measure], qrels, run))
        self.assertEqual(result[0], Metric('0', measure, 0.))

        measure = ir_measures.NumRet(rel=1)
        result = list(ir_measures.ranx.iter_calc([measure], qrels, run))
        self.assertEqual(result[0], Metric('0', measure, 3.))
        measure = ir_measures.NumRet(rel=2)
        result = list(ir_measures.ranx.iter_calc([measure], qrels, run))

        measure = ir_measures.nDCG
        result = list(ir_measures.ranx.iter_calc([measure], qrels, run))
        self.assertEqual(result[0], Metric('0', measure, 0.6584645692843067))
        measure = ir_measures.nDCG@5
        result = list(ir_measures.ranx.iter_calc([measure], qrels, run))
        self.assertEqual(result[0], Metric('0', measure, 0.6584645692843067))
        measure = ir_measures.nDCG@2
        result = list(ir_measures.ranx.iter_calc([measure], qrels, run))
        self.assertEqual(result[0], Metric('0', measure, 0.23981246656813146))

        measure = ir_measures.nDCG(dcg='exp-log2')
        result = list(ir_measures.ranx.iter_calc([measure], qrels, run))
        self.assertEqual(result[0], Metric('0', measure, 0.6201040599710453))
        measure = ir_measures.nDCG(dcg='exp-log2')@5
        result = list(ir_measures.ranx.iter_calc([measure], qrels, run))
        self.assertEqual(result[0], Metric('0', measure, 0.6201040599710453))
        measure = ir_measures.nDCG(dcg='exp-log2')@2
        result = list(ir_measures.ranx.iter_calc([measure], qrels, run))
        self.assertEqual(result[0], Metric('0', measure, 0.17376534287144002))

        measure = ir_measures.Rprec
        result = list(ir_measures.ranx.iter_calc([measure], qrels, run))
        self.assertEqual(result[0], Metric('0', measure, 0.6666666666666666))
        measure = ir_measures.Rprec(rel=2)
        result = list(ir_measures.ranx.iter_calc([measure], qrels, run))
        self.assertEqual(result[0], Metric('0', measure, 0.))


if __name__ == '__main__':
    unittest.main()
