import os
import unittest
import itertools
import ir_measures
from ir_measures import *


class TestCwlEval(unittest.TestCase):

    def test_measures(self):
        qrels = list(ir_measures.read_trec_qrels(os.path.join(os.path.dirname(__file__), 'cwl.qrels')))
        run = list(ir_measures.read_trec_run(os.path.join(os.path.dirname(__file__), 'cwl.run')))
        provider = ir_measures.cwl_eval
        # based on a manual execution of cwl-eval
        expected_results = [
            [AP, [('T1', 0.7087), ('T2', 0.7438), ('T3', 0.3068)]],
            [BPM(T=1.0, max_rel=1)@20, [('T1', 1.0000), ('T2', 1.0000), ('T3', 0.1667)]],
            [BPM(T=2.0, max_rel=1)@10, [('T1', 0.6667), ('T2', 1.0000), ('T3', 0.2857)]],
            [INSQ(T=1.0, max_rel=1), [('T1', 0.5872), ('T2', 0.6629), ('T3', 0.0880)]],
            [INSQ(T=2.0, max_rel=1), [('T1', 0.4513), ('T2', 0.5068), ('T3', 0.1292)]],
            [INST(T=1.0, max_rel=1), [('T1', 0.7934), ('T2', 0.9226), ('T3', 0.0888)]],
            [INST(T=2.0, max_rel=1), [('T1', 0.5994), ('T2', 0.6924), ('T3', 0.1397)]],
            [SDCG(max_rel=1)@10, [('T1', 0.5645), ('T2', 0.6531), ('T3', 0.2848)]],
            [NERR8(max_rel=1)@10, [('T1', 1.0000), ('T2', 1.0000), ('T3', 0.1667)]],
            [NERR9(max_rel=1)@10, [('T1', 1.0000), ('T2', 1.0000), ('T3', 0.0680)]],
            [NERR10(p=0.8, max_rel=1), [('T1', 1.0000), ('T2', 1.0000), ('T3', 0.0888)]],
            [NERR11(T=2.0, max_rel=1), [('T1', 1.0000), ('T2', 1.0000), ('T3', 0.0691)]],
            [P@1, [('T1', 1.0000), ('T2', 1.0000), ('T3', 0.0000)]],
            [P@10, [('T1', 0.5000), ('T2', 0.6000), ('T3', 0.4000)]],
            [P@20, [('T1', 0.2500), ('T2', 0.3000), ('T3', 0.2000)]],
            [P@5, [('T1', 0.6000), ('T2', 0.6000), ('T3', 0.0000)]],
            [RBP(p=0.9, rel=1), [('T1', 0.3501), ('T2', 0.3996), ('T3', 0.1988)]],
            [RR, [('T1', 1.0000), ('T2', 1.0000), ('T3', 0.1667)]],
        ]
        for measure, expected in expected_results:
            with self.subTest(measure=measure):
                self.assertTrue(provider.supports(measure))
                results = list(provider.iter_calc([measure], qrels, run))
                for result, (query_id, value) in zip(results, expected):
                    self.assertAlmostEqual(result.query_id, query_id, delta=0.0001)
                    self.assertAlmostEqual(result.value, value, delta=0.0001)


if __name__ == '__main__':
    unittest.main()
