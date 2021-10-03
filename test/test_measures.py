import unittest
import itertools
import ir_measures

class TestMeasures(unittest.TestCase):

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
        result = list(measure.iter_calc(qrels, run))
        print(result)
        measure = ir_measures.P(rel=2)@5
        result = list(measure.iter_calc(qrels, run))
        print(result)
        measure = ir_measures.RR
        result = list(measure.iter_calc(qrels, run))
        print(result)
        measure = ir_measures.RR(rel=2)
        result = list(measure.iter_calc(qrels, run))
        print(result)
        measure = ir_measures.Rprec
        result = list(measure.iter_calc(qrels, run))
        print(result)
        measure = ir_measures.Rprec(rel=2)
        result = list(measure.iter_calc(qrels, run))
        print(result)
        measure = ir_measures.AP
        result = list(measure.iter_calc(qrels, run))
        print(result)
        measure = ir_measures.AP@2
        result = list(measure.iter_calc(qrels, run))
        print(result)
        measure = ir_measures.AP(rel=2)
        result = list(measure.iter_calc(qrels, run))
        print(result)
        measure = ir_measures.AP(rel=2)@2
        result = list(measure.iter_calc(qrels, run))
        print(result)
        measure = ir_measures.nDCG
        result = list(measure.iter_calc(qrels, run))
        print(result)
        measure = ir_measures.nDCG@2
        result = list(measure.iter_calc(qrels, run))
        print(result)
        measure = ir_measures.R@2
        result = list(measure.iter_calc(qrels, run))
        print(result)
        measure = ir_measures.R(rel=2)@2
        result = list(measure.iter_calc(qrels, run))
        print(result)
        measure = ir_measures.Bpref
        result = list(measure.iter_calc(qrels, run))
        print(result)
        measure = ir_measures.Bpref(rel=2)
        result = list(measure.iter_calc(qrels, run))
        print(result)
        measure = ir_measures.P(rel=(1, 2))@(1,5,10,20)
        result = list(measure.iter_calc(qrels, run))
        print(result)
        measure = ir_measures.Judged@5
        result = list(measure.iter_calc(qrels, run))
        print(result)
        measure = ir_measures.Judged@20
        result = list(measure.iter_calc(qrels, run))
        print(result)
        measure = ir_measures.ERR@2
        result = list(measure.iter_calc(qrels, run))
        print(result)
        measure = ir_measures.ERR@20
        result = list(measure.iter_calc(qrels, run))
        print(result)
        measure = ir_measures.nDCG(dcg='exp-log2')@2
        result = list(measure.iter_calc(qrels, run))
        print(result)
        measure = ir_measures.nDCG(dcg='exp-log2')@5
        result = list(measure.iter_calc(qrels, run))
        print(result)
        # measure = ir_measures.RBP(p=[0.5, 0.8, 1.0, 1.2, 1.5])
        # result = list(measure.iter_calc(qrels, run))
        # print(result)
        # measure = ir_measures.RBP(p=[0.5, 0.8, 1.0, 1.2, 1.5])@(1,5,10,20)
        # result = list(measure.iter_calc(qrels, run))
        # print(result)

    def test_measures(self):
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
        measures = ir_measures.util.flatten_measures([
            ir_measures.P(rel=[1,2])@[1,5,10,20,50,100],
            ir_measures.R(rel=[1,2])@[1,5,10,20,50,100],
            ir_measures.RR(rel=[1,2]),
            ir_measures.RR(rel=[1,2])@[1,5,10,20,50,100],
            ir_measures.Rprec(rel=[1,2]),
            ir_measures.AP(rel=[1,2]),
            ir_measures.AP(rel=[1,2])@[1,5,10,20,50,100],
            ir_measures.nDCG(dcg=['log2', 'exp-log2']),
            ir_measures.nDCG(dcg=['log2', 'exp-log2'])@[1,5,10,20,50,100],
            ir_measures.Bpref(rel=[1,2]),
            ir_measures.Judged@[1,5,10,20,50,100],
            ir_measures.ERR@[1,5,10,20,50,100],
            #disable RBP
            #ir_measures.RBP(p=[0.5, 0.8, 1.0, 1.2, 1.5]),
            #ir_measures.RBP(p=[0.5, 0.8, 1.0, 1.2, 1.5])@[1,5,10,20,50,100],
        ])
        providers = [v for k, v in ir_measures.providers.registry.items() if k != 'trectools']
        for measure in measures:
            values = [(next(p.iter_calc([measure], qrels, run)), p) for p in providers if p.supports(measure)]
            print(measure, len(values))
            for (v1, p1), (v2, p2) in itertools.combinations(values, 2):
                with self.subTest(measure=measure, p1=p1, p2=p2):
                    self.assertAlmostEqual(v1.value, v2.value, places=4, msg=str(measure))



if __name__ == '__main__':
    unittest.main()
