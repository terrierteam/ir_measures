import numpy
import unittest
import itertools
import ir_measures
from ir_measures import *
from ir_measures import Metric


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
        empty = []

        # qrels but no run
        self.assertEqual(set(ir_measures.iter_calc([P@5], qrels, empty)), {Metric('0', P@5, 0.), Metric('1', P@5, 0.)})
        self.assertEqual(set(ir_measures.gdeval.iter_calc([ERR@5], qrels, empty)), {Metric('0', ERR@5, 0.), Metric('1', ERR@5, 0.)})
        self.assertEqual(set(ir_measures.judged.iter_calc([Judged@5], qrels, empty)), {Metric('0', Judged@5, 0.), Metric('1', Judged@5, 0.)})
        self.assertEqual(set(ir_measures.msmarco.iter_calc([RR@5], qrels, empty)), {Metric('0', RR@5, 0.), Metric('1', RR@5, 0.)})
        self.assertEqual(set(ir_measures.pytrec_eval.iter_calc([P@5], qrels, empty)), {Metric('0', P@5, 0.), Metric('1', P@5, 0.)})
        self.assertEqual(set(ir_measures.trectools.iter_calc([P@5], qrels, empty)), {Metric('0', P@5, 0.), Metric('1', P@5, 0.)})
        self.assertEqual(set(ir_measures.cwl_eval.iter_calc([P@5], qrels, empty)), {Metric('0', P@5, 0.0), Metric('1', P@5, 0.0)})

        # run but no qrels
        self.assertEqual(list(ir_measures.iter_calc([P@5], empty, run)), [])
        self.assertEqual(list(ir_measures.gdeval.iter_calc([ERR@5], empty, run)), [])
        self.assertEqual(list(ir_measures.judged.iter_calc([Judged@5], empty, run)), [])
        self.assertEqual(list(ir_measures.msmarco.iter_calc([RR@5], empty, run)), [])
        self.assertEqual(list(ir_measures.pytrec_eval.iter_calc([P@5], empty, run)), [])
        self.assertEqual(list(ir_measures.trectools.iter_calc([P@5], empty, run)), [])
        self.assertEqual(list(ir_measures.cwl_eval.iter_calc([P@5], empty, run)), [])

        # both no run and no qrels
        self.assertEqual(list(ir_measures.iter_calc([P@5], empty, empty)), [])
        self.assertEqual(list(ir_measures.gdeval.iter_calc([ERR@5], empty, empty)), [])
        self.assertEqual(list(ir_measures.judged.iter_calc([Judged@5], empty, empty)), [])
        self.assertEqual(list(ir_measures.msmarco.iter_calc([RR@5], empty, empty)), [])
        self.assertEqual(list(ir_measures.pytrec_eval.iter_calc([P@5], empty, empty)), [])
        self.assertEqual(list(ir_measures.trectools.iter_calc([P@5], empty, empty)), [])
        self.assertEqual(list(ir_measures.cwl_eval.iter_calc([P@5], empty, empty)), [])

        # qrels but no run
        numpy.testing.assert_equal(ir_measures.calc_aggregate([P@5], qrels, empty), {P@5: 0.})
        numpy.testing.assert_equal(ir_measures.gdeval.calc_aggregate([ERR@5], qrels, empty), {ERR@5: 0.})
        numpy.testing.assert_equal(ir_measures.judged.calc_aggregate([Judged@5], qrels, empty), {Judged@5: 0.})
        numpy.testing.assert_equal(ir_measures.msmarco.calc_aggregate([RR@5], qrels, empty), {RR@5: 0.})
        numpy.testing.assert_equal(ir_measures.pytrec_eval.calc_aggregate([P@5], qrels, empty), {P@5: 0.})
        numpy.testing.assert_equal(ir_measures.trectools.calc_aggregate([P@5], qrels, empty), {P@5: 0.})
        numpy.testing.assert_equal(ir_measures.cwl_eval.calc_aggregate([P@5], qrels, empty), {P@5: 0.})

        # run but no qrels
        numpy.testing.assert_equal(ir_measures.calc_aggregate([P@5], empty, run), {P@5: float('NaN')})
        numpy.testing.assert_equal(ir_measures.gdeval.calc_aggregate([ERR@5], empty, run), {ERR@5: float('NaN')})
        numpy.testing.assert_equal(ir_measures.judged.calc_aggregate([Judged@5], empty, run), {Judged@5: float('NaN')})
        numpy.testing.assert_equal(ir_measures.msmarco.calc_aggregate([RR@5], empty, run), {RR@5: float('NaN')})
        numpy.testing.assert_equal(ir_measures.pytrec_eval.calc_aggregate([P@5], empty, run), {P@5: float('NaN')})
        numpy.testing.assert_equal(ir_measures.trectools.calc_aggregate([P@5], empty, run), {P@5: float('NaN')})
        numpy.testing.assert_equal(ir_measures.cwl_eval.calc_aggregate([P@5], empty, run), {P@5: float('NaN')})

        # both no run and no qrels
        numpy.testing.assert_equal(ir_measures.calc_aggregate([P@5], empty, empty), {P@5: float('NaN')})
        numpy.testing.assert_equal(ir_measures.gdeval.calc_aggregate([ERR@5], empty, empty), {ERR@5: float('NaN')})
        numpy.testing.assert_equal(ir_measures.judged.calc_aggregate([Judged@5], empty, empty), {Judged@5: float('NaN')})
        numpy.testing.assert_equal(ir_measures.msmarco.calc_aggregate([RR@5], empty, empty), {RR@5: float('NaN')})
        numpy.testing.assert_equal(ir_measures.pytrec_eval.calc_aggregate([P@5], empty, empty), {P@5: float('NaN')})
        numpy.testing.assert_equal(ir_measures.trectools.calc_aggregate([P@5], empty, empty), {P@5: float('NaN')})
        numpy.testing.assert_equal(ir_measures.cwl_eval.calc_aggregate([P@5], empty, empty), {P@5: float('NaN')})



if __name__ == '__main__':
    unittest.main()
