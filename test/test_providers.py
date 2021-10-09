import numpy
import unittest
import itertools
import ir_measures
from ir_measures import *
from ir_measures import Metric, CwlMetric


class TestPytrecEval(unittest.TestCase):

    def test_empty(self):
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
        partial_qrels = [q for q in qrels if q.query_id == '0']
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
        partial_run = [r for r in run if r.query_id == '0']
        empty = []

        # qrels but no run
        self.assertEqual(set(ir_measures.iter_calc([P@5], qrels, empty)), {Metric('0', P@5, 0.), Metric('1', P@5, 0.)})
        self.assertEqual(set(ir_measures.gdeval.iter_calc([ERR@5], qrels, empty)), {Metric('0', ERR@5, 0.), Metric('1', ERR@5, 0.)})
        self.assertEqual(set(ir_measures.judged.iter_calc([Judged@5], qrels, empty)), {Metric('0', Judged@5, 0.), Metric('1', Judged@5, 0.)})
        self.assertEqual(set(ir_measures.msmarco.iter_calc([RR@5], qrels, empty)), {Metric('0', RR@5, 0.), Metric('1', RR@5, 0.)})
        self.assertEqual(set(ir_measures.pytrec_eval.iter_calc([P@5], qrels, empty)), {Metric('0', P@5, 0.), Metric('1', P@5, 0.)})
        self.assertEqual(set(ir_measures.trectools.iter_calc([P@5], qrels, empty)), {Metric('0', P@5, 0.), Metric('1', P@5, 0.)})
        self.assertEqual(set(ir_measures.cwl_eval.iter_calc([P@5], qrels, empty)), {Metric('0', P@5, 0.0), Metric('1', P@5, 0.0)})
        self.assertEqual(set(ir_measures.compat.iter_calc([Compat(p=0.8)], qrels, empty)), {Metric('0', Compat(p=0.8), 0.0), Metric('1', Compat(p=0.8), 0.0)})

        # qrels but partial run
        self.assertEqual(set(ir_measures.iter_calc([P@5], qrels, partial_run)), {Metric('0', P@5, 0.6), Metric('1', P@5, 0.)})
        self.assertEqual(set(ir_measures.gdeval.iter_calc([ERR@5], qrels, partial_run)), {Metric('0', ERR@5, 0.10175), Metric('1', ERR@5, 0.)})
        self.assertEqual(set(ir_measures.judged.iter_calc([Judged@5], qrels, partial_run)), {Metric('0', Judged@5, 1.), Metric('1', Judged@5, 0.)})
        self.assertEqual(set(ir_measures.msmarco.iter_calc([RR@5], qrels, partial_run)), {Metric('0', RR@5, 0.5), Metric('1', RR@5, 0.)})
        self.assertEqual(set(ir_measures.pytrec_eval.iter_calc([P@5], qrels, partial_run)), {Metric('0', P@5, 0.6), Metric('1', P@5, 0.)})
        self.assertEqual(set(ir_measures.trectools.iter_calc([P@5], qrels, partial_run)), {Metric('0', P@5, 0.6), Metric('1', P@5, 0.)})
        self.assertEqual(set(ir_measures.cwl_eval.iter_calc([P@5], qrels, partial_run)), {CwlMetric('0', P@5, 0.6000000000000001, 3.0, 1.0, 5.0, 5.0), Metric('1', P@5, 0.0)})
        self.assertEqual(set(ir_measures.compat.iter_calc([Compat(p=0.8)], qrels, partial_run)), {Metric('0', Compat(p=0.8), 0.4744431703672816), Metric('1', Compat(p=0.8), 0.0)})

        # run but no qrels
        self.assertEqual(list(ir_measures.iter_calc([P@5], empty, run)), [])
        self.assertEqual(list(ir_measures.gdeval.iter_calc([ERR@5], empty, run)), [])
        self.assertEqual(list(ir_measures.judged.iter_calc([Judged@5], empty, run)), [])
        self.assertEqual(list(ir_measures.msmarco.iter_calc([RR@5], empty, run)), [])
        self.assertEqual(list(ir_measures.pytrec_eval.iter_calc([P@5], empty, run)), [])
        self.assertEqual(list(ir_measures.trectools.iter_calc([P@5], empty, run)), [])
        self.assertEqual(list(ir_measures.cwl_eval.iter_calc([P@5], empty, run)), [])
        self.assertEqual(list(ir_measures.compat.iter_calc([Compat(p=0.8)], empty, run)), [])

        # run but partial qrels
        self.assertEqual(set(ir_measures.iter_calc([P@5], partial_qrels, run)), {Metric('0', P@5, 0.6)})
        self.assertEqual(set(ir_measures.gdeval.iter_calc([ERR@5], partial_qrels, run)), {Metric('0', ERR@5, 0.10175)})
        self.assertEqual(set(ir_measures.judged.iter_calc([Judged@5], partial_qrels, run)), {Metric('0', Judged@5, 1.)})
        self.assertEqual(set(ir_measures.msmarco.iter_calc([RR@5], partial_qrels, run)), {Metric('0', RR@5, 0.5)})
        self.assertEqual(set(ir_measures.pytrec_eval.iter_calc([P@5], partial_qrels, run)), {Metric('0', P@5, 0.6)})
        self.assertEqual(set(ir_measures.trectools.iter_calc([P@5], partial_qrels, run)), {Metric('0', P@5, 0.6)})
        self.assertEqual(set(ir_measures.cwl_eval.iter_calc([P@5], partial_qrels, run)), {CwlMetric('0', P@5, 0.6000000000000001, 3.0, 1.0, 5.0, 5.0)})
        self.assertEqual(set(ir_measures.compat.iter_calc([Compat(p=0.8)], partial_qrels, run)), {Metric('0', Compat(p=0.8), 0.4744431703672816)})

        # both no run and no qrels
        self.assertEqual(list(ir_measures.iter_calc([P@5], empty, empty)), [])
        self.assertEqual(list(ir_measures.gdeval.iter_calc([ERR@5], empty, empty)), [])
        self.assertEqual(list(ir_measures.judged.iter_calc([Judged@5], empty, empty)), [])
        self.assertEqual(list(ir_measures.msmarco.iter_calc([RR@5], empty, empty)), [])
        self.assertEqual(list(ir_measures.pytrec_eval.iter_calc([P@5], empty, empty)), [])
        self.assertEqual(list(ir_measures.trectools.iter_calc([P@5], empty, empty)), [])
        self.assertEqual(list(ir_measures.cwl_eval.iter_calc([P@5], empty, empty)), [])
        self.assertEqual(list(ir_measures.compat.iter_calc([Compat(p=0.8)], empty, empty)), [])

        # qrels but no run
        numpy.testing.assert_equal(ir_measures.calc_aggregate([P@5], qrels, empty), {P@5: 0.})
        numpy.testing.assert_equal(ir_measures.gdeval.calc_aggregate([ERR@5], qrels, empty), {ERR@5: 0.})
        numpy.testing.assert_equal(ir_measures.judged.calc_aggregate([Judged@5], qrels, empty), {Judged@5: 0.})
        numpy.testing.assert_equal(ir_measures.msmarco.calc_aggregate([RR@5], qrels, empty), {RR@5: 0.})
        numpy.testing.assert_equal(ir_measures.pytrec_eval.calc_aggregate([P@5], qrels, empty), {P@5: 0.})
        numpy.testing.assert_equal(ir_measures.trectools.calc_aggregate([P@5], qrels, empty), {P@5: 0.})
        numpy.testing.assert_equal(ir_measures.cwl_eval.calc_aggregate([P@5], qrels, empty), {P@5: 0.})
        numpy.testing.assert_equal(ir_measures.compat.calc_aggregate([Compat(p=0.8)], qrels, empty), {Compat(p=0.8): 0.})

        # qrels but partial run
        numpy.testing.assert_equal(ir_measures.calc_aggregate([P@5], qrels, partial_run), {P@5: 0.3})
        numpy.testing.assert_equal(ir_measures.gdeval.calc_aggregate([ERR@5], qrels, partial_run), {ERR@5: 0.050875})
        numpy.testing.assert_equal(ir_measures.judged.calc_aggregate([Judged@5], qrels, partial_run), {Judged@5: 0.5})
        numpy.testing.assert_equal(ir_measures.msmarco.calc_aggregate([RR@5], qrels, partial_run), {RR@5: 0.25})
        numpy.testing.assert_equal(ir_measures.pytrec_eval.calc_aggregate([P@5], qrels, partial_run), {P@5: 0.3})
        numpy.testing.assert_equal(ir_measures.trectools.calc_aggregate([P@5], qrels, partial_run), {P@5: 0.3})
        numpy.testing.assert_equal(ir_measures.cwl_eval.calc_aggregate([P@5], qrels, partial_run), {P@5: 0.30000000000000004})
        numpy.testing.assert_equal(ir_measures.compat.calc_aggregate([Compat(p=0.8)], qrels, partial_run), {Compat(p=0.8): 0.2372215851836408})

        # run but no qrels
        numpy.testing.assert_equal(ir_measures.calc_aggregate([P@5], empty, run), {P@5: float('NaN')})
        numpy.testing.assert_equal(ir_measures.gdeval.calc_aggregate([ERR@5], empty, run), {ERR@5: float('NaN')})
        numpy.testing.assert_equal(ir_measures.judged.calc_aggregate([Judged@5], empty, run), {Judged@5: float('NaN')})
        numpy.testing.assert_equal(ir_measures.msmarco.calc_aggregate([RR@5], empty, run), {RR@5: float('NaN')})
        numpy.testing.assert_equal(ir_measures.pytrec_eval.calc_aggregate([P@5], empty, run), {P@5: float('NaN')})
        numpy.testing.assert_equal(ir_measures.trectools.calc_aggregate([P@5], empty, run), {P@5: float('NaN')})
        numpy.testing.assert_equal(ir_measures.cwl_eval.calc_aggregate([P@5], empty, run), {P@5: float('NaN')})
        numpy.testing.assert_equal(ir_measures.compat.calc_aggregate([Compat(p=0.8)], empty, run), {Compat(p=0.8): float('NaN')})

        # run but partial qrels
        numpy.testing.assert_equal(ir_measures.calc_aggregate([P@5], partial_qrels, run), {P@5: 0.6})
        numpy.testing.assert_equal(ir_measures.gdeval.calc_aggregate([ERR@5], partial_qrels, run), {ERR@5: 0.10175})
        numpy.testing.assert_equal(ir_measures.judged.calc_aggregate([Judged@5], partial_qrels, run), {Judged@5: 1.0})
        numpy.testing.assert_equal(ir_measures.msmarco.calc_aggregate([RR@5], partial_qrels, run), {RR@5: 0.5})
        numpy.testing.assert_equal(ir_measures.pytrec_eval.calc_aggregate([P@5], partial_qrels, run), {P@5: 0.6})
        numpy.testing.assert_equal(ir_measures.trectools.calc_aggregate([P@5], partial_qrels, run), {P@5: 0.6})
        numpy.testing.assert_equal(ir_measures.cwl_eval.calc_aggregate([P@5], partial_qrels, run), {P@5: 0.6000000000000001})
        numpy.testing.assert_equal(ir_measures.compat.calc_aggregate([Compat(p=0.8)], partial_qrels, run), {Compat(p=0.8): 0.4744431703672816})

        # both no run and no qrels
        numpy.testing.assert_equal(ir_measures.calc_aggregate([P@5], empty, empty), {P@5: float('NaN')})
        numpy.testing.assert_equal(ir_measures.gdeval.calc_aggregate([ERR@5], empty, empty), {ERR@5: float('NaN')})
        numpy.testing.assert_equal(ir_measures.judged.calc_aggregate([Judged@5], empty, empty), {Judged@5: float('NaN')})
        numpy.testing.assert_equal(ir_measures.msmarco.calc_aggregate([RR@5], empty, empty), {RR@5: float('NaN')})
        numpy.testing.assert_equal(ir_measures.pytrec_eval.calc_aggregate([P@5], empty, empty), {P@5: float('NaN')})
        numpy.testing.assert_equal(ir_measures.trectools.calc_aggregate([P@5], empty, empty), {P@5: float('NaN')})
        numpy.testing.assert_equal(ir_measures.cwl_eval.calc_aggregate([P@5], empty, empty), {P@5: float('NaN')})
        numpy.testing.assert_equal(ir_measures.compat.calc_aggregate([Compat(p=0.8)], empty, empty), {Compat(p=0.8): float('NaN')})



if __name__ == '__main__':
    unittest.main()
