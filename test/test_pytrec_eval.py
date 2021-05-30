import unittest
import itertools
import ir_measures


class TestPytrecEval(unittest.TestCase):

    def test_NumRet(self):
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
        provider = ir_measures.providers.PytrecEvalProvider()
        measure = ir_measures.NumRet
        result = list(provider.iter_calc([measure], qrels, run))
        self.assertEqual(result[0].query_id, "0")
        self.assertEqual(result[0].value, 5)
        self.assertEqual(result[1].query_id, "1")
        self.assertEqual(result[1].value, 4)
        self.assertEqual(provider.calc_aggregate([measure], qrels, run)[measure], 9)

        measure = ir_measures.NumRet(rel=1)
        result = list(provider.iter_calc([measure], qrels, run))
        self.assertEqual(result[0].query_id, "0")
        self.assertEqual(result[0].value, 3)
        self.assertEqual(result[1].query_id, "1")
        self.assertEqual(result[1].value, 1)
        self.assertEqual(provider.calc_aggregate([measure], qrels, run)[measure], 4)

        measure = ir_measures.NumRet(rel=2)
        result = list(provider.iter_calc([measure], qrels, run))
        self.assertEqual(result[0].query_id, "0")
        self.assertEqual(result[0].value, 1)
        self.assertEqual(result[1].query_id, "1")
        self.assertEqual(result[1].value, 1)
        self.assertEqual(provider.calc_aggregate([measure], qrels, run)[measure], 2)

        measure = ir_measures.NumRet(rel=3)
        result = list(provider.iter_calc([measure], qrels, run))
        self.assertEqual(result[0].query_id, "0")
        self.assertEqual(result[0].value, 0)
        self.assertEqual(result[1].query_id, "1")
        self.assertEqual(result[1].value, 0)
        self.assertEqual(provider.calc_aggregate([measure], qrels, run)[measure], 0)

    def test_NumQ(self):
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
        provider = ir_measures.providers.PytrecEvalProvider()
        measure = ir_measures.NumQ
        result = list(provider.iter_calc([measure], qrels, run))
        self.assertEqual(result[0].query_id, "0")
        self.assertEqual(result[0].value, 1)
        self.assertEqual(result[1].query_id, "1")
        self.assertEqual(result[1].value, 1)
        self.assertEqual(provider.calc_aggregate([measure], qrels, run)[measure], 2)

    def test_NumRel(self):
        qrels = list(ir_measures.read_trec_qrels('''
0 0 D0 0
0 0 D1 1
0 0 D2 1
0 0 D3 2
0 0 D4 0
1 0 D0 1
1 0 D3 2
1 0 D5 0
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
        provider = ir_measures.providers.PytrecEvalProvider()
        measure = ir_measures.NumRel
        result = list(provider.iter_calc([measure], qrels, run))
        self.assertEqual(result[0].query_id, "0")
        self.assertEqual(result[0].value, 3)
        self.assertEqual(result[1].query_id, "1")
        self.assertEqual(result[1].value, 2)
        self.assertEqual(provider.calc_aggregate([measure], qrels, run)[measure], 5)


    def test_Success(self):
        qrels = list(ir_measures.read_trec_qrels('''
0 0 D0 0
0 0 D1 1
0 0 D2 2
0 0 D3 2
0 0 D4 0
1 0 D0 1
1 0 D3 2
1 0 D5 0
'''))
        run = list(ir_measures.read_trec_run('''
0 0 D0 1 0.8 run
0 0 D2 2 0.7 run
0 0 D1 3 0.3 run
0 0 D3 4 0.4 run
0 0 D4 5 0.1 run
1 0 D1 1 0.8 run
1 0 D4 2 0.7 run
1 0 D3 3 0.3 run
1 0 D2 4 0.4 run
'''))
        provider = ir_measures.providers.PytrecEvalProvider()
        measure = ir_measures.Success@2
        result = list(provider.iter_calc([measure], qrels, run))
        self.assertEqual(result[0].query_id, "0")
        self.assertEqual(result[0].value, 1)
        self.assertEqual(result[1].query_id, "1")
        self.assertEqual(result[1].value, 0)
        self.assertEqual(provider.calc_aggregate([measure], qrels, run)[measure], 0.5)

        measure = ir_measures.Success(rel=2)@2
        result = list(provider.iter_calc([measure], qrels, run))
        self.assertEqual(result[0].query_id, "0")
        self.assertEqual(result[0].value, 1)
        self.assertEqual(result[1].query_id, "1")
        self.assertEqual(result[1].value, 0)
        self.assertEqual(provider.calc_aggregate([measure], qrels, run)[measure], 0.5)

        measure = ir_measures.Success(rel=3)@2
        result = list(provider.iter_calc([measure], qrels, run))
        self.assertEqual(result[0].query_id, "0")
        self.assertEqual(result[0].value, 0)
        self.assertEqual(result[1].query_id, "1")
        self.assertEqual(result[1].value, 0)
        self.assertEqual(provider.calc_aggregate([measure], qrels, run)[measure], 0)

    def test_SetP(self):
        qrels = list(ir_measures.read_trec_qrels('''
0 0 D0 0
0 0 D1 1
0 0 D2 2
0 0 D3 2
0 0 D4 0
1 0 D0 1
1 0 D3 2
1 0 D5 0
'''))
        run = list(ir_measures.read_trec_run('''
0 0 D0 1 0.8 run
0 0 D2 2 0.7 run
0 0 D1 3 0.3 run
0 0 D3 4 0.4 run
0 0 D4 5 0.1 run
1 0 D1 1 0.8 run
1 0 D4 2 0.7 run
1 0 D3 3 0.3 run
1 0 D2 4 0.4 run
'''))
        provider = ir_measures.providers.PytrecEvalProvider()
        measure = ir_measures.SetP(rel=1)
        result = list(provider.iter_calc([measure], qrels, run))
        self.assertEqual(result[0].query_id, "0")
        self.assertEqual(result[0].value, .6)
        self.assertEqual(result[1].query_id, "1")
        self.assertEqual(result[1].value, .25)
        self.assertEqual(provider.calc_aggregate([measure], qrels, run)[measure], 0.425)

        measure = ir_measures.SetRelP(rel=1)
        result = list(provider.iter_calc([measure], qrels, run))
        self.assertEqual(result[0].query_id, "0")
        self.assertEqual(result[0].value, 1.0)
        self.assertEqual(result[1].query_id, "1")
        self.assertEqual(result[1].value, .5)
        self.assertEqual(provider.calc_aggregate([measure], qrels, run)[measure], 0.75)

        measure = ir_measures.SetP(rel=2)
        result = list(provider.iter_calc([measure], qrels, run))
        self.assertEqual(result[0].query_id, "0")
        self.assertEqual(result[0].value, .4)
        self.assertEqual(result[1].query_id, "1")
        self.assertEqual(result[1].value, .25)
        self.assertEqual(provider.calc_aggregate([measure], qrels, run)[measure], 0.325)

        measure = ir_measures.SetRelP(rel=2)
        result = list(provider.iter_calc([measure], qrels, run))
        self.assertEqual(result[0].query_id, "0")
        self.assertEqual(result[0].value, 1.0)
        self.assertEqual(result[1].query_id, "1")
        self.assertEqual(result[1].value, 1.0)
        self.assertEqual(provider.calc_aggregate([measure], qrels, run)[measure], 1.0)

        measure = ir_measures.SetP(rel=3)
        result = list(provider.iter_calc([measure], qrels, run))
        self.assertEqual(result[0].query_id, "0")
        self.assertEqual(result[0].value, 0)
        self.assertEqual(result[1].query_id, "1")
        self.assertEqual(result[1].value, 0)
        self.assertEqual(provider.calc_aggregate([measure], qrels, run)[measure], 0)

    def test_SetR(self):
        qrels = list(ir_measures.read_trec_qrels('''
0 0 D0 0
0 0 D1 1
0 0 D2 2
0 0 D3 2
0 0 D4 0
1 0 D0 1
1 0 D3 2
1 0 D5 0
'''))
        run = list(ir_measures.read_trec_run('''
0 0 D0 1 0.8 run
0 0 D2 2 0.7 run
0 0 D1 3 0.3 run
0 0 D3 4 0.4 run
0 0 D4 5 0.1 run
1 0 D1 1 0.8 run
1 0 D4 2 0.7 run
1 0 D3 3 0.3 run
1 0 D2 4 0.4 run
'''))
        provider = ir_measures.providers.PytrecEvalProvider()
        measure = ir_measures.SetR(rel=1)
        result = list(provider.iter_calc([measure], qrels, run))
        self.assertEqual(result[0].query_id, "0")
        self.assertEqual(result[0].value, 1.)
        self.assertEqual(result[1].query_id, "1")
        self.assertEqual(result[1].value, .5)
        self.assertEqual(provider.calc_aggregate([measure], qrels, run)[measure], 0.75)

        measure = ir_measures.SetR(rel=2)
        result = list(provider.iter_calc([measure], qrels, run))
        self.assertEqual(result[0].query_id, "0")
        self.assertEqual(result[0].value, 1.0)
        self.assertEqual(result[1].query_id, "1")
        self.assertEqual(result[1].value, 1.0)
        self.assertEqual(provider.calc_aggregate([measure], qrels, run)[measure], 1.0)

        measure = ir_measures.SetR(rel=3)
        result = list(provider.iter_calc([measure], qrels, run))
        self.assertEqual(result[0].query_id, "0")
        self.assertEqual(result[0].value, 0)
        self.assertEqual(result[1].query_id, "1")
        self.assertEqual(result[1].value, 0)
        self.assertEqual(provider.calc_aggregate([measure], qrels, run)[measure], 0)

    def test_SetAP(self):
        qrels = list(ir_measures.read_trec_qrels('''
0 0 D0 0
0 0 D1 1
0 0 D2 2
0 0 D3 2
0 0 D4 0
1 0 D0 1
1 0 D3 2
1 0 D5 0
'''))
        run = list(ir_measures.read_trec_run('''
0 0 D0 1 0.8 run
0 0 D2 2 0.7 run
0 0 D1 3 0.3 run
0 0 D3 4 0.4 run
0 0 D4 5 0.1 run
1 0 D1 1 0.8 run
1 0 D4 2 0.7 run
1 0 D3 3 0.3 run
1 0 D2 4 0.4 run
'''))
        provider = ir_measures.providers.PytrecEvalProvider()
        measure = ir_measures.SetAP(rel=1)
        result = list(provider.iter_calc([measure], qrels, run))
        self.assertEqual(result[0].query_id, "0")
        self.assertEqual(result[0].value, 0.6)
        self.assertEqual(result[1].query_id, "1")
        self.assertEqual(result[1].value, 0.125)
        self.assertEqual(provider.calc_aggregate([measure], qrels, run)[measure], 0.3625)

        measure = ir_measures.SetAP(rel=2)
        result = list(provider.iter_calc([measure], qrels, run))
        self.assertEqual(result[0].query_id, "0")
        self.assertEqual(result[0].value, 0.4)
        self.assertEqual(result[1].query_id, "1")
        self.assertEqual(result[1].value, 0.25)
        self.assertEqual(provider.calc_aggregate([measure], qrels, run)[measure], 0.325)

        measure = ir_measures.SetAP(rel=3)
        result = list(provider.iter_calc([measure], qrels, run))
        self.assertEqual(result[0].query_id, "0")
        self.assertEqual(result[0].value, 0)
        self.assertEqual(result[1].query_id, "1")
        self.assertEqual(result[1].value, 0)
        self.assertEqual(provider.calc_aggregate([measure], qrels, run)[measure], 0)

    def test_SetF(self):
        qrels = list(ir_measures.read_trec_qrels('''
0 0 D0 0
0 0 D1 1
0 0 D2 2
0 0 D3 2
0 0 D4 0
1 0 D0 1
1 0 D3 2
1 0 D5 0
'''))
        run = list(ir_measures.read_trec_run('''
0 0 D0 1 0.8 run
0 0 D2 2 0.7 run
0 0 D1 3 0.3 run
0 0 D3 4 0.4 run
0 0 D4 5 0.1 run
1 0 D1 1 0.8 run
1 0 D4 2 0.7 run
1 0 D3 3 0.3 run
1 0 D2 4 0.4 run
'''))
        provider = ir_measures.providers.PytrecEvalProvider()
        measure = ir_measures.SetF(rel=1)
        result = list(provider.iter_calc([measure], qrels, run))
        self.assertEqual(result[0].query_id, "0")
        self.assertAlmostEqual(result[0].value, 0.75, places=4)
        self.assertEqual(result[1].query_id, "1")
        self.assertAlmostEqual(result[1].value, .33333, places=4)
        self.assertAlmostEqual(provider.calc_aggregate([measure], qrels, run)[measure], 0.5417, places=4)

        measure = ir_measures.SetF(rel=1, beta=0.5)
        result = list(provider.iter_calc([measure], qrels, run))
        self.assertEqual(result[0].query_id, "0")
        self.assertAlmostEqual(result[0].value, 0.6923, places=4)
        self.assertEqual(result[1].query_id, "1")
        self.assertEqual(result[1].value, 0.3)
        self.assertAlmostEqual(provider.calc_aggregate([measure], qrels, run)[measure], 0.49615, places=4)

        measure = ir_measures.SetF(rel=1, beta=2.0)
        result = list(provider.iter_calc([measure], qrels, run))
        self.assertEqual(result[0].query_id, "0")
        self.assertAlmostEqual(result[0].value, 0.81818, places=4)
        self.assertEqual(result[1].query_id, "1")
        self.assertEqual(result[1].value, 0.375)
        self.assertAlmostEqual(provider.calc_aggregate([measure], qrels, run)[measure], 0.59659, places=4)

        measure = ir_measures.SetF(rel=3)
        result = list(provider.iter_calc([measure], qrels, run))
        self.assertEqual(result[0].query_id, "0")
        self.assertEqual(result[0].value, 0)
        self.assertEqual(result[1].query_id, "1")
        self.assertEqual(result[1].value, 0)
        self.assertEqual(provider.calc_aggregate([measure], qrels, run)[measure], 0)

        # make sure the multiple invocations hapen correctly
        res = provider.calc_aggregate([ir_measures.SetF(rel=1), ir_measures.SetF(rel=1, beta=0.5), ir_measures.SetF(rel=1, beta=2.0), ir_measures.SetF(rel=3)], qrels, run)
        self.assertAlmostEqual(res[ir_measures.SetF(rel=1)], 0.5417, places=4)
        self.assertAlmostEqual(res[ir_measures.SetF(rel=1, beta=0.5)], 0.49615, places=4)
        self.assertAlmostEqual(res[ir_measures.SetF(rel=1, beta=2.0)], 0.59659, places=4)
        self.assertEqual(res[ir_measures.SetF(rel=3)], 0)


    def test_IPrec(self):
        qrels = list(ir_measures.read_trec_qrels('''
0 0 D0 1
0 0 D1 1
0 0 D2 2
0 0 D3 2
0 0 D4 0
1 0 D0 1
1 0 D3 2
1 0 D5 0
'''))
        run = list(ir_measures.read_trec_run('''
0 0 D0 1 0.8 run
0 0 D2 2 0.7 run
0 0 D1 3 0.3 run
0 0 D3 4 0.4 run
0 0 D4 5 0.1 run
1 0 D1 1 0.8 run
1 0 D4 2 0.7 run
1 0 D3 3 0.3 run
1 0 D2 4 0.4 run
'''))
        provider = ir_measures.providers.PytrecEvalProvider()
        measure = ir_measures.IPrec@0.25
        result = list(provider.iter_calc([measure], qrels, run))
        self.assertEqual(result[0].query_id, "0")
        self.assertEqual(result[0].value, 1.0)
        self.assertEqual(result[1].query_id, "1")
        self.assertEqual(result[1].value, .25)
        self.assertEqual(provider.calc_aggregate([measure], qrels, run)[measure], 0.625)

        measure = ir_measures.IPrec@0.5
        result = list(provider.iter_calc([measure], qrels, run))
        self.assertEqual(result[0].query_id, "0")
        self.assertEqual(result[0].value, 1.0)
        self.assertEqual(result[1].query_id, "1")
        self.assertEqual(result[1].value, .25)
        self.assertEqual(provider.calc_aggregate([measure], qrels, run)[measure], 0.625)

        measure = ir_measures.IPrec@0.75
        result = list(provider.iter_calc([measure], qrels, run))
        self.assertEqual(result[0].query_id, "0")
        self.assertEqual(result[0].value, 1.0)
        self.assertEqual(result[1].query_id, "1")
        self.assertEqual(result[1].value, 0)
        self.assertEqual(provider.calc_aggregate([measure], qrels, run)[measure], 0.5)

        measure = ir_measures.IPrec(rel=2)@0.1
        result = list(provider.iter_calc([measure], qrels, run))
        self.assertEqual(result[0].query_id, "0")
        self.assertAlmostEqual(result[0].value, .6666666, places=4)
        self.assertEqual(result[1].query_id, "1")
        self.assertEqual(result[1].value, .25)
        self.assertAlmostEqual(provider.calc_aggregate([measure], qrels, run)[measure], 0.4583, places=4)

        measure = ir_measures.IPrec(rel=2)@0.25
        result = list(provider.iter_calc([measure], qrels, run))
        self.assertEqual(result[0].query_id, "0")
        self.assertAlmostEqual(result[0].value, .6666666, places=4)
        self.assertEqual(result[1].query_id, "1")
        self.assertEqual(result[1].value, .25)
        self.assertAlmostEqual(provider.calc_aggregate([measure], qrels, run)[measure], 0.4583, places=4)

        measure = ir_measures.IPrec(rel=2)@0.5
        result = list(provider.iter_calc([measure], qrels, run))
        self.assertEqual(result[0].query_id, "0")
        self.assertAlmostEqual(result[0].value, .6666666, places=4)
        self.assertEqual(result[1].query_id, "1")
        self.assertEqual(result[1].value, .25)
        self.assertAlmostEqual(provider.calc_aggregate([measure], qrels, run)[measure], 0.4583, places=4)

        measure = ir_measures.IPrec(rel=2)@0.75
        result = list(provider.iter_calc([measure], qrels, run))
        self.assertEqual(result[0].query_id, "0")
        self.assertAlmostEqual(result[0].value, .6666666, places=4)
        self.assertEqual(result[1].query_id, "1")
        self.assertEqual(result[1].value, .25)
        self.assertAlmostEqual(provider.calc_aggregate([measure], qrels, run)[measure], 0.4583, places=4)


    def test_infAP(self):
        qrels = list(ir_measures.read_trec_qrels('''
0 0 D0 1
0 0 D1 -1
0 0 D2 0
0 0 D3 2
0 0 D4 0
1 0 D0 1
1 0 D3 2
1 0 D4 -1
1 0 D5 0
'''))
        run = list(ir_measures.read_trec_run('''
0 0 D0 1 0.8 run
0 0 D2 2 0.7 run
0 0 D1 3 0.3 run
0 0 D3 4 0.4 run
0 0 D4 5 0.1 run
1 0 D1 1 0.8 run
1 0 D4 2 0.7 run
1 0 D3 3 0.3 run
1 0 D2 4 0.4 run
'''))
        provider = ir_measures.providers.PytrecEvalProvider()
        measure = ir_measures.AP
        result = list(provider.iter_calc([measure], qrels, run))
        self.assertEqual(result[0].query_id, "0")
        self.assertAlmostEqual(result[0].value, 0.8333, places=4)
        self.assertEqual(result[1].query_id, "1")
        self.assertEqual(result[1].value, .125)
        self.assertAlmostEqual(provider.calc_aggregate([measure], qrels, run)[measure], 0.47916666666666663, places=4)

        measure = ir_measures.infAP
        result = list(provider.iter_calc([measure], qrels, run))
        self.assertEqual(result[0].query_id, "0")
        self.assertAlmostEqual(result[0].value, 0.8333, places=4)
        self.assertEqual(result[1].query_id, "1")
        self.assertEqual(result[1].value, 0.1875)
        self.assertAlmostEqual(provider.calc_aggregate([measure], qrels, run)[measure], 0.510416, places=4)

        provider = ir_measures.providers.PytrecEvalProvider()
        measure = ir_measures.AP(rel=2)
        result = list(provider.iter_calc([measure], qrels, run))
        self.assertEqual(result[0].query_id, "0")
        self.assertAlmostEqual(result[0].value, 0.33333, places=4)
        self.assertEqual(result[1].query_id, "1")
        self.assertAlmostEqual(result[1].value, 0.25, places=4)
        self.assertAlmostEqual(provider.calc_aggregate([measure], qrels, run)[measure], 0.2917, places=4)

        measure = ir_measures.infAP(rel=2)
        result = list(provider.iter_calc([measure], qrels, run))
        self.assertEqual(result[0].query_id, "0")
        self.assertAlmostEqual(result[0].value, 0.33333, places=4)
        self.assertEqual(result[1].query_id, "1")
        self.assertAlmostEqual(result[1].value, 0.375, places=4)
        self.assertAlmostEqual(provider.calc_aggregate([measure], qrels, run)[measure], 0.3542, places=4)



if __name__ == '__main__':
    unittest.main()
