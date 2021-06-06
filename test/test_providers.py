import unittest
import itertools
import ir_measures
from ir_measures import *


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
        self.assertEqual(list(ir_measures.iter_calc([P@5], qrels, empty)), [])
        self.assertEqual(list(ir_measures.gdeval.iter_calc([ERR@5], qrels, empty)), [])
        self.assertEqual(list(ir_measures.judged.iter_calc([Judged@5], qrels, empty)), [])
        self.assertEqual(list(ir_measures.msmarco.iter_calc([RR@5], qrels, empty)), [])
        self.assertEqual(list(ir_measures.pytrec_eval.iter_calc([P@5], qrels, empty)), [])
        self.assertEqual(list(ir_measures.trectools.iter_calc([P@5], qrels, empty)), [])

        # run but no qrels
        self.assertEqual(list(ir_measures.iter_calc([P@5], empty, run)), [])
        self.assertEqual(list(ir_measures.gdeval.iter_calc([ERR@5], empty, run)), [])
        self.assertEqual(list(ir_measures.judged.iter_calc([Judged@5], empty, run)), [])
        self.assertEqual(list(ir_measures.msmarco.iter_calc([RR@5], empty, run)), [])
        self.assertEqual(list(ir_measures.pytrec_eval.iter_calc([P@5], empty, run)), [])
        self.assertEqual(list(ir_measures.trectools.iter_calc([P@5], empty, run)), [])

        # both no run and no qrels
        self.assertEqual(list(ir_measures.iter_calc([P@5], empty, empty)), [])
        self.assertEqual(list(ir_measures.gdeval.iter_calc([ERR@5], empty, empty)), [])
        self.assertEqual(list(ir_measures.judged.iter_calc([Judged@5], empty, empty)), [])
        self.assertEqual(list(ir_measures.msmarco.iter_calc([RR@5], empty, empty)), [])
        self.assertEqual(list(ir_measures.pytrec_eval.iter_calc([P@5], empty, empty)), [])
        self.assertEqual(list(ir_measures.trectools.iter_calc([P@5], empty, empty)), [])



if __name__ == '__main__':
    unittest.main()
