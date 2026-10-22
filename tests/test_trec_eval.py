import unittest
import ir_measures
from ir_measures import AP, RR, Rprec, NumRet, NumRel, P, R

try:
    from trec_eval.compat.ir_measures import TeRustProvider
except ImportError:
    TeRustProvider = None

QRELS = '''
0 0 D0 0
0 0 D1 1
0 0 D2 1
0 0 D3 2
0 0 D4 0
1 0 D0 1
1 0 D3 2
1 0 D5 2
'''
RUN = '''
0 0 D0 1 0.8 run
0 0 D2 2 0.7 run
0 0 D1 3 0.3 run
0 0 D3 4 0.4 run
0 0 D4 5 0.1 run
1 0 D1 1 0.8 run
1 0 D3 2 0.7 run
1 0 D4 3 0.3 run
1 0 D2 4 0.4 run
'''


@unittest.skipIf(TeRustProvider is None, 'trec-eval (te-rust) not installed')
class TestTrecEval(unittest.TestCase):

    def setUp(self):
        self.qrels = list(ir_measures.read_trec_qrels(QRELS))
        self.run = list(ir_measures.read_trec_run(RUN))
        self.provider = TeRustProvider()

    def test_matches_pytrec_eval(self):
        measures = [AP, RR, Rprec, NumRet, NumRel, P@2, P@5(rel=2)]
        expected = ir_measures.pytrec_eval.calc_aggregate(measures, self.qrels, self.run)
        actual = self.provider.calc_aggregate(measures, self.qrels, self.run)
        self.assertEqual(set(expected), set(actual))
        for m in measures:
            with self.subTest(measure=m):
                self.assertAlmostEqual(actual[m], expected[m], places=6)

    def test_iter_calc(self):
        measures = [AP, RR, R@1, R@5(rel=2)]
        expected = {(r.query_id, r.measure): r.value for r in ir_measures.pytrec_eval.iter_calc(measures, self.qrels, self.run)}
        actual = {(r.query_id, r.measure): r.value for r in self.provider.iter_calc(measures, self.qrels, self.run)}
        self.assertEqual(expected.keys(), actual.keys())
        for k in expected:
            self.assertAlmostEqual(actual[k], expected[k], places=6)


if __name__ == '__main__':
    unittest.main()
